"""
This file contains functions to parse the outputs of SUMMER
and other LLM baselines.

The corresponding outputs can be found on our data distribution.
"""


def load_outputs_summer(fp, keys):
    preds = load_outputs(fp, keys,
                         copies=[1, 1, 1],
                         adjacent_copies=True,
                         reduce=False)
    return preds


def load_outputs_no_retrieve(fp, keys):
    preds = load_outputs_old(fp, keys,
                             copies=[1, 1, 1, 1],
                             reduce=False,
                             adjacent_copies=False)
    return preds


def load_outputs_no_cot(fp, keys):
    preds = load_outputs_old(fp, keys,
                             copies=[1, 1, 1],
                             reduce=False,
                             adjacent_copies=False)
    return preds


labels_0 = [
    "Knockdown of {} does not impact {}",
    "Knockdown of {} is unlikely to result in differential expression of {}",
    "Knockdown of {} is not likely to result in differential expression of {}",
    "Knockdown of {} results in a decrease in expression of {}",
    "unlikely that a CRISPRi knockdown of {}",
    "knockdown of {} is not likely to",
    "unlikely that knocking down {}",
    "it is unlikely that a CRISPRi knockdown of {} will result in differential expression of {}",
    "{} does not result in differential expression of {}",
    "a CRISPRi knockdown of {} is unlikely to",
    "Answer: No", "answer: No", "answer: no", "Answer: no",
    "Answer: Decrease", "answer: Decrease", "answer: decrease", "Answer: decrease",
    "Decrease.", "No.", "No",
    "**Decrease**", "**decrease**"
]

labels_1 = [
    "Knockdown of {} results in differential expression of {}",
    "nockdown of {} is likely to result in differential expression of {}",
    "Knockdown of {} results in an increase in expression of {}",
    "of {} does result in differential expression of {}",
    "{} is likely to result in differential expression of {}",
    "{} may result in differential expression of {}",
    "Answer: Yes", "answer: Yes", "answer: yes", "Answer: yes",
    "Answer: Increase", "answer: Increase", "answer: increase", "Answer: increase",
    "**Increase**", "**increase**",
    "is likely that a CRISPRi knockdown of {} will result in differential expression of {}",
    "is likely that a CRISPRi knockdown of {} would result in an increase in expression of {}",
    "may result in an increase in the expression of",
    "Increase.", "Yes.", "Yes",
    "is likely that a CRISPRi knockdown of {} will result in an increase in the expression of {}",
    "is possible that a CRISPRi knockdown of {} may result in an increase in expression of {}",
]


def load_outputs(fp, keys, copies=[1], reduce=True,
                 adjacent_copies=False):
    with open(fp) as f:
        lines = json.load(f)[:len(keys) * len(copies)]
    assert len(lines) % len(copies) == 0, (fp, len(lines), len(copies))
    assert len(keys) * len(copies) == len(lines)
    num_unique = len(lines) // len(copies)
    preds = [[] for _ in range(num_unique)]
    # look through each copy
    for i, to_keep in enumerate(copies):
        if not to_keep:
            continue
        if not adjacent_copies:
            start = num_unique * i
            end = start + num_unique
            iterator = enumerate(lines[start:end])
        else:
            iterator = enumerate([lines[j*len(copies)+i] for j in range(num_unique)])
        for j, line in iterator:
            if "Note" in line.strip().split("\n")[-1]:
                line = line.strip().rsplit("\n")[:-1]
                line = "\n".join(line)
            line = line.split("[End of Output]")[0]
            line = line.split("Output:")[0]
            line = line.replace("in K562 cells ", "")
            found_0, found_1 = False, False
            for cur_0 in labels_0:
                if cur_0.format(*keys[j]) in line:
                    found_0 = True
            for cur_1 in labels_1:
                if cur_1.format(*keys[j]) in line:
                    found_1 = True
            if found_0 and not found_1:
                preds[j].append(0)
            elif found_1 and not found_0:
                preds[j].append(1)
            else:
                preds[j].append(-1)
    if reduce:
        preds_new = []
        for pred in preds:
            if max(pred) < 0:
                preds_new.append(-1)
            else:
                pred = [p for p in pred if p >= 0]
                preds_new.append(np.mean(pred))
        preds = preds_new
    return preds


labels_0_old = [
    "does not impact",
    "down-regulation of"
]

labels_1_old = [
    "in differential expression of",
    "up-regulation of",
]


def load_outputs_old(fp, keys, copies=[1], reduce=True,
                     adjacent_copies=False):
    with open(fp) as f:
        lines = json.load(f)[:len(keys) * len(copies)]
    assert len(lines) % len(copies) == 0, (fp, len(lines), len(copies))
    assert len(keys) * len(copies) == len(lines)
    num_unique = len(lines) // len(copies)
    preds = [[] for _ in range(num_unique)]
    # look through each copy
    for i, to_keep in enumerate(copies):
        if not to_keep:
            continue
        if not adjacent_copies:
            start = num_unique * i
            end = start + num_unique
            iterator = enumerate(lines[start:end])
        else:
            iterator = enumerate([lines[j*len(copies)+i] for j in range(num_unique)])
        for j, line in iterator:
            if "4) Answer:" in line:
                line = line.split("4) Answer:", 1)[1]
            line = line.replace("in K562 cells ", "")
            found_0, found_1 = False, False
            for cur_0 in labels_0_old:
                if cur_0 in line:
                    found_0 = True
            for cur_1 in labels_1_old:
                if cur_1 in line:
                    found_1 = True
            if found_0 and not found_1:
                preds[j].append(0)
            elif found_1 and not found_0:
                preds[j].append(1)
            else:
                preds[j].append(-1)
    if reduce:
        preds_new = []
        for pred in preds:
            if max(pred) < 0:
                preds_new.append(-1)
            else:
                pred = [p for p in pred if p >= 0]
                preds_new.append(np.mean(pred))
        preds = preds_new
    return preds

