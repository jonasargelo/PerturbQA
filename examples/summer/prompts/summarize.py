# Prompt templates provided for reference
# Usage:
#   prompt_pert.format(gene="ABCE1", entries="- enables something")
#   prompt_gene.format(gene="ABCE1", entries="- enables something")
#   prompt_pert_1hop.format(gene="ABCE1", entries="- enables something", summary="ABCE1 is a gene")
#   prompt_gene_1hop.format(gene="ABCE1", entries="- enables something", summary="ABCE1 is a gene")

prompt_pert = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Task: You are writing a brief overview of the human gene {{name}}, with a focus on its molecular and cellular functions. You will be provided a set of database entries about the gene. Ensure that your overview remains faithful to this domain knowledge.

Format:
- Write one to two sentences describing the primary molecular and cellular function of gene {{name}}.
- Write one sentence describing the potential downstream impact of perturbing gene {{name}} via gene knockdown.

Constraints:
- Maintain a professional tone throughout.
- Do not comment on your own writing.
- Do not add any notes or references. Do not make up additional information.
- Do not discuss the importance or impact of the gene. Focus only on its function.

Domain knowledge:
{{entries}}

Brief overview of gene {{name}}:
"""

prompt_gene = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Task: You are writing a brief overview of the human gene {{name}}, with a focus on its molecular and cellular functions. You will be provided a set of database entries about the gene. Ensure that your overview remains faithful to this domain knowledge.

Format:
- Write one to two sentences describing the primary molecular and cellular function of gene {{name}}.
- Write one sentence describing what types of perturbations might impact the expression of gene {{name}}. For example, you might consider pathways that are upstream of the gene or compensatory mechanisms.

Constraints:
- Maintain a professional tone throughout.
- Do not comment on your own writing.
- Do not add any notes or references. Do not make up additional information.
- Do not discuss the importance or impact of the gene. Focus only on its function.

Domain knowledge:
{{entries}}

Brief overview of gene {{name}}:
"""

prompt_pert_1hop = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Task: You are writing a brief overview of the human gene {{name}}, with a focus on the downstream effects of perturbing {{name}} via gene knockdown (loss of function).

Inputs: You are provided
- Description of perturbed gene {{name}}
- Database entries relating {{name}} to other genes or pathways

Format:
- Write up to five sentences describing the molecular and cellular impact of perturbing gene {{name}} via gene knockdown.

Constraints:
- Remain faithful to all domain knowledge. Do not make up additional information.
- Summarize all common aspects succintly, but point out notable differences within these sets of genes.
- Maintain a professional tone throughout. Do not comment on your own writing. Do not add any notes or references.
- Omit the importance or impact of the gene. Focus only on its function.
- Omit all non-specific information and obvious statements, e.g. "this gene is involved in cellular processes."

Description of gene {{name}}: {{summary}}

Relations to other genes:
{{entries}}

Downstream effects of perturbing {{name}} via gene knockdown:
"""

prompt_gene_1hop = f"""You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Task: You are writing a brief overview of the human gene {{name}}, with a focus on molecular and cellular perturbations that may affect the levels of gene {{name}}. For example, you might consider pathways that are upstream of the gene or compensatory mechanisms.

Inputs: You are provided
- Description of gene of interest {{name}}
- Database entries relating {{name}} to other genes or pathways

Format:
- Write up to five sentences describing potential molecular and cellular perturbations that may impact the levels of {{name}}.

Constraints:
- Remain faithful to all domain knowledge. Do not make up additional information.
- Summarize all common aspects succintly, but point out notable differences within these sets of genes.
- Maintain a professional tone throughout. Do not comment on your own writing. Do not add any notes or references.
- Omit the importance or impact of the gene. Focus only on its function.
- Omit all non-specific information and obvious statements, e.g. "this gene is involved in cellular processes."

Description of gene {{name}}: {{summary}}

Relations to other genes:
{{entries}}

Perturbations that may affect the levels of {{name}}:
"""

