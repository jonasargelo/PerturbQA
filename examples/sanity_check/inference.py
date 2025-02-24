import os
import sys
import random
from collections import defaultdict

import torch
import numpy as np
import pytorch_lightning as pl

from data import InferenceDataModule
from model import load_model
from parser import parse_args
from utils import printt, get_suffix, save_pickle


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def main():
    args = parse_args()
    set_seed(args.seed)

    torch.set_float32_matmul_precision("medium")

    data = InferenceDataModule(args)
    model = load_model(args, data)
    model.eval()

    # inference
    kwargs = {
        "accelerator": "gpu" if args.gpu >= 0 else "cpu"
    }
    if args.gpu >= 0:
        kwargs["devices"] = [args.gpu]
    tester = pl.Trainer(num_nodes=1,
                        enable_checkpointing=False,
                        logger=False,
                        **kwargs)
    printt("Initialized trainer.")

    best_path = args.checkpoint_path
    if os.path.exists(best_path):
        results_all = tester.predict(model, data,
                                     ckpt_path=best_path)
    else:
        raise Exception("NO checkpoint available")

    results_dict_all = []
    for results in results_all:
        results_dict = defaultdict(list)
        for batch in results:
            for k, v in batch.items():
                if type(v) is list:
                    results_dict[k].extend(v)
                else:
                    results_dict[k].append(v)
        results_dict_all.append(dict(results_dict))

    save_pickle(args.results_file, results_dict_all)
    printt("Done")



if __name__ == "__main__":
    main()

