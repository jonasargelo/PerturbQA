import json
import os
import numpy as np
from tqdm.auto import tqdm


def load_string_data(string_json_path):
    """Load STRING protein interaction data from JSON file."""
    with open(string_json_path) as f:
        string = json.load(f)
    return string


def build_neighbors_dict(string_data):
    """Build dictionary with set of neighbors for each protein."""
    string_neighbors = {}
    
    for k, v in string_data.items():
        neighbors = set()
        for edge in v:
            neighbors.add(edge[0])
        string_neighbors[k] = neighbors
    
    return string_neighbors


def find_top_shared_neighbors(string_neighbors, top_k=10):
    """
    Find genes with the most shared neighbors for each gene.
    
    Args:
        string_neighbors: Dictionary mapping genes to their neighbor sets
        top_k: Number of top genes to return for each gene
        
    Returns:
        Dictionary mapping each gene to its top_k genes with most shared neighbors
    """
    top_neighbors_dict = {}
    all_genes = list(string_neighbors.keys())
    
    print(f"Processing {len(all_genes)} genes...")
    
    for gene in tqdm(all_genes):
        shared_neighbors = []
        for gene2 in all_genes:
            if gene != gene2:
                common_neighbors = string_neighbors[gene].intersection(string_neighbors[gene2])
                shared_neighbors.append(len(common_neighbors))
        
        # Find the top_k genes with the most shared neighbors
        top_indices = np.argsort(shared_neighbors)[-top_k:]
        top_neighbors = [all_genes[i] for i in top_indices]
        top_neighbors_dict[gene] = top_neighbors
    
    return top_neighbors_dict


def main():
    """Main function to run the neighbor analysis."""
    # Find the repository root and construct absolute path to STRING data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    string_json_path = os.path.join(repo_root, "PerturbQA", "perturbqa", "datasets", "kg", "string.json")
    
    # Check if the file exists
    if not os.path.exists(string_json_path):
        print(f"Error: STRING data file not found at {string_json_path}")
        print("Please ensure the string.json file exists in the correct location.")
        return
    
    print("Loading STRING data...")
    string_data = load_string_data(string_json_path)
    print(f"Loaded {len(string_data)} genes from STRING database")
    
    # Show example of data structure
    if string_data:
        first_gene = list(string_data.keys())[0]
        print(f"Example gene: {first_gene}")
        print(f"Example edges: {string_data[first_gene][:3]}...")  # Show first 3 edges
    
    print("Building neighbors dictionary...")
    string_neighbors = build_neighbors_dict(string_data)
    
    print("Finding genes with most shared neighbors...")
    top_neighbors_dict = find_top_shared_neighbors(string_neighbors, top_k=10)
    
    
    print(f"\nAnalysis complete! Found top neighbors for {len(top_neighbors_dict)} genes.")
    
    # Save results to gene_neighbors directory
    output_dir = os.path.join(repo_root, "PerturbQA", "examples", "gene_neighbors")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "string.json")
    
    with open(output_file, 'w') as f:
        json.dump(top_neighbors_dict, f, indent=2)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()