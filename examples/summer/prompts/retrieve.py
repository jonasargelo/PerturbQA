"""
This file does not contain prompts, but documentation for the retrieval step

Order of priority
1. same P, close G'
2. same G, close P'
3. close P', close G'
4. same P, random G'
5. same G, random P'
6. close P', random G
7. random P', close G'
"""

import numpy as np


def get_pairs(*, pert, gene,
              close_perts, close_genes,
              seen, seen_gene, budget, seed=0):
    """
    @param pert          perturbation of interest
    @param gene          gene of interest
    
    @param close_perts   neighbors of perturbation of interest
    @param close_genes   neighbors of gene of interest
    
    @param seen          training set perturbations (to sample)
    @param seen_gene     training set genes (to sample)
    
    @param (int) budget  per perturbation + gene + both
    """
    np.random.seed(seed)  # set per instance
    # option 1 and option 2 are XOR based on test setting
    pert_pairs = []
    gene_pairs = []
    if pert in seen:
        for gene2 in close_genes:
            if gene2 in seen[pert]:
                pert_pairs.append((pert, gene2))
    elif gene in seen_gene:
        for pert2 in close_perts:
            if pert2 in seen_gene[gene]:
                gene_pairs.append((pert2, gene))
    if len(pert_pairs) > budget:
        pert_pairs = [pert_pairs[i] for i in np.random.choice(len(pert_pairs), budget, replace=False)]
    if len(gene_pairs) > budget:
        gene_pairs = [gene_pairs[i] for i in np.random.choice(len(gene_pairs), budget, replace=False)]

    # option 3
    both_pairs = []
    for pert2 in close_perts:
        for gene2 in close_genes:
            if gene2 in seen[pert2]:
                both_pairs.append((pert2, gene2))
    if len(both_pairs) > budget:
        both_pairs = [both_pairs[i] for i in np.random.choice(len(both_pairs), budget, replace=False)]

    # options 4 and 5 are mutually exclusive
    cur_pert_pairs = []  # we added original to all_pairs already
    cur_gene_pairs = []
    pert_budget = budget - len(pert_pairs)
    gene_budget = budget - len(gene_pairs)
    if pert in seen and pert_budget > 0:
        for gene2 in seen[pert]:
            cur_pert_pairs.append((pert, gene2))
        if len(cur_pert_pairs) > pert_budget:
            cur_pert_pairs = [cur_pert_pairs[i] for i in np.random.choice(len(cur_pert_pairs), pert_budget, replace=False)]
    elif gene in seen_gene and gene_budget > 0:
        for pert2 in seen_gene[gene]:
            cur_gene_pairs.append((pert2, gene))
        if len(cur_gene_pairs) > gene_budget:
            cur_gene_pairs = [cur_gene_pairs[i] for i in np.random.choice(len(cur_gene_pairs), gene_budget, replace=False)]
    pert_pairs.extend(cur_pert_pairs)
    gene_pairs.extend(cur_gene_pairs)

    # options 6 and 7
    cur_pert_pairs = []  # we added original to all_pairs already
    cur_gene_pairs = []
    pert_budget = budget - len(pert_pairs)
    gene_budget = budget - len(gene_pairs)
    if pert_budget > 0:
        for pert2 in close_perts:
            for gene2 in seen[pert2]:
                cur_pert_pairs.append((pert2, gene2))
        if len(cur_pert_pairs) > pert_budget:
            cur_pert_pairs = [cur_pert_pairs[i] for i in np.random.choice(len(cur_pert_pairs), pert_budget, replace=False)]
    elif gene_budget > 0:
        for gene2 in close_genes:
            for pert2 in seen_gene[gene2]:
                cur_gene_pairs.append((pert2, gene2))
        if len(cur_gene_pairs) > gene_budget:
            cur_gene_pairs = [cur_gene_pairs[i] for i in np.random.choice(len(cur_gene_pairs), gene_budget, replace=False)]
    pert_pairs.extend(cur_pert_pairs)
    gene_pairs.extend(cur_gene_pairs)

    all_pairs = pert_pairs + gene_pairs + both_pairs

    total_budget = budget * 2 - len(all_pairs)
    if total_budget <= 0:
        return all_pairs

    return all_pairs

