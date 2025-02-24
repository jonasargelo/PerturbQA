import torch
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.nn import GATConv



class GAT(nn.Module):
    def __init__(self, args, graph):
        super().__init__()
        self.args = args
        self.embedding = nn.Embedding(args.vocab_size, args.embed_dim)
        self.edge_embedding = nn.Embedding(args.num_kgs, args.embed_dim)
        self.layers = nn.ModuleList([
            GATConv(args.embed_dim, args.embed_dim)
            for _ in range(args.num_layers)
        ])
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(args.embed_dim)
            for _ in range(args.num_layers)
        ])
        self.dropout = nn.Dropout(args.dropout)
        self.activation = nn.GELU()
        # map to classes
        self.mlp = nn.Sequential(
            nn.Linear(args.embed_dim*2, args.ffn_embed_dim),
            nn.Dropout(args.dropout),
            nn.GELU(),
            nn.Linear(args.ffn_embed_dim, 3),
        )
        # global graph
        self.register_buffer("x", graph.x)
        self.register_buffer("edge_index", graph.edge_index.T)
        self.register_buffer("edge_attr", graph.edge_attr)

    def forward(self, batch):
        """
        convolve whole graph, extract source/target
        """
        # unpack
        x_V_d = self.embedding(self.x)  # node features
        edge_index = self.edge_index
        edge_attr = self.edge_embedding(self.edge_attr)  # edge features
        # convolve
        x_resid = x_V_d
        for layer_idx, layer in enumerate(self.layers[:-1]):
            x_V_d = self.layer_norms[layer_idx](x_V_d)
            x_V_d = layer(x_V_d, edge_index, edge_attr)
            x_V_d = self.activation(self.dropout(x_V_d))
            x_V_d = x_resid + x_V_d  # residual for depth
            x_resid = x_V_d
        x_V_d = self.layer_norms[-1](x_V_d)
        x_V_d = self.layers[-1](x_V_d, edge_index)
        x_V_d = x_resid + x_V_d  # residual for depth
        # pool
        xP_B_d = x_V_d[batch["pert"]]
        xG_B_d = x_V_d[batch["gene"]]
        x_B_2d = torch.cat([xP_B_d, xG_B_d], dim=1)
        y_B = self.mlp(x_B_2d)
        return y_B

