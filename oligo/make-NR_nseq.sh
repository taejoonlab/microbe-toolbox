#!/bin/bash

DIR_RRNA_FA=$1
DIR_SCRIPT=$(dirname $0)

for FA in $(ls $DIR_RRNA_FA/*fa)
do
  echo $FA
  $DIR_SCRIPT/make-NR_nseq.py $FA
done
