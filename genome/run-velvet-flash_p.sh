#!/bin/bash

VELVETH="$HOME/git/NuevoTx/denovo/velveth-101"
VELVETG="$HOME/git/NuevoTx/denovo/velvetg-101"

#FQ="/path/to/foobar.paired.fastq"

for FQ_pa in $(ls ../fastq/*CCARM*notCombined.fastq)
do
  FQ_sa=${FQ_pa/.notCombined/.extendedFrags}

  for K in 35 25
	do
	  DIRNAME=$(basename $FQ_pa)
	  DIRNAME=${DIRNAME/.notCombined.fastq/}".K"$K"p"

	  $VELVETH $DIRNAME $K -shortPaired -fastq $FQ_pa -short -fastq $FQ_sa
	  $VELVETG $DIRNAME -read_trkg yes -cov_cutoff auto
	done 
done
