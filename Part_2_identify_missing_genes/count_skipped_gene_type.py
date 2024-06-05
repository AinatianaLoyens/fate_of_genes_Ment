#!/usr/bin/env python3

#This script gives a file of a table which counts the gene by duplication category 

import os
dir_of_skipped_genes_type='align_skipped_genes_type' #There is normally a dir called align_skipped_genes_type in the dir of this script

for filename in os.listdir(dir_of_skipped_genes_type):
    count = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, 'NA': 0}

    #Fill the dictionnary count
    with open(os.path.join(dir_of_skipped_genes_type,filename), 'r') as file:
        for line in file:
            gene, gene_type = line.strip().split('\t')
            count[gene_type] += 1

    print(count)

    #Write the dictionnary count in a txt file
    file_gene_type_count=filename.replace('.txt','_count.txt')
    with open(file_gene_type_count, 'w') as countfile:
        countfile.write('Gene_type\tCounts\n')  # The header
        for gene_type, number in count.items():
            countfile.write(f"{gene_type}\t{number}\n")
