"""
scDataset is a single dataset

DataModule is lightning's entrypoint into all data-related objects.
"""

import os
import csv
import json
import yaml
import itertools
from functools import partial
from collections import defaultdict

from tqdm import tqdm
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl

from torch.utils.data import DataLoader, Dataset, Subset
from torch.utils.data import default_collate
from torch.nn.utils.rnn import pad_sequence

from torch_geometric.data import Data



def get_dataset(args):
    if "mlp" in args.model:
        return scDataset(args)
    elif "kg_gnn" in args.model:
        return KGPyGDataset(args)


class scDataset(Dataset):
    """
    Single-cell dataset
    """
    def __init__(self, args):
        super().__init__()
        self.args = args
        # load raw data items
        data, splits, perts, genes = self._load_data(args.data_file)
        self.data = data  # list(dict)
        self.splits = splits  # dict: split -> index
        # vocabulary of genes + tokenizer
        self.vocab = sorted(perts.union(genes))
        tokenizer = {token:i+1 for i,token in enumerate(self.vocab)}
        tokenizer[None] = 0  # padding
        self._tokenize("pert", tokenizer)
        self._tokenize("gene", tokenizer)
        self.tokenizer = tokenizer
        # this is bad practice !!! teeheehee
        args.vocab_size = len(tokenizer)

        # (optional) load pathways
        if "pathway" in args.model:
            self.params = self._load_pathways()

    def _tokenize(self, key, tokenizer):
        """
        Modiies self.data in place
        """
        for item in self.data:
            item[key] = tokenizer[item[key]]

    def _load_data(self, data_file):
        """
        Read CSV file
        """
        data = []
        splits = defaultdict(list)
        perts, genes = set(), set()
        with open(data_file) as f:
            reader = csv.DictReader(f)
            for item in reader:
                # DE vs. down vs. up
                label = int(item["label"])  # DE vs. not
                if item["direction"] == "1":
                    label = 2
                # 0-index, add index before appending to data
                splits[item["split"]].append(len(data))
                # now append to data
                item["label"] = label
                del item["direction"], item["split"]
                data.append(item)
                perts.add(item["pert"])
                genes.add(item["gene"])
                item["key"] = f'{item["pert"]},{item["gene"]}'
        return data, splits, perts, genes

    def _load_pathways(self):
        with open(self.args.pathway_file) as f:
            path_to_gene = json.load(f)
        # update tokenizer and vocab
        for nodes in sorted(path_to_gene.values()):
            for node in nodes:
                if node not in self.tokenizer:
                    self.tokenizer[node] = len(self.tokenizer)
        self.vocab = list(self.tokenizer)
        self.args.vocab_size = len(self.vocab)
        # canonical ordering
        paths = sorted(path_to_gene)
        path_to_idx = {path:i for i,path in enumerate(paths)}
        # tokens, for the model
        max_len = max(len(nodes) for nodes in path_to_gene.values())
        # +1 since "gene" is +1'd (legacy for padding)
        tokens = torch.zeros(len(paths)+1, max_len, dtype=torch.long)
        mask = torch.zeros(len(paths)+1, max_len, dtype=torch.long)
        for i, path in enumerate(paths):
            cur_len = len(path_to_gene[path])
            cur_tokens = torch.tensor(
                [self.tokenizer[node] for node in path_to_gene[path]])
            tokens[i+1][:cur_len] = cur_tokens
            mask[i+1][:cur_len] = torch.ones_like(cur_tokens)
        return tokens, mask

        self.length = len(self.data)

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        return self.data[idx]


class KGPyGDataset(scDataset):
    """
    Knowledge-graph powered single-cell dataset
    """
    def __init__(self, args):
        super().__init__(args)
        # load graph and add missing nodes as singletons
        graph = load_graph(args.graph_config_file)
        # update tokenizer and vocab
        for node in sorted(graph[0]):
            if node not in self.tokenizer:
                self.tokenizer[node] = len(self.tokenizer)
        self.vocab = list(self.tokenizer)
        args.vocab_size = len(self.vocab)
        self.graph = self.convert_to_pyg(*graph[1:])

    def convert_to_pyg(self, edge_index, edge_attr):
        """
        Preprocess graph into PyG Data object
        """
        # nodes: genes and pathways
        nodes = torch.arange(len(self.vocab))
        # edges of all sorts
        edge_index = torch.tensor([
            [self.tokenizer[x1], self.tokenizer[x2]]
            for x1, x2 in edge_index]
        )
        # knowledge graph identities
        attr_to_idx = {attr:i for i, attr in
            enumerate(sorted(set(edge_attr)))
        }
        self.args.num_kgs = len(attr_to_idx)  # teehee
        edge_attr = torch.tensor(
            [attr_to_idx[attr] for attr in edge_attr]
        )
        # create big graph object
        data = Data(x=nodes,
                    edge_index=edge_index,
                    edge_attr=edge_attr)
        return data


