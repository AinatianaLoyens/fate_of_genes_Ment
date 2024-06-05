#!/usr/bin/env python3

#Some contigs are "too short" to entirely match on the two others in the block
#They some genes are considered as lost on them but it's actually the beginning or the ending of the contigs
#This script will give a file which contains only the center region (no part before the beginning or after the ending of the contig)

import os 
dir_of_ordered = 'align_ordered' #There is normally a dir called align_ordered in the dir of this script

###Step 1 : Define a function which determine if a line has got an hole

def hasanhole(line):
    '''This function determine if one of the three genes in a line is an hole'''
    hole='||||||||||||||||||||'
    genes=line.split()
    return hole in genes

#print(hasanhole('|||||||||||||||||||| ME_e1834_027g0215721 ME_e1834_053g0317391'))
#print(hasanhole('ME_e1834_005g0072761 ME_e1834_027g0215631 ||||||||||||||||||||\n')) #It was to test if the function works when the hole is followed by \n

###Step 2 : Store in a list the lines which contain holes in the beginning and in the ending of the file 
###In any contig? Let's say yes first

for filename_ordered in os.listdir(dir_of_ordered):
    all_lines=[] #will contain all lines. It will be useful to delete lines from the ending
    file_ordered=open(os.path.join(dir_of_ordered, filename_ordered), 'r')
    for line in file_ordered:
        all_lines.append(line)
    file_ordered.close()
    print(len(all_lines))

    lines_to_delete_begin=[] #will contain the lines to delete (from the beginning)
    for i in all_lines:
        if hasanhole(i):
            lines_to_delete_begin.append(i)
        else:
            break #We break the loop at the first line without hole
    print('number of 1st lines to delete', len(lines_to_delete_begin))

    lines_to_delete_end=[] #will contains the lines to delete (from the end)
    for i in reversed(all_lines):
        if hasanhole(i):
            lines_to_delete_end.append(i)
        else:
            break #We break the loop at the first line without hole
    print('number of last lines to delete', len(lines_to_delete_end))

    lines_to_delete = lines_to_delete_begin + lines_to_delete_end #All lines to delete
    print(len(lines_to_delete_begin), '+', len(lines_to_delete_end), '=', len(lines_to_delete) )

    #Everything right for the Step2

    ###Step3 : Write the ordered file without the lines to delete

    filename_centered = filename_ordered.replace('ordered.txt', 'centered.txt') #The files are now called 'xxx_centered.txt'
    file_centered=open(filename_centered, 'w')
    for i in all_lines:
        if i not in lines_to_delete:
            print('Cette ligne est à conserver')
            file_centered.write(i)
        else:
            print('Cette ligne est à supprimer')
    file_centered.close()
