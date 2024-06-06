#!/usr/bin/env python3

###This script will create a directory "align_gene_exonerate"...
###...In this directory, there is a file by alignX_Y_Z_expected loss...
###This file will contains the genes we are going to use on exonerate

import subgenome as subg
import os
import shutil

#Create the directory for the results
result_dir="align_gene_exonerate"
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

#Create the output files
input_dir="align_expected_loss"
for filename in os.listdir(input_dir):
    list_of_genes=subg.take_genes_to_use(os.path.join(input_dir,filename))
    file_output=filename.replace('expected_loss.txt','gene_exonerate.txt')
    file_to_write=open(os.path.join(result_dir,file_output),'w')
    for gene in list_of_genes:
        file_to_write.write(gene + '\n')
    file_to_write.close
