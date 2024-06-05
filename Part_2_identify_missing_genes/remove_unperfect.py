#!/usr/bin/env python3

#Some triplets of genes are matching to each other as following : X with Y - Y with Z - X not with Z
#In this case, the gene Y is written in two consecutive lines in the file
#This script will remove those lines

import os

hole='||||||||||||||||||||'
dir_of_centered = 'align_centered' #There is normally a dir called align_centered in the dir of this script

###Step 1: fill a list of all lines in the file

for file_centered in os.listdir(dir_of_centered):
    print('We are processing this file:', file_centered)
    all_lines=[] #A list of lists which will contain all lines. 
    #Example : [['||||||||||||||||||||','ME_e1834_027g0215721','ME_e1834_053g0317391'],['ME_e1834_005g0072761','ME_e1834_027g0215631','||||||||||||||||||||']] 

    file=open(os.path.join(dir_of_centered, file_centered), 'r')
    for line in file:
        three_genes=line.split()
        all_lines.append(three_genes)
    file.close()

    #print('informations sur all_lines:')
    #print('le début de all_lines:', all_lines[:3])
    #print('la fin de all_lines:', all_lines[-3:])
    #print('longueur de all_lines', len(all_lines), '\n') #all_lines is correct

    ###Step 2: fill a list of all genes and a list of genes written twice

    all_genes=[] #will contains all genes (which are not hole)
    twicegenes=[] #A list of genes written twice in the file
    for t in all_lines: #take each three_genes in all_lines
        for g in t: #take each gene in the three_genes
            if g not in all_genes and g != hole: #The gene is not already listed and is not an hole
                all_genes.append(g)
            elif g in all_genes :
                twicegenes.append(g)

    #print('informations sur all_genes:')
    #print('le début de all_genes:', all_genes[:5])
    #print('la fin de all_genes:', all_genes[-5:])
    #print('longueur de all_genes', len(all_genes), '\n') #all_genes is realistic but wasn't checked precisely

    #print('informations sur twicegenes:')
    #print('twicegenes', twicegenes)
    #print('le début de twicegenes:', twicegenes[:5])
    #print('la fin de twicegenes:', twicegenes[-5:])
    #print('longueur de twicegenes', len(twicegenes), '\n') #twicegenes is correct

    ###Step 3: write a file without the lines where a twicegenes is there

    #The name of the file to write 
    file_final = file_centered.replace('centered.txt', 'final.txt') #The files are now called 'xxx_final.txt'

    file_to_write=open(file_final,'w')
    file_to_read=open(os.path.join(dir_of_centered, file_centered), 'r') 
    lines_ignored=0 
    for line in file_to_read:
        three_genes=line.split()
        #If all genes in three genes are not in twicegenes : write it
        if not any(gene in twicegenes for gene in three_genes):
            file_to_write.write(line)
        else:
            #The line has been ignored and is not written
            lines_ignored += 1
    file_to_read.close()
    file_to_write.close()

    print('number of lines ignored:', lines_ignored) #lignes_ignored is realistic. 

#all_lines - lines_ignored = 159 - 34 = 125 = number of lines of contig_final.txt #correct.