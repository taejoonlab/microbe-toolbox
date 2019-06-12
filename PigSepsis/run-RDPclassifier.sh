#!/bin/bash

#FA=$1

#if [ -e $FA ]; then
for FA in $(ls *V4.fa)
do
  OUT=${FA/.fa/}".RDPcls"
  echo $OUT
  java -jar ~/git/RDPTools/classifier.jar classify $FA -o $OUT
  ANNOT=${FA/.fa/_annot.fa}
  ~/git/microbe-toolbox/annot-fasta-RDPcls.py $FA $OUT > $ANNOT
done
#fi
