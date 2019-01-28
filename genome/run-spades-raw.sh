#!/bin/bash

NUM_THREADS=4

## Run trimmermatic & flash before running this.

for FQ_1 in $(ls ../fastq/*CCARM*_R1.raw.fastq.gz)
do
  FQ_2=${FQ_1/_R1/_R2}

  OUT=$(basename $FQ_1)
  OUT=${OUT/_R1.raw.fastq.gz}".raw"

  spades.py -t $NUM_THREADS --phred-offset auto -o $OUT -1 $FQ_1 -2 $FQ_2
done
