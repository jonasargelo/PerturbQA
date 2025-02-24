# Prompt templates for LLM (No Retrieve)
# Usage:
#   exampleA, exampleB   gene summaries
#   hypothesis           pick from choices_de or choices_dir
#   cell_desc            pick from cell_lines
#
#   prompt_test_de.format(exampleA=exampleA,
#                         exampleB=exampleB,
#                         hypothesis=hypothesis,
#                         cell_desc=cell_desc)
#

desc_pert = "description of gene that is perturbed via CRISPRi knockdown"
desc_gene = "description of gene, the impact on which you wish to infer"
desc_hypothesis = "hypothesis regarding how the specified perturbation affects the gene of interest"


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
- Hypothesis: {desc_hypothesis}

Context: {{cell_desc}}

Question: If you knockdown the perturbed gene using CRISPRi, how does the gene of interest's expression change?

Task: Your goal is to identify evidence in the input that supports or refutes the hypothesis, and explain whether the hypothesis is likely to be true.

Output format: Please fill in the following four sections. Preserve the formatting and add the corresponding content.

1) Supporting evidence: Identify all relevant parts of the input that support the hypothesis.
2) Refuting evidence: Identify all relevant parts of the input that refute the hypothesis.
3) Explanation: Based on the evidence, explain how to answer the question, step by step. In particular,
- if there is a causal relationship from the perturbed gene to the gene of interest, explain how biological mechanisms relate the perturbed gene to the gene of interest.
- if there is no causal relationship from the perturbed gene to the gene of interest, explain why. For example, the perturbed gene may be downstream of the gene of interest, or there may be no relationship between the two genes.
- if there is insufficient evidence to answer the question, say so.
4) Answer: Your answer must end with one of these three choices and nothing else.
A) Knockdown of the perturbed gene does not impact the gene of interest.
B) Knockdown of the perturbed gene results in differential expression of the gene of interest.
C) There is insufficient evidence to determine how knockdown of the perturbed gene affects the gene of interest.

Input:
- Perturbed gene: {{exampleA}}
- Gene of interest: {{exampleB}}
- Hypothesis: {{hypothesis}}

Output:
1) Supporting evidence:
2) Refuting evidence:
3) Explanation:
4) Answer:
"""


prompt_test_dir = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

You are given as Input:
- Perturbed gene: {desc_pert}
- Gene of interest: {desc_gene}
- Hypothesis: {desc_hypothesis}

Context: {{cell_desc}}

Question: When you knockdown the perturbed gene using CRISPRi, the gene of interest is differentially expressed. Is the gene of interest down-regulated or up-regulated?

Task: Your goal is to identify evidence in the input that supports or refutes the hypothesis, and explain whether the hypothesis is likely to be true.

Output format: Please fill in the following four sections. Preserve the formatting and add the corresponding content.

1) Supporting evidence: Identify all relevant parts of the input that support the hypothesis.
2) Refuting evidence: Identify all relevant parts of the input that refute the hypothesis.
3) Explanation: Based on the evidence, explain how to answer the question, step by step. In particular,
- if there is a causal relationship from the perturbed gene to the gene of interest, explain how biological mechanisms relate the perturbed gene to the gene of interest, with a focus on direction of change.
- if there is no causal relationship from the perturbed gene to the gene of interest, explain why. For example, the direction of change may contradict one of the known relationships.
- if there is insufficient evidence to answer the question, say so.
4) Answer: Your answer must end with one of these three choices and nothing else.
A) Knockdown of the perturbed gene results in down-regulation of the gene of interest.
B) Knockdown of the perturbed gene results in up-regulation of the gene of interest.
C) There is insufficient evidence to determine how knockdown of the perturbed gene affects the gene of interest.

Input:
- Perturbed gene: {{exampleA}}
- Gene of interest: {{exampleB}}
- Hypothesis: {{hypothesis}}

Output:
1) Supporting evidence:
2) Refuting evidence:
3) Explanation:
4) Answer:
"""


choices_de = [
    "Knockdown of the perturbed gene does not impact the gene of interest.",
    "Knockdown of the perturbed gene results in differential expression of the gene of interest.",
]


choices_dir = [
    "A) Knockdown of the perturbed gene results in down-regulation of the gene of interest.",
    "B) Knockdown of the perturbed gene results in up-regulation of the gene of interest."
]

