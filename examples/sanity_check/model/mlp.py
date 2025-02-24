"""
MLP encoder
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MLP(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.embedding = nn.Embedding(args.vocab_size, args.embed_dim)
        # make layers + norms
        layers = [
            nn.Linear(args.embed_dim*2, args.ffn_embed_dim)
        ]
        for _ in range(args.num_layers):
            layers.append(
                nn.Linear(args.ffn_embed_dim, args.ffn_embed_dim)
            )
        layers.append(
            nn.Linear(args.ffn_embed_dim, 3)
        )
        self.layers = nn.ModuleList(layers)
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(args.ffn_embed_dim)
            for _ in range(args.num_layers + 1)
        ])
        # non-learned
        self.dropout = nn.Dropout(args.dropout)
        self.activation = nn.GELU()

    def forward(self, batch):
        x_pert = self.embedding(batch["pert"])
        x_gene = self.embedding(batch["gene"])
        x_B_2d = torch.cat([x_pert, x_gene], dim=1)
        x_B_d = self.layers[0](x_B_2d)
        x_resid = x_B_d
        for layer_idx, layer in enumerate(self.layers[1:-1]):
            x_B_d = self.layer_norms[layer_idx](x_B_d)
            x_B_d = layer(x_B_d)
            x_B_d = self.activation(self.dropout(x_B_d))
            x_B_d = x_resid + x_B_d  # residual for depth
            x_resid = x_B_d
        x_B_d = self.layer_norms[-1](x_B_d)
        x_B = self.layers[-1](x_B_d).squeeze(1)
        return x_B

