# Prompt templates for SUMMER final QA
# Usage:
#   pert, gene           gene names
#   pert_desc, gene_desc gene summaries
#   cell_short           from cell_lines
#   cell_desc            from cell_lines
#   obs                  list of examples, each formatted as
#                        - pert_desc
#                        - gene_desc
#                        - answer (from choices_de, choices_dir)
#
# prompt_test_dir.format(pert=pert, gene=gene,
#                        pert_desc=pert_str, gene_desc=gene_str,
#                        cell_short=cell_name,
#                        cell_desc=cell_desc,
#                        obs=observations)
#


desc_pert = "description of gene that is perturbed via CRISPRi knockdown"
desc_gene = "description of gene, the impact on which you wish to infer"
desc_context = "description of cell line in which the genes are expressed"
desc_obs = "set of experimental observations that describe the impact of CRISPRi perturbations on related genes, to contextualize your answer"


cell_lines = [
    ("K562 cells", "K562 cells are immortalised myelogenous leukemia cells of the erythroleukemia type."),
    ("K562 cells", "K562 cells are immortalised myelogenous leukemia cells of the erythroleukemia type."),
    ("RPE1 cells", "RPE1 cells are a non-cancerous, hTERT-immortalized, near-euploid, adherent, and p53-positive cell line."),
    ("Jurkat cells", "Jurkat cells are an immortalized line of human T lymphocyte cells."),
    ("HepG2 cells", "HepG2 cells are a human liver cancer cell line, derived from a patient with a well-differentiated hepatocellular carcinoma.")
]


choices_de = [
    "A) Knockdown of the perturbed gene does not impact the gene of interest.",
    "B) Knockdown of the perturbed gene results in differential expression of the gene of interest.",
]

choices_dir = [
    "A) Knockdown of the perturbed gene results in a decrease in expression of the gene of interest.",
    "B) Knockdown of the perturbed gene results in an increase in expression of the gene of interest."
]


prompt_test_de = f"""[Start of Prompt]
You are an expert molecular biologist who studies how genes are related using Perturb-seq. Your goal is to determine: Does a CRISPRi knockdown of {{pert}} in {{cell_short}} result in differential expression of {{gene}}?

You are given as input:
- Description of perturbed gene ({{pert}}): {desc_pert}
- Description of gene of interest ({{gene}}): {desc_gene}
- Context: {desc_context}
- Examples: {desc_obs}

Output: Please extract the most relevant parts of the examples that address these five questions. Be specific.

1) Which of the observed perturbed genes are most similar to {{pert}} (if any, including {{pert}} itself)?
2) When perturbing {{pert}} or similar genes, what downstream pathways or genes are differentially expressed? Justify your answer with the observed outcomes.
3) Which of the observed genes of interest are most similar to {{gene}} (if any, including {{gene}} itself)?
4) What perturbations of upstream pathways or genes result in differential expression of {{gene}} or similar genes (if any)? Justify your answer with the observed outcomes.
5) Is a CRISPRi knockdown of {{pert}} in {{cell_short}} likely to result in differential expression of {{gene}}? For example, if 2) and 4) are unrelated or only indirectly related, it is unlikely we will observe differential expression. On the other hand, if 2) and 4) significantly overlap in specific genes or pathways, we may observe differential expression. Your final answer should end with one of these three options and nothing else.
- No. Knockdown of {{pert}} does not impact {{gene}}.
- Yes. Knockdown of {{pert}} results in differential expression of {{gene}}.
- There is insufficient evidence to determine how knockdown of {{pert}} affects {{gene}}.
[End of Prompt]

[Start of Input]
- Description of perturbed gene ({{pert}}): {{pert_desc}}
- Description of gene of interest ({{gene}}): {{gene_desc}}
- Context: {{cell_desc}}
- Examples: {{obs}}
[End of Input]

[Start of Output]
1)
2)
3)
4)
5)
[End of Output]"""


prompt_test_dir = f"""[Start of Prompt]
You are an expert molecular biologist who studies how genes are related using Perturb-seq. Your goal is to determine: Does a CRISPRi knockdown of {{pert}} in {{cell_short}} result in a decrease or increase in expression of {{gene}}?

You are given as input:
- Description of perturbed gene ({{pert}}): {desc_pert}
- Description of gene of interest ({{gene}}): {desc_gene}
- Context: {desc_context}
- Examples: {desc_obs}

Output: Please extract the most relevant parts of the examples that address these seven questions. Be specific and address each part.

1) Which of the observed perturbed genes are most similar to {{pert}} (if any, including {{pert}} itself)?
2) When {{pert}} or similar genes are knocked down: summarize the genes whose expression decreases (if any), and the specific pathways they are involved in.
3) When {{pert}} or similar genes are knocked down: summarize the genes whose expression increases (if any), and the specific pathways they are involved in.

4) Which of the observed genes of interest are most similar to {{gene}} (if any, including {{gene}} itself)?
5) Summarize the genes and specific pathways whose knockdown causes expression of {{gene}} or similar genes to decrease (if any).
6) Summarize the genes and specific pathways whose knockdown causes expression of {{gene}} or similar genes to increase (if any).

7) Does a CRISPRi knockdown of {{pert}} in {{cell_short}} likely to result in decrease or increase of {{gene}}? For example, if the genes or pathways in 2) and 5) significantly overlap, we may observe a decrease. On the contrary, if genes or pathways in 3) and 6) significantly overlap, we may observe an increase.

Your final answer should end with one of these three options and nothing else.
- Decrease. Knockdown of {{pert}} results in a decrease in expression of {{gene}}.
- Increase. Knockdown of {{pert}} results in an increase in expression of {{gene}}.
- There is insufficient evidence to determine how knockdown of {{pert}} affects {{gene}}.
[End of Prompt]

[Start of Input]
- Description of perturbed gene ({{pert}}): {{pert_desc}}
- Description of gene of interest ({{gene}}): {{gene_desc}}
- Context: {{cell_desc}}
- Examples: {{obs}}
[End of Input]

[Start of Output]
1)
2)
3)
4)
5)
[End of Output]"""

