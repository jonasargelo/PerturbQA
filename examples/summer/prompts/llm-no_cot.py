# Prompt templates for LLM (No CoT)
# Usage:
#   exampleA, exampleB   gene summaries
#   answer               pick from choices_de or choices_dir
#   cell_desc            pick from cell_lines
#
#   prompt_test_de.format(example1A=example1A,
#                         example1B=example1B,
#                         answer1=answer1,
#                         example2A=example2A,
#                         example2B=example2B,
#                         answer2=answer2,
#                         example3A=example3A,
#                         example3B=example3B,
#                         cell_desc=cell_desc)
#

desc_pert = "description of gene that is perturbed via CRISPRi knockdown"
desc_gene = "description of gene, the impact on which you wish to infer"


cell_lines = [
    "K562 cells are immortalised myelogenous leukemia cells of the erythroleukemia type.",
    "RPE1 cells are a non-cancerous, hTERT-immortalized, near-euploid, adherent, and p53-positive cell line.",
    "Jurkat cells are an immortalized line of human T lymphocyte cells.",
    "HepG2 cells are a human liver cancer cell line, derived from a patient with a well-differentiated hepatocellular carcinoma."
]


prompt_test_de = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

You are given as Input:
- Perturbed gene: {desc_pert}
- Gene of interest: {desc_gene}

Context: {{cell_desc}}

Question: If you knockdown the perturbed gene using CRISPRi, how does the gene of interest's expression change?

Answer: Your answer must end with one of these two choices and nothing else.
A) Knockdown of the perturbed gene does not impact the gene of interest.
B) Knockdown of the perturbed gene results in differential expression of the gene of interest.

Format: Follow the same format as Examples 1 and 2, and complete Example 3.

Example 1.

Input:
- Perturbed gene: {{example1A}}
- Gene of interest: {{example1B}}
Answer: {{answer1}}

Example 2.

Input:
- Perturbed gene: {{example2A}}
- Gene of interest: {{example2B}}
Answer: {{answer2}}

Example 3.

Input:
- Perturbed gene: {{example3A}}
- Gene of interest: {{example3B}}
Answer: """


prompt_test_dir = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

You are given as Input:
- Perturbed gene: {desc_pert}
- Gene of interest: {desc_gene}

Context: {{cell_desc}}

Question: When you knockdown the perturbed gene using CRISPRi, the gene of interest is differentially expressed. Is the gene of interest down-regulated or up-regulated?
Answer: Your answer must end with one of these two choices and nothing else.
A) Knockdown of the perturbed gene results in down-regulation of the gene of interest.
B) Knockdown of the perturbed gene results in up-regulation of the gene of interest.

Format: Follow the same format as Examples 1 and 2, and complete Example 3.

Example 1.

Input:
- Perturbed gene: {{example1A}}
- Gene of interest: {{example1B}}
Answer: {{answer1}}

Example 2.

Input:
- Perturbed gene: {{example2A}}
- Gene of interest: {{example2B}}
Answer: {{answer2}}

Example 3.

Input:
- Perturbed gene: {{example3A}}
- Gene of interest: {{example3B}}
Answer: """


choices_de = [
    "Knockdown of the perturbed gene does not impact the gene of interest.",
    "Knockdown of the perturbed gene results in differential expression of the gene of interest.",
]


choices_dir = [
    "A) Knockdown of the perturbed gene results in down-regulation of the gene of interest.",
    "B) Knockdown of the perturbed gene results in up-regulation of the gene of interest."
]

