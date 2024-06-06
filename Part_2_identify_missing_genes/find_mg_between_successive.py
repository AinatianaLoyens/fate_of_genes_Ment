#!/usr/bin/env python3

#This script will extract lines with holes where its upstream and the downstream genes are successive

import os

dir_of_final="align_final"  #There is normally a dir called align_final in the dir of this script
hole='||||||||||||||||||||'

###Step 1: Define a function which determine if two genes are successive i.e. their numbers have a difference of 10
def aresuccessive(gene1, gene2):
    last_six_1 = gene1[-6:]
    last_six_2 = gene2[-6:]

    num1=int(last_six_1)
    num2=int(last_six_2)
    return abs(num1 - num2) == 10

print(aresuccessive("ME_e1834_053g0318871", "ME_e1834_053g0318841")) #Expected False #Observed False
print(aresuccessive ("ME_e1834_027g0217111", "ME_e1834_027g0217101")) #Expected True #Observed True

#Step 2: Extract the line where a hole is between consecutive

#Get lists of all genes for each contig

for filename in os.listdir(dir_of_final):
    print('We are processing this file:', filename)
    acc=0
    contig1=[] #A list of all genes in the first contig
    contig2=[] #A list of all genes in the second contig
    contig3=[] #A list of all genes in the third contig

    file=open(os.path.join(dir_of_final, filename),'r')
    for line in file:
        columns=line.split()
        contig1.append(columns[0])
        contig2.append(columns[1])
        contig3.append(columns[2])
    file.close()
    #The three contig_lists have the same length
    #print(len(contig1) == len(contig2) and len(contig2) == len(contig3))

    #Extract the upstream and the downstream of each hole
    file_loss=filename.replace('final.txt','expected_loss.txt')
    file_to_write=open(file_loss, 'w')
    for j in range(len(contig1)): #Never out of range because a file can't begin or end with a hole
        if contig1[j] == hole or contig2[j] == hole or contig3[j] == hole: #If there is an hole at this line,...
            #...verify where it is and assign the upstream and downstream of each hole
            if contig1[j] == hole:
                i=j-1
                while contig1[i] == hole: 
                    i-=1 #We keep searching an upstream gene if the current upstream gene is an hole
                upstream = contig1[i]
                k=j+1
                while contig1[k] == hole:
                    k+=1 #We keep searching an downstream gene if the current downstream gene is an hole
                downstream = contig1[k]
            elif contig2[j] == hole:
                i=j-1
                while contig2[i] == hole: 
                    i-=1 #We keep searching an upstream gene if the current upstream gene is an hole
                upstream = contig2[i]
                k=j+1
                while contig2[k] == hole:
                    k+=1 #We keep searching an downstream gene if the current downstream gene is an hole
                downstream = contig2[k]
            elif contig3[j] == hole:
                i=j-1
                while contig3[i] == hole: 
                    i-=1 #We keep searching an upstream gene if the current upstream gene is an hole
                upstream = contig3[i]
                k=j+1
                while contig3[k] == hole:
                    k+=1 #We keep searching an downstream gene if the current downstream gene is an hole
                downstream = contig3[k]
            
            #Verify if uptream and downstream are successive
            if aresuccessive(upstream, downstream):
                acc+=1
                #print('Un trou entre consécutifs')
                #Write the lines where an hole is between successive genes
                file_to_write.write(contig1[i] + ' ' + contig2[i] + ' ' + contig3[i] + '\n') #Write it only if we need the context
                file_to_write.write(contig1[j] + ' ' + contig2[j] + ' ' + contig3[j] + '\n')
                file_to_write.write(contig1[k] + ' ' + contig2[k] + ' ' + contig3[k] + '\n' + '\n') #Write it only if we need the context
    print('Number of holes between successive:', acc)       
    file_to_write.close()
