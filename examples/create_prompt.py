import json
import os
import argparse
import polars as pl

def create_template_de():
    k562 = ("K562 cells", "K562 cells are immortalised myelogenous leukemia cells of the erythroleukemia type.")

    desc_pert = "description of gene that is perturbed via CRISPRi knockdown"
    desc_gene = "description of gene, the impact on which you wish to infer"
    desc_context = "description of cell line in which the genes are expressed"
    desc_obs = "set of experimental observations that describe the impact of CRISPRi perturbations on related genes, to contextualize your answer"

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
    - Description of perturbed gene ({{pert}}): {{pert_desc}}\n
    - Description of gene of interest ({{gene}}): {{gene_desc}}\n
    - Context: {{cell_desc}}\n
    - Examples: 
    {{obs}}
    [End of Input]"""

    return prompt_test_de


def get_summaries(args):
    """Load gene descriptions from json files."""
    # Get the directory where this script is located and navigate to gene_summary
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gene_summary_dir = os.path.join(os.path.dirname(script_dir), 'gene_summary')
    
    desc_pert_path = os.path.join(gene_summary_dir, 'desc_pert.json')
    desc_gene_path = os.path.join(gene_summary_dir, 'desc_gene.json')
    
    with open(desc_pert_path, 'r') as file:
        desc_pert_dict = json.load(file)

    with open(desc_gene_path, 'r') as file:
        desc_gene_dict = json.load(file)

    return desc_pert_dict, desc_gene_dict

def construct_obs(pert_gene, target_gene):
    """Construct the observations string based on perturbed and target genes."""
    neighbors_dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gene_neighbors', 'string.json')

    # Load neighbors dictionary
    with open(neighbors_dict_path, 'r') as f:
        neighbors_dict = json.load(f)

    pert_neighbors = set(neighbors_dict.get(pert_gene, []))
    target_neighbors = set(neighbors_dict.get(target_gene, []))

    # Load the DE data
    de_data_path = os.path.join("/home/j.argelo/llm_scFMs/PerturbQA/perturbqa/datasets/k562-de.csv")
    de_data = pl.read_csv(de_data_path)

    # Filter to split = train
    de_data = de_data.filter(pl.col("split") == "train")

    max_examples = 10
    # Get tuples where both the pert and gene are in the respective neighbors lists
    de_data_both_in = de_data.filter(pl.col("pert").is_in(pert_neighbors) & pl.col("gene").is_in(target_neighbors))
    obs_tuples = de_data_both_in.select(["pert", "gene", "label"]).limit(max_examples).to_dicts()

    # Get tuples where only the pert is in the pert_neighbors list if less than max_examples
    if len(obs_tuples) < max_examples:
        additional_needed = max_examples - len(obs_tuples)
        # de_data_additional = de_data.filter(pl.col("pert").is_in(pert_neighbors) & ~pl.col("gene").is_in(target_neighbors))
        de_data_pert_in = de_data.filter(pl.col("pert").is_in(pert_neighbors))
        additional_tuples = de_data_pert_in.select(["pert", "gene", "label"]).limit(additional_needed).to_dicts()
        obs_tuples.extend(additional_tuples)

    # Get tuples where only the gene is in the target_neighbors list if still less than max_examples
    if len(obs_tuples) < max_examples:
        additional_needed = max_examples - len(obs_tuples)
        de_data_target_in = de_data.filter(~pl.col("pert").is_in(pert_neighbors) & pl.col("gene").is_in(target_neighbors))
        additional_tuples = de_data_target_in.select(["pert", "gene", "label"]).limit(additional_needed).to_dicts()
        obs_tuples.extend(additional_tuples)

    return obs_tuples

def main(args):
    prompt_de = create_template_de()

    desc_pert_dict, desc_gene_dict = get_summaries(args)

    desc_pert = desc_pert_dict[args.pert_gene]
    desc_gene = desc_gene_dict[args.target_gene]

    k562 = ("K562 cells", "K562 cells are immortalised myelogenous leukemia cells of the erythroleukemia type.")

    cell_short, cell_desc = k562

    obs_tuples = construct_obs(args.pert_gene, args.target_gene)

    obs = ""
    for i, obs_tuple in enumerate(obs_tuples):
        pert = obs_tuple['pert']
        gene = obs_tuple['gene']
        label = obs_tuple['label']
        
        # Convert label to outcome text
        if label == 1:
            outcome = f"B) Knockdown of {pert} results in differential expression of {gene}."
        else:
            outcome = f"A) Knockdown of {pert} does not impact {gene}."
        
        obs += f""" Example {i + 1}: Impact of knocking down {pert} on {gene}
    Description of perturbed gene {pert}: {desc_pert_dict[pert]}\n
    Description of gene of interest {gene}: {desc_gene_dict[gene]}

    Outcome: {outcome}
    """

    formatted_prompt = prompt_de.format(pert=args.pert_gene,
                                       gene=args.target_gene,
                                       pert_desc=desc_pert,
                                       gene_desc=desc_gene,
                                       cell_short=cell_short,
                                       cell_desc=cell_desc,
                                       obs=obs)
    
    # Create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "summer", "inputs", "diff_exp")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output filename
    output_filename = f"{args.pert_gene}_{args.target_gene}_example.json"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save as JSON
    output_data = [formatted_prompt]
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Prompt saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pert_gene", type=str, required=True, help="Gene to be perturbed")
    parser.add_argument("--target_gene", type=str, required=True, help="Target gene to analyze")
    args = parser.parse_args()

    main(args)