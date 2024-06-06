#!/bin/bash

###This script execute exonerate on every *_cds.fasta

#Load modules
module load bioinfo/Exonerate/2.2.0

# The corresponding files:
for file in align_gene_exonerate/align*_dir/*_prot.fasta; do
    # Extraction of the path and the name of the file without extension
    file_path=$(dirname "$file")
    file_name=$(basename "$file" _prot.fasta)
    
    # Output path for the exonerate result
    output_path="$file_path/${file_name}_prot2genome.exonerate"
    echo "Creating $output_path"
    #Execute exonerate on the file
    exonerate -q $file -t Meloidogyne_enterolobii_E1834_Hifi_Peregrine_genome.fa -m protein2genome -n 5 > $output_path
    echo "This file is created $output_path"
done
