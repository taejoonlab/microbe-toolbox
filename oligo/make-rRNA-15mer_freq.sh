#!/bin/bash

DIR_RRNA_FA=$1
KMER_LEN=20

DIR_SCRIPT=$(dirname $0)

for FA in $(ls $DIR_RRNA_FA/*fa)
do
  echo $FA
  $DIR_SCRIPT/make-rRNA-kmer_freq.py $FA $KMER_LEN
done