def load_graph(graph_file):
    """
    Parses processed knowledge graphs into networkx graph over
    genes and pathways
    """
    graph_file_cache = graph_file.replace("yaml", "json")
    if os.path.exists(graph_file_cache):
        with open(graph_file_cache) as f:
            return json.load(f)

    # otherwise, process each graph
    with open(graph_file) as f:
        graph_paths = yaml.safe_load(f)

    # gene to gene graphs
    nodes = set()
    edge_index = []  # keeps track of edges
    edge_attr = []  # keeps track of source graph
    for path in graph_paths["pairwise"]:
        graph = _read_graph(path, bipartite=False)
        nodes.update(graph[0])
        edge_index.extend(graph[1])
        edge_attr.extend(graph[2])

    # gene to pathway graphs
    for path in graph_paths["bipartite"]:
        graph = _read_graph(path, bipartite=True)
        nodes.update(graph[0])
        edge_index.extend(graph[1])
        edge_attr.extend(graph[2])
    nodes = sorted(nodes)

    # save to cache
    with open(graph_file_cache, "w+") as f:
        json.dump([nodes, edge_index, edge_attr], f)
    return nodes, edge_index, edge_attr


def _read_graph(path, bipartite=False):
    """
    not bipartite: gene to gene graphs
    bipartite: gene to pathway graphs
    """
    name = path.split("/")[-1].split(".json")[0]
    edge_index = []
    nodes = set()
    with open(path) as f:
        graph = json.load(f)
        if bipartite:
            graph = graph[0]
        for node1, edges in graph.items():
            nodes.add(node1)
            for node2, _ in edges:
                nodes.add(node2)
                edge_index.append([node1, node2])
                edge_index.append([node2, node1])
    edge_attr = [name] * len(edge_index)
    return nodes, edge_index, edge_attr


def get_neighbors(graph, node, k, pad=True):
    """
    BFS until we get k neighbors (or exhaust subgraph)
    """
    neighbors = [node]
    nodes_to_see = [node]
    cur_pointer = 0
    while len(neighbors) < k:
        cur_node = nodes_to_see[cur_pointer]
        neighbors.append(cur_node)
        new_nodes = graph.neighbors(cur_node)
        # nodes before cur_pointer are seen
        # those after are to-be-seen (don't add twice)
        nodes_to_see.extend([x for x in new_nodes if x not in
            nodes_to_see])
        cur_pointer += 1
        # no more new nodes
        if cur_pointer == len(nodes_to_see):
            break
    # add padding if needed
    deficit = k - len(neighbors)
    if pad and deficit > 0:
        neighbors.extend([None] * deficit)
    return neighbors


class DataModule(pl.LightningDataModule):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.seed = args.seed
        self.batch_size = args.batch_size
        self.num_workers = args.num_workers
        self.data_file = args.data_file

        dataset = get_dataset(args)
        delim = int(len(dataset.splits["train"]) *
                    args.val_proportion)
        self.subset_train = Subset(dataset,
                dataset.splits["train"][delim:])
        self.subset_val = Subset(dataset,
                dataset.splits["train"][:delim])
        if "kg" in args.model:
            self.graph = dataset.graph
        if "pathway" in args.model:
            self.params = dataset.params

    def train_dataloader(self):
        train_loader = DataLoader(self.subset_train,
                                  batch_size=self.batch_size,
                                  num_workers=self.num_workers,
                                  shuffle=True,
                                  pin_memory=True,
                                  #persistent_workers=(not self.args.debug),
                                  collate_fn=partial(collate, self.args))
        return train_loader

    def val_dataloader(self):
        # batch_size smaller since we sample more batches on average
        val_loader = DataLoader(self.subset_val,
                                batch_size=self.batch_size,
                                num_workers=self.num_workers,
                                shuffle=False,
                                pin_memory=True,
                                #persistent_workers=(not self.args.debug),
                                collate_fn=partial(collate, self.args))
        return val_loader


class InferenceDataModule(pl.LightningDataModule):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.seed = args.seed
        self.batch_size = args.batch_size
        self.num_workers = args.num_workers
        self.data_file = args.data_file

        dataset = get_dataset(args)
        self.subsets = []
        for key in ["test_cond", "test_gene", "test"]:
            self.subsets.append(Subset(dataset,
                dataset.splits[key]))
        if "kg" in args.model:
            self.graph = dataset.graph
        if "pathway" in args.model:
            self.params = dataset.params

    def predict_dataloader(self):
        test_loaders = []
        for subset in self.subsets:
            loader = DataLoader(subset,
                                batch_size=self.batch_size,
                                num_workers=self.num_workers,
                                shuffle=False,
                                pin_memory=False,
                                collate_fn=partial(collate, self.args))

            test_loaders.append(loader)
        return test_loaders

    def test_dataloader(self):
        return self.predict_dataloader()


def collate(args, batch):
    """
        Overwrite default_collate for jagged tensors
    """
    #if "gnn" in args.model:  # very different workflow
    #    return _collate_pyg(args, batch)
    # my default workflow
    keys = ["key", "pert", "gene", "label"]
    batch = {key:[item[key] for item in batch if key in item] for key in keys}
    new_batch = {}
    for key, val in batch.items():
        # different models
        if len(val) == 0:
            continue
        if key in ["path"]:
            new_batch[key] = pad_sequence(val, batch_first=True)
        elif not torch.is_tensor(val[0]) or val[0].ndim == 0:
            new_batch[key] = default_collate(val)
        else:
            new_batch[key] = default_collate(val)
    return new_batch


def get_mask(lens, max_len=None):
    # mask where 0 is padding and 1 is token
    if max_len is None:
        max_len = lens.max()
    mask = torch.arange(max_len)[None, :] < lens[:, None]
    return mask

