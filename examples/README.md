# Examples

This directory contains various examples, as well as the baselines for our various tasks.

## Knowledge graphs to prompts

`kg_to_prompt.ipynb` shows how to convert our processed knowledge
graphs into text (e.g. for LLM summarization).
Note that this requires the knowledge graphs `kg.zip`, from our [data distribution](https://zenodo.org/records/13760748?token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImQ2NTU1MTZjLTQ1OTktNGFlZi1hNWE2LTk5ZDRhNzIwMGZjZSIsImRhdGEiOnt9LCJyYW5kb20iOiI4ZmQzNDZlNmZhZGQ1MTAzN2YyM2ZlYjU4ZWNjMGZmNCJ9.Ym9Ws841nq4_KDAFxXg4f7FC55jBCCedCEAyh5q44j3D5834pxUIU2mhZwYytQ2NJfb4kSe9re9gTqXJ68F_PA).
Place the unzipped folder at `perturbqa/datasets/kg`.

Licenses of individual files are noted in the main `README`. Please note that CORUM is licensed under [CC BY NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en).

Our gene LLM-generated summaries can be found under `gene_summary.zip`, with an example notebook at `gene_summary.ipynb`.

## Results

`results.ipynb` contains examples of scoring predictions and generating Table 1.
Place the unzipped `results.zip` at `results` (root level, same as `perturbqa`).

`kg_analysis.ipynb` contains analysis of knowledge graph connectivity, i.e. Figure 2D and Table 1 "Physical" baseline.

## Baselines

### Differential expression and direction of change

- `sanity_check` contains the MLP and GAT baselines.
- GEARS was run with the [authors' original
  codebase](https://github.com/snap-stanford/GEARS/tree/master/gears)
  without pre-filtering for highly variables genes, for comparability.
- GenePT was run with the [published
  embeddings](https://github.com/yiqunchen/GenePT)
  using `LogisticRegression` from `scikit-learn` on default settings (as
  published).

### Gene set enrichment
- `gene_set.ipynb` contains the gene set over-representation analysis
code. This requires package `gseapy`.

