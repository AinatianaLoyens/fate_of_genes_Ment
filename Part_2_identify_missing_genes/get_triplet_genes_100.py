#!/usr/bin/env python3


#This script will use a genes_ment.txt file as input
#to make a file which is contains triplets or couples on genes of each triplet of alignment
#Genes are put in the column of their contig

genes_file='genes_100_ment.txt' #Put the path of genes_N_ment.txt here


#Create a list of alignments
#Each element of this list is a list of strings which are the name of the three alignments involved in a triplet
alignments_list=[] #The list of triplets of alignment
file_to_read=open(genes_file,'r')
for line in file_to_read:
    columns=line.split('\t') #We separate the columns of three genes and the columns of three alignments. They are separated by a tabulation
    alignments=columns[1]
    alignments_splitted=alignments.split()
    #print(alignments_splitted)
    if len(alignments_splitted)==3: #We only continue if we have 3 alignments
        three_alignments=[alignments_splitted[0],alignments_splitted[1],alignments_splitted[2]] #We put the three alignments of the triplet in a alignments_list
        three_alignments.sort()
        if three_alignments not in alignments_list:
            alignments_list.append(three_alignments) #We add the list of three alignments to the list alignments_list #In a certain order to not have doubles

file_to_read.close()
print(alignments_list)

#Creating one file per three-alignments
for a in alignments_list:
    print('Nous créons le fichier de cet alignement \n', a)
    #Naming the file we are creating
    alignment_1_number=a[0].split(':')[0] #We extract the three last caracters of the first contig : it's the number
    alignment_2_number=a[1].split(':')[0]
    alignment_3_number=a[2].split(':')[0]
    filename=alignment_1_number + '_' + alignment_2_number + '_' + alignment_3_number + '_temp.txt' #The the temporary files 
    #Writing genes in the file
    file_triple_genes=open(filename,'w')    
    file_gene=open(genes_file,'r') #We are reading the file genes_N_ment.txt in order to find the ones which correspond to the triplet
    for line in file_gene:
        
        columns=line.split('\t') #We separate the columns of three genes and the columns of three alignments. They are separated by a tabulation
        genes=columns[0]
        alignments=columns[1]
        alignments_splitted=alignments.split()
        #print(genes)
        #print(alignments)
        if len(alignments_splitted)==1 or len(alignments_splitted)==3: 
            alignment1=alignments_splitted[0]
            if len(alignments_splitted) == 3: #Because sometimes there is only 1 alignment (2 genes)
                alignment2=alignments_splitted[1]
                alignment3=alignments_splitted[2]

            
            #Here test if the alignments at this line are all from the triplet
            if len(alignments_splitted) == 1:
                #print('Ligne de deux colonnes')

                if alignment1 in a:
                    #print('Les deux alignements sont dans le triplet')         
                    file_triple_genes.write(genes + '\n') #The goal is to write the group in the file.
                #else:
                    #print('Au moins un des deux alignements pas dans le triplet')
            elif len(alignments_splitted) == 3:
                if alignment1 in a and alignment2 in a and alignment3 in a:
                    file_triple_genes.write(genes + '\n')
                #else:
                    #print('Au moins un des trois gènes pas dans le triplet')
    file_gene.close()
    file_triple_genes.close()

#Creating files where the genes are in the good column.
import glob
pattern='*_temp.txt' #Each temporary file
list_of_files = glob.glob(pattern)

for filename_temp in list_of_files:
    file_temp=open(filename_temp,'r')
    new_filename=filename_temp.rstrip("_temp.txt") + '.txt'
    new_file=open(new_filename,'w')
    
    for line in file_temp:
        group=['||||||||||||||||||||','||||||||||||||||||||','||||||||||||||||||||']  #This list will change depending on the content of the couple or the triplet.
        genes=line.split()
        if len(genes) == 3:
            genes.sort()
            new_file.write(genes[0] + ' ' + genes[1] + ' ' + genes[2] + '\n' )
            three_contigs=[genes[0][0:12],genes[1][0:12],genes[2][0:12]] #It's always the same because we it's sorted but we can't do otherwise
        elif len(genes) == 2:
            if genes[0][0:12] == three_contigs[0]: #We assign the gene1 to the correct column #three_contigs is the last three_contigs we had
                group[0] = genes[0] 
                #print('gene1 match avec', group[0])
            elif genes[0][0:12] == three_contigs[1]:
                group[1] = genes[0]
                #print('gene1 match avec', group[1])
            elif genes[0][0:12] == three_contigs[2]:
                group[2] = genes[0]
                #print('gene1 match avec', group[2])
            
            if genes[1][0:12] == three_contigs[0]: #We assign the gene2 to the correct column
                group[0] = genes[1] 
                #print('gene1 match avec', group[0])
            elif genes[1][0:12] == three_contigs[1]:
                group[1] = genes[1]
                #print('gene1 match avec', group[1])
            elif genes[1][0:12] == three_contigs[2]:
                group[2] = genes[1]
                #print('gene1 match avec', group[2])          
            new_file.write(group[0] + ' ' + group[1] + ' ' + group[2] + '\n')  