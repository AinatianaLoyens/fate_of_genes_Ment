#!/usr/bin/env python3

#This script will put in a file the genes that are skipped between the three contigs of a file.

import glob
import os

hole='||||||||||||||||||||'
dir_of_centered = 'align_centered' #There is normally a dir called align_centered in the dir of this script
#not 'ordered' because there are the begining/ending of the contig
#not 'final' because the unclosed triangles are already removed so they will be considered as a skipped gene
#The remaining is 'centered'

###Step 1 : create lists of genes in contigs in alphabetical order

###This step takes as inputs files with 3 columns (1 contig per column)
###Each contig contains genes
for filename in os.listdir(dir_of_centered):
    print('We are processing this file:', filename)
    file=open(os.path.join(dir_of_centered,filename),'r') 
    cont1_list=[] 
    cont2_list=[]
    cont3_list=[] #A list of genes of each contig
    for line in file:
        columns=line.split()
        gene1=columns[0]
        gene2=columns[1]
        gene3=columns[2]
        cont1_list.append(gene1)
        cont2_list.append(gene2)
        cont3_list.append(gene3) #We fill each cont_list with the genes it has
    file.close()

    cont1_list.sort()
    cont2_list.sort()
    cont3_list.sort() #We sort each cont_list depending on the genes they have

    #contN_list will be used to determine the skipped genes. Skipped genes are in the total list but not in contN_list

    ###Step 2: Create lists that contains all the supposed genes of the contigs
    #We create a sorted list without hole in order to make the indexation possible
    cont1_gene_list=[g for g in cont1_list if g != hole] 
    cont2_gene_list=[g for g in cont2_list if g != hole]
    cont3_gene_list=[g for g in cont3_list if g != hole]
    #print('cont1_list',cont1_list)
    #contN_gene_list will be used to determine the skipped genes. Skipped genes are in the total list but not in contN_list

    #We give the contig name to each contig, which is the 12 first caracters of the gene name
    #To get the gene name, we just take the first element of the gene list of each contig
    cont1_name=cont1_list[0][:13]
    cont2_name=cont2_list[0][:13]
    cont3_name=cont3_list[0][:13]

    #We create the lists of all supposed genes for each contig
    cont1_all_gene_list=[cont1_name + f"{i:07}" for i in range(int(cont1_gene_list[0][13:]), int(cont1_gene_list[-1][13:]) + 1, 10)] 
    cont2_all_gene_list=[cont2_name + f"{i:07}" for i in range(int(cont2_gene_list[0][13:]), int(cont2_gene_list[-1][13:]) + 1, 10)] 
    cont3_all_gene_list=[cont3_name + f"{i:07}" for i in range(int(cont3_gene_list[0][13:]), int(cont3_gene_list[-1][13:]) + 1, 10)] 

    ###Step 3: Create the list of skipped genes

    skipped_gene1= [gene for gene in cont1_all_gene_list if gene not in cont1_gene_list]
    skipped_gene2= [gene for gene in cont2_all_gene_list if gene not in cont2_gene_list]
    skipped_gene3= [gene for gene in cont3_all_gene_list if gene not in cont3_gene_list]

    ###Step 4: Write the skipped genes in a file
    file_skipped_genes = filename.replace('centered.txt','skipped_genes.txt')
    file_to_write=open(file_skipped_genes,'w')
    for g in skipped_gene1:
        #print(g)
        file_to_write.write(g + '\n')
    for g in skipped_gene2:
        file_to_write.write(g + '\n')
    for g in skipped_gene3:
        file_to_write.write(g + '\n')
    file_to_write.close()    


