#!/bin/bash

NUM_THREADS=4

## Run trimmermatic & flash before running this.

for FQ_s in $(ls ../fastq/*extendedFrags.fastq)
do
  FQ_p=${FQ_s/.extendedFrags/.notCombined}

  OUT=$(basename $FQ_s)
  OUT=${OUT/.extendedFrags.fastq/}".spades"

  echo $FQ_s, $FQ_p
  spades.py -t $NUM_THREADS --phred-offset auto -o $OUT -s $FQ_s --12 $FQ_p
done
