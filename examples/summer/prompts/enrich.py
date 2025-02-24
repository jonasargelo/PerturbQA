# Prompt templates provided for gene set enrichment
# Usage: prompt.format(desc)
#   where desc is a concatenation of single-gene summaries

prompt = f"""[Start of Prompt]
You are an expert molecular biologist who studies how genes and pathways are related using Perturb-seq.

Task: You are writing a brief overview of a gene set observed to have a similar transcriptional response when upstream genes are perturbed.

Input: You will be provided descriptions of the constituent genes. Ensure that your overview remains faithful to this domain knowledge.

Output format: Fill in each of these three sections.
1) Brief overview of gene set: Write one to two sentences summarizing how the given genes are related. Focus on the most specific pathways that are common among these genes.
2) Upstream pathways may affect this gene set: Write one to two sentences describing what types of perturbations might impact the expression of the genes in this gene set. For example, you might consider pathways that are upstream of these genes or compensatory mechanisms.
3) Name of gene set: Summarize the gene set within ten words.

Constraints:
- Maintain a professional tone throughout.
- Do not comment on your own writing.
- Do not add any notes or references. Do not make up additional information.
- Do not discuss the importance or impact of the gene set. Focus only on its function.
[End of Prompt]

[Start of Input]{{desc}}
[End of Input]

[Start of Output]
1) Brief overview of gene set:
2) Upstream pathways may affect this gene set:
3) Name of gene set:
[End of Output]
"""

