#!/usr/bin/env python3

#This script will create a file with two columns : one with the skipped genes and one with the corresponding duplication category

import os
dir_of_skipped_genes='align_skipped_genes' #There is normally a dir called align_skipped_genes in the dir of this script

#Create a dictionnary where the keys are the protein-coding genes and the values are their duplication category
gene_type_dict={}
with open('MENTE1834.20230906.recipeA.gene_type', 'r') as file:
    for line in file:
        gene, gene_type = line.strip().split()
        gene_type_dict[gene] = gene_type

for filename in os.listdir(dir_of_skipped_genes):
    #Put the skipped_genes in a list
    with open(os.path.join(dir_of_skipped_genes,filename), 'r') as file:
        skipped_genes = [line.strip() for line in file]

    #Create the file where a skipped gene is associated to its duplication category if it's a protein-coding gene
    file_gene_type=filename.replace('skipped_genes.txt','skipped_genes_type.txt')
    with open(file_gene_type, 'w') as file:
        for gene in skipped_genes:
            if gene in gene_type_dict:
                file.write(f"{gene}\t{gene_type_dict[gene]}\n")
            else:
                file.write(f"{gene}\tNA\n")