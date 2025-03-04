# Contextualizing biological perturbation experiments through language

This is the official repository for PerturbQA.
If you find our work interesting, please check out our
[paper](https://arxiv.org/abs/2502.21290)
to learn more!

```
@inproceedings{
    wu2025perturbqa,
    title={Contextualizing biological perturbation experiments through language},
    author={Menghua Wu and Russell Littman and Jacob Levine and Lin Qiu and Tommaso Biancalani and David Richmond and Jan-Christian Huetter},
    booktitle={The Thirteenth International Conference on Learning Representations},
    year={2025},
}
```

## Installation

```
git clone git@github.com:Genentech/PerturbQA.git
cd PerturbQA
pip install -e .
```

Specifically, the following packages are required to run our evaluation.

```
- scikit-learn
- numpy
- (optional, for ROUGE and BERT scores) torchmetrics, which requires torch
- (optional, for BERT score) transformers
```

This code distribution contains the PerturbQA input and label pairs.
For additional materials, including processed knowledge graphs and model
predictions, please see the
[data distribution](https://doi.org/10.5281/zenodo.14915312).

## PerturbQA benchmark

### Differential expression and direction of change

Datasets can be loaded as follows.

```python
from pertqa import load_de, load_dir

# options: "k562" "rpe1" "hepg2" "jurkat" "k562_set"
data_de = load_de("k562")
# train/test splits
X_train = data_de["train"]
X_test = data_de["test"]

data_dir = load_dir("k562")
```

To evaluate your predictions (additional example in `examples/results.ipynb`):

```
import numpy as np
from pertqa import auc_per_gene

keys = [(x["pert"], x["gene"]) for x in X_test]
pred = np.random.randn(len(keys))  # list / numpy array of floats
true = [x["label"] for x in X_test]  # from load_de/dir
auc = auc_per_gene(keys, pred, true)
```

### Gene set enrichment

Set flag `skip_empty` to skip entries without manual annotation
(defaults to `True`).

```python
from pertqa import load_gse

# options: "pert" "gene"
data = load_gse("pert", skip_empty=True)
```

To evaluate your predictions (requires `torchmetrics`):

```python
from pertqa import rouge1_recall

pred = ["hello world"]  # list of predictions
true = ["hello"]  # list of labels, e.g. from load_gse
score = rouge1_recall(pred, true)
```

The `transformers` library is required to compute BERTScore,
and we recommend having access to a GPU.

```python
from pertqa import bert_score

pred = ["hello world"]  # list of predictions
true = ["hello"]  # list of labels, e.g. from load_gse
scores = bert_score(pred, true)
```

### Knowledge graph to prompts

Processed knowledge graphs are available in the [data
distribution](https://doi.org/10.5281/zenodo.14915312)
under the archive `kg.zip`.

See `examples/kg_to_prompt.ipynb` for details about how to load these files
and how to generate gene summary prompts.
Please place `kg` at `perturbqa/datasets/kg` if you wish to run these examples.

## Models

### LLMs

Please see `examples/summer` for more details.

- All prompt templates may be found at `examples/summer/prompts`.
- Raw LLM outputs can be found in the [data
  distribution](https://doi.org/10.5281/zenodo.14915312), in the archives named:
  - `summer_outputs.zip`
  - `llm-nocot.zip`
  - `llm-noretrieve.zip`

### Baselines

- Code or instructions required to run baselines can be found under `examples`
- Baselines have their own installation requirements.

## Data attribution and license

This codebase is licensed under the Genentech Non-Commercial Software License Version 1.0.
For more information, please see the attached LICENSE.txt file.

The PerturbQA datasets in the data folder of this repository are licensed under the CC BY 4.0 license.
They are derived from the following datasets:

|Datasets|Reference|License|
|--|--|--|
|DE/Dir: k562, k562_set, rpe1. Gene set enrichment|**Mapping information-rich genotype-phenotype landscapes with genome-scale perturb-seq** Cell, 185(14):2559–2575.e28, 2022. ISSN 0092-8674. doi:505 [(link)](https://www.cell.com/cell/pdf/S0092-8674(22)00597-9.pdf)|[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)|
|DE/Dir: hepg2, jurkat|**Transcriptome-wide characterization of genetic perturbations.** bioRxiv, 07 2024. doi: 10.1101/2024.07.03.601903 [(link)](https://www.biorxiv.org/content/10.1101/2024.07.03.601903v1)| [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The LLM outputs in the data distribution (`summer_outputs.zip`, `summer_enrichment.zip`, `llm-nocot.zip`, `llm-noretrieve.zip`) and results tables (`results.zip`) are licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

The knowledge graph entries and gene summaries (`kg.zip`, `gene_summary.zip` of the data distribution, respectively) are derived from the following datasets and are governed by the original licenses of these datasets:

|Database|Reference|License|
|--|--|--|
|[UniProt](https://www.uniprot.org/)|UniProt: the Universal Protein Knowledgebase in 2023 Nucleic Acids Res. 51:D523–D531 (2023) [(link)](https://academic.oup.com/nar/article/51/D1/D523/6835362?login=true)|[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)|
|[Ensembl](https://ensembl.org)|Ensembl 2024 Nucleic Acids Res. 2024, 52(D1):D891–D899 PMID: 37953337 10.1093/nar/gkad1049 [(link)](https://academic.oup.com/nar/article/52/D1/D891/7416379?login=true)|[Apache 2.0](https://www.ensembl.org/info/about/legal/code_licence.html)|
|[Gene Ontology](https://geneontology.org/)|[2024-01-17](http://release.geneontology.org/2024-01-17) release ([DOI:10.5281/zenodo.10536401](https://doi.org/10.5281/zenodo.10536401))|[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)|
|[CORUM](https://mips.helmholtz-muenchen.de/corum/)|CORUM: the comprehensive resource of mammalian protein complexes–2022  Nucleic Acids Research, 51(D1):D539–D545 [(link)](https://academic.oup.com/nar/article/51/D1/D539/6830667)|[CC BY NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en)|
|[STRINGDB](https://string-db.org/)|Szklarczyk et al. Nucleic acids research 51.D1 (2023): D638-D646 [(link)](https://pubmed.ncbi.nlm.nih.gov/36370105/)|[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)|
|[Reactome](https://reactome.org/)|The Reactome Pathway Knowledgebase 2024. Nucleic Acids Research. 2024. doi: 10.1093/nar/gkad1025. [(link)](https://academic.oup.com/nar/article/52/D1/D672/7369850?login=true&utm_source=advanceaccess&utm_campaign=nar&utm_medium=email)|[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)|
|[Bioplex](https://bioplex.hms.harvard.edu/)|Huttlin et al. (2021) Cell 184(11):3022-3040. doi: 10.1016/j.cell.2021.04.011. [(link)](https://doi.org/10.1101/2020.01.19.905109)

Please note that CORUM is licensed under [CC BY NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.en)
