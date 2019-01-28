#!/bin/bash
SAMPLE=$1

for FA in $(ls *$SAMPLE*/scaffolds.fasta)
do
    NEW=${FA/\/scaffolds.fasta/.spades_scaffolds.fa}
    echo "$FA --> $NEW"
    mv $FA $NEW
done
