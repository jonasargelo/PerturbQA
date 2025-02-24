import os
import csv
import json

import importlib.resources


def read_csv(fp):
    """
    Convert label to int
    """
    with importlib.resources.open_text("perturbqa.datasets", fp) as f:
        reader = csv.DictReader(f)
        data = []
        for item in reader:
            if "label" in item:
                item["label"] = int(item["label"])
            data.append(item)
    return data


def load_de(dataset_name):
    """
    Load differential expression dataset
    """
    fp = f"{dataset_name}-de.csv"
    try:
        items = read_csv(fp)
    except:
        options = ["k562", "rpe1", "hepg2", "jurkat", "k562_set"]
        raise Exception(f"Invalid dataset: {dataset_name}. Options: {options}")
    # organize by split
    data = {"train": [], "test": []}
    for item in items:
        data[item["split"]].append(item)
        del item["split"]
    return data


def load_dir(dataset_name):
    """
    Load direction of change dataset
    """
    fp = f"{dataset_name}-dir.csv"
    try:
        items = read_csv(fp)
    except:
        options = ["k562", "rpe1", "hepg2", "jurkat", "k562_set"]
        raise Exception(f"Invalid dataset: {dataset_name}. Options: {options}")
    # organize by split
    data = {"train": [], "test": []}
    for item in items:
        data[item["split"]].append(item)
        del item["split"]
    return data


def load_gse(dataset_name, skip_empty=True):
    """
    Load direction of change dataset
    """
    fp = f"k562_{dataset_name}-gse.json"
    try:
        with importlib.resources.open_text("perturbqa.datasets", fp) as f:
            data = json.load(f)
    except:
        options = ["pert", "gene"]
        raise Exception(f"Invalid dataset: {dataset_name}. Options: {options}")
    if skip_empty:
        data = [x for x in data if x["label"] is not None]
    return data


