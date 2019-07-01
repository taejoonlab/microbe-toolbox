#!/usr/bin/env python3
# Source: https://stackoverflow.com/questions/27551921/how-to-extend-ambiguous-dna-sequence

from Bio import Seq
from itertools import product

def extend_ambiguous_dna(seq):
   """return list of all possible sequences given an ambiguous DNA input"""
   d = Seq.IUPAC.IUPACData.ambiguous_dna_values
   r = []
   for i in product(*[d[j] for j in seq]):
      r.append("".join(i))
   return r

primer_V34F = 'CTACGGGNGGCWGCAG'
primer_V34R = 'GACTACHVGGGTATCTAATCC'

idx = 1
for tmp_F in extend_ambiguous_dna(primer_V34F):
    for tmp_R in extend_ambiguous_dna(primer_V34R):
        print("ILMN_V4-%02d\t%s\t%s\t%d\t%d" % (idx, tmp_F, tmp_R, 300, 500))
        idx += 1

#print(extend_ambiguous_dna(primer_V3F))
#print(extend_ambiguous_dna(primer_V34R))
#print(extend_ambiguous_dna(primer_V34F))
