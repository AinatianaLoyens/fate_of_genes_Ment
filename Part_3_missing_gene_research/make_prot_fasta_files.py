#!/usr/bin/env python3

###This script will create a directory per align in align_gene_exonerate called alignX_Y_Z_gene_dir...
###In each folder, there will be the fasta files of each gene in alignX_Y_Z_gene_exonerate.txt

import os

prot_fasta_file='menterolobii.e1834.20230906.recipeA_prot.fna'  #The fasta of all proteins in the genome

#Create the directories
current_dir=os.getcwd()
exonerate_dir=os.path.join(current_dir, "align_gene_exonerate")
exonerate_files= [f for f in os.listdir(exonerate_dir) if f.endswith("exonerate.txt")] #the files of genes
for filename in exonerate_files:
    new_dir=filename.replace("exonerate.txt","dir")
    new_dir_path=os.path.join(exonerate_dir,new_dir)
    if not os.path.exists(new_dir_path):
        os.mkdir(new_dir_path) #a directory per file of genes
    #Store the genes per file
    with open(os.path.join(exonerate_dir, filename),'r') as file_to_read:
        #print('The genes in', filename, ':')
        genes= [line.strip() for line in file_to_read] 
        #print(genes)
    #Path and name of the output
    for g in genes:
        output_file_name=f'{g}_prot.fasta' 
        output_file_path=os.path.join(new_dir_path,output_file_name)
        print('writing', output_file_name)

        #Create a file per gene
        with open(prot_fasta_file, 'r') as fasta_file:
            gene_name=None
            sequence=''
            for line in fasta_file:
                if line.startswith('>'): #if we find a gene
                    if gene_name is not None and gene_name == g: #if we find the current gene
                        print('we found the current gene', gene_name)
                        with open(output_file_path,'w') as output_file:
                            output_file.write(f'>{gene_name}\n') #we write the name of the gene in the file
                            output_file.write(sequence + '\n') #we write the sequence in the file
                            print('we wrote its fasta')
                    gene_name=line.strip()[1:21] #we change the name of the gene each time we find a gene. The gene name is the 2nd to 21st character
                    sequence=''
                else: #if we don't find a gene but a sequence
                    sequence += line.strip() #we change the sequence of the gene
            if gene_name is not None and gene_name == g: #we need to write the last gene if applicable
                print('we found the current gene')
                with open(output_file_path,'w') as output_file:
                    output_file.write(f'>{gene_name}\n') #we write the name of the gene in the file
                    output_file.write(sequence + '\n') #we write the sequence in the file  
                    print('we found the current gene')              



    

