#!/bin/bash
for FA in $(ls *.msa_in.fa)
do
  OUT=${FA/.msa_in.fa/}".msa_out.fa"
  if [ -e $OUT ]; then
    echo "$OUT exists. Skip."
  else
    echo $OUT
    mafft $FA > $OUT
  fi
done
