#!/bin/bash
SAMPLE=$1

for FA in $(ls *$SAMPLE*/contigs.fa)
do
    NEW=${FA/\/contigs.fa/.velvet_ctg.fa}
    echo "$FA --> $NEW"
    mv $FA $NEW
done
