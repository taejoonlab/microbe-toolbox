#!/bin/bash
#IPCRESS="/work/project/src/exonerate/exonerate-2.4.0/src/program/ipcress"
IPCRESS="/work/project/src/exonerate/exonerate-2.2.0-x86_64/bin/ipcress"
MISMATCH=2

USAGE_MESG="\n Usage: run-ipcress.sh <ipcress input file> <fasta paths>\n
  using $IPCRESS\n"

IPCRESS_IN=$1
FASTA_DB=$2

if [ $# -lt 2 ]; then
  echo -e $USAGE_MESG
  exit
fi

if [ ! -e $IPCRESS_IN ]; then
  echo "IPCRESS input file "$IPCRESS_IN" is not available."
  echo -e $USAGE_MESG
  exit
fi

if [ ! -e $FASTA_DB ]; then
  echo "FASTA DB file "$FASTA_DB" is not available."
  echo -e $USAGE_MESG
  exit
fi

$IPCRESS -m $MISMATCH $IPCRESS_IN $FASTA_DB
