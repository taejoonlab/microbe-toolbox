#!/bin/bash
VSEARCH="$HOME/src/vsearch/vsearch-2.13.4/bin/vsearch"

FA=$1

for ID in 99 
do
  OUT=${FA/.fa/}".uc"$ID
  $VSEARCH --cluster_smallmem $FA --uc $OUT --usersort --threads 4 --id 0.$ID
done
