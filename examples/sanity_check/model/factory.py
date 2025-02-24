"""
LightningModule file
"""

import os
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW

import pytorch_lightning as pl
from torchmetrics.classification import BinaryAUROC, BinaryAveragePrecision
from torchmetrics.classification import BinaryAccuracy

from utils import get_params_groups
from .mlp import MLP
from .mlp_pathway import PathwayMLP
from .gnn import GAT
from .gnn_pathway import PathwayGAT


def load_model(args, data_module):
    return Module(args, data_module)


class Module(pl.LightningModule):
    def __init__(self, args, data_module):
        super().__init__()

        self.args = args
        # Transformer on sequence of predicted graphs
        if args.model == "mlp":
            self.encoder = MLP(args)
        elif args.model == "mlp_pathway":
            self.encoder = PathwayMLP(args, *data_module.params)
        elif args.model == "kg_gnn":
            self.encoder = GAT(args, data_module.graph)
        elif args.model == "kg_gnn_pathway":
            self.encoder = PathwayGAT(args, data_module.graph,
                                            *data_module.params)
        else:
            raise Exception(f"Invalid model: '{args.model}'")

        # validation meters
        self.auroc = BinaryAUROC()
        self.auprc = BinaryAveragePrecision()
        self.acc = BinaryAccuracy()

        self.save_hyperparameters()

    def forward(self, batch):
        """
        Used on predict_dataloader
        """
        output = self.encoder(batch)
        pred_list = output.cpu().numpy().tolist()
        true_list = batch["label"].cpu().numpy().tolist()
        results = {
            "key": batch["key"],
            "pred": pred_list,
            "true": true_list
        }
        return results

    def compute_losses(self, output, batch):
        losses = {}
        losses["loss"] = F.cross_entropy(output,
                                         batch["label"])
        return losses

    def compute_metrics(self, output, batch):
        """
        Differential expression (de) and direction (dir) treated
        separately
        """
        losses = self.compute_losses(output, batch)
        metrics = {
            "key": batch["key"],
            "loss": losses["loss"]
        }

        # differential expression metrics (binary)
        de_pred = 1 - output[:,0]
        de_mask = batch["label"] > 0
        de_true = de_mask.long()
        metrics["de_acc"] = self.acc(de_pred, de_true)
        if de_true.sum() > 0:
            metrics["de_auroc"] = self.auroc(de_pred, de_true)
            metrics["de_auprc"] = self.auprc(de_pred, de_true)

            # direction metrics (binary)
            dir_pred = output[de_mask][:,2]
            dir_true = (batch["label"][de_mask] > 1).long()
            metrics["dir_acc"] = self.acc(dir_pred, dir_true)
            if dir_true.sum() > 0:
                metrics["dir_auroc"] = self.auroc(dir_pred, dir_true)
                metrics["dir_auprc"] = self.auprc(dir_pred, dir_true)

        # convert to floats
        for k, v in metrics.items():
            if k != "key":
                metrics[k] = v.item()

        return metrics

    def training_step(self, batch, batch_idx):
        # cuda oom
        try:
            output = self.encoder(batch)
            losses = self.compute_losses(output, batch)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            return
        for k, v in losses.items():
            if not torch.is_tensor(v) or v.numel() == 1:
                self.log(f"Train/{k}", v.item(),
                    batch_size=len(output), sync_dist=True)
        return losses["loss"]

    def validation_step(self, batch, batch_idx):
        # cuda oom
        try:
            output = self.encoder(batch)
            results = self.compute_metrics(output, batch)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            return
        # logging
        for k, v in results.items():
            if type(v) is float:  # loss
                self.log(f"Val/{k}", v,
                    batch_size=len(output), sync_dist=True)
            elif torch.is_tensor(v):  # loss
                self.log(f"Val/{k}", v.item(),
                    batch_size=len(output), sync_dist=True)

    def configure_optimizers(self):
        param_groups = get_params_groups(self, self.args)
        optimizer = AdamW(param_groups)
        return [optimizer]

