#!/bin/bash

#FA=$1

for FA in $(ls *fa)
do
PRIMER="$HOME/git/microbe-toolbox/ILMN_V4/ILMN_V4_primers.ipcress"
OUT="ILMN_V4."$FA
OUT=${OUT/.fa/}".ipcress_out"

ipcress $PRIMER $FA | grep ^ipcress > $OUT
/home/taejoon/git/microbe-toolbox/ILMN_V4/get-V4_seq.py $FA $OUT > ${FA/.fa/}"+V4.fa"
done
