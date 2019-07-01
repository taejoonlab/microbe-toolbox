#!/bin/bash

for FA in $(ls ../Ptags/*Ptags.fa)
do
  OUT=$(basename $FA)
  OUT=${OUT/.fa/}".mapseq_out"
  $HOME/src/MAPseq/mapseq-1.2.3-linux/mapseq $FA > $OUT
done
