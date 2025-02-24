import os
import sys
import random
from datetime import datetime
from collections import defaultdict

import torch
import numpy as np
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks import RichProgressBar
from pytorch_lightning.callbacks import ModelCheckpoint, LearningRateMonitor
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

from data import DataModule
from model import load_model
from parser import parse_args
from utils import printt, get_suffix


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def main():
    args = parse_args()
    set_seed(args.seed)

    torch.set_float32_matmul_precision("medium")

    data = DataModule(args)
    model = load_model(args, data)

# logger
    if args.debug:
        wandb_logger = None
    else:
        name = f"{args.model}-{args.embed_dim}x{args.num_layers}"
        name += f"-{args.ffn_embed_dim}-"
        #if "kg" in args.model and "path" not in args.model:
        #    name += f"k={args.num_neighbors}-"
        #if "path" in args.model:
        #    name += f"-{args.path_cache}-"
        name += datetime.now().strftime("%Y%m%d-%H:%M:%S")
        wandb_logger = WandbLogger(project=args.run_name,
                                   name=name)
        wandb_logger.watch(model)  # gradients
        args.save_path = os.path.join(args.save_path, name)

    # train loop
    mode = "max"
    for keyword in ["loss"]:
        if keyword in args.metric:
            mode = "min"

    checkpoint_kwargs = {
        "save_top_k": 1,
        "monitor": args.metric,
        "mode": mode,
        "filename": get_suffix(args.metric),
        "dirpath": args.save_path,
        "save_last": True,
    }
    # checkpoint_path is a PTH to resume training
    #if os.path.exists(args.checkpoint_path):
    #    checkpoint_kwargs["dirpath"] = args.checkpoint_path
    cb_checkpoint = ModelCheckpoint(**checkpoint_kwargs)

    cb_earlystop = EarlyStopping(
            monitor=args.metric,
            patience=args.patience,
            mode=mode,
    )
    callbacks=[
            RichProgressBar(),
            cb_checkpoint,
            cb_earlystop,
    ]
    if args.no_tqdm:
        callbacks[0].disable()

    device_ids = [args.gpu + i for i in range(args.num_gpu)]

    trainer_kwargs = {
        "max_epochs": args.epochs,
        "min_epochs": args.min_epochs,
        "accumulate_grad_batches": args.accumulate_batches,
        "gradient_clip_val": 1.,
        # evaluate more frequently
        #"limit_train_batches": 500,
        #"limit_val_batches": 50,
        # logging and saving
        "callbacks": callbacks,
        "log_every_n_steps": args.log_frequency,
        "fast_dev_run": args.debug,
        "logger": wandb_logger,
        # GPU utilization
        #"devices": device_ids,
        "accelerator": "gpu" if args.num_gpu > 0 else "cpu",
        #"strategy": "ddp"
        #"precision": 16,
    }

    trainer = pl.Trainer(**trainer_kwargs)
    printt("Initialized trainer.")

    # data loaders
    data = DataModule(args)
    printt("Finished loading raw data.")

    # if applicable, restore full training
    fit_kwargs = {}
    if os.path.exists(args.checkpoint_path):
        fit_kwargs["ckpt_path"] = args.checkpoint_path
    trainer.fit(model, data, **fit_kwargs)

    if not args.debug:
        best_path = cb_checkpoint.best_model_path
        printt(best_path)

    printt("Done")



if __name__ == "__main__":
    main()

