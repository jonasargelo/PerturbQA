from datetime import datetime

import pickle
import numpy as np
import torch
import torch.nn as nn


def get_params_groups(model, args):
    regularized = []
    not_regularized = []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        # we do not regularize biases nor Norm parameters
        if name.endswith(".bias") or len(param.shape) == 1:
            not_regularized.append(param)
        else:
            regularized.append(param)
    groups = [{"params": regularized,
               "weight_decay": args.weight_decay,
               "lr": args.lr},
              {"params": not_regularized,
               "weight_decay": 0.,
               "lr": args.lr},
               ]
    return groups


def get_timestamp():
    return datetime.now().strftime('%H:%M:%S')


def printt(*args, **kwargs):
    print(get_timestamp(), *args, **kwargs)


def get_suffix(metric):
    suffix = "model_best_"
    suffix = suffix + "{global_step}_{epoch}_{"
    suffix = suffix + metric + ":.3f}_{val_loss:.3f}"
    return suffix

def save_pickle(fp, data):
    with open(fp, "wb+") as f:
        pickle.dump(data, f)

