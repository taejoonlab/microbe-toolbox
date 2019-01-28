#!/bin/bash

REF="/home/taejoon/Microbiome/db/ECOLI_ASM584v2_ens42.dna_sm.fa"

for BAM in $(ls ../bwa/*.rmdup.bam)
do
  OUT=${BAM/.rmdup.bam/}
  OUT=$(basename $OUT)

  /home/taejoon/src/strelka/2.8.3/bin/configureStrelkaGermlineWorkflow.py \
    --referenceFasta=$REF --runDir=$OUT --bam=$BAM
done
