import sys
from collections import defaultdict

import numpy as np

from sklearn.metrics import roc_auc_score

try:
    from torchmetrics.text.rouge import ROUGEScore
    from torchmetrics.text.bert import BERTScore
except ImportError as e:
    # error will be thrown if function is called
    pass


def get_group_to_idx(vals):
    group_to_idx = defaultdict(list)
    for i, v in enumerate(vals):
        group_to_idx[v].append(i)
    return dict(group_to_idx)


def auc_per_gene(keys, pred, true, reduce=True):
    """
    AUC computed per gene

    @param (list) keys  [(pert, gene), ...]
    @param (list, np.ndarray) pred
    @param (list, np.ndarray) true
    """
    # sanitize
    if not isinstance(pred, np.ndarray):
        pred = np.array(pred)
    if not isinstance(true, np.ndarray):
        true = np.array(true)
    # group
    genes = [k[1] for k in keys]
    groups = get_group_to_idx(genes)
    metrics = []
    for group, idx in groups.items():
        ts = true[idx]
        ps = pred[idx]
        # skip all 0s or 1s (shouldn't be in the input)
        if sum(ts) == 0 or sum(ts) == len(ts):
            continue
        metrics.append(roc_auc_score(ts, ps))
    if reduce:
        metrics = np.mean(metrics).item()
    return metrics


def rouge1_recall(pred, true, reduce=True):
    """
    @param pred  str, or list of str
    @param true  str, or list of str
    """
    if "ROUGEScore" not in sys.modules:
        raise Exception("Please install `torchmetrics`")

    scorer = ROUGEScore()
    scores = []
    # check type and sanitize
    if type(pred) is str:
        pred = [pred]
    if type(true) is str:
        true = [true]
    assert len(pred) == len(true)
    # compute scores
    for p, t in zip(pred, true):
        scores.append(scorer(p, t)["rouge1_recall"])
    # optional mean
    if reduce:
        scores = np.mean(scores).item()
    return scores


def bert_score(pred, true, reduce=True, **kwargs):
    """
    Requires transformers. Recommend GPU.

    @param pred  str, or list of str
    @param true  str, or list of str

    @param **kwargs  passed directly to BERTScore
    """
    if "BERTScore" not in sys.modules:
        raise Exception("Please install `torchmetrics` and `transformers`")

    scorer = BERTScore(
        model_name_or_path="dmis-lab/biobert-base-cased-v1.2",
        **kwargs
    )
    scores = []
    # check type and sanitize
    if type(pred) is str:
        pred = [pred]
    if type(true) is str:
        true = [true]
    assert len(pred) == len(true)
    # compute scores
    try:
        scores = {k: v.numpy() for k, v in scorer(pred, true).items()}
    except:
        print("One of your inputs is too long.")
        return
    # optional mean
    if reduce:
        scores = {k: np.mean(v).item() for k, v in scores.items()}
    return scores

