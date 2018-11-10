#!/usr/bin/env python3

## Source: illumina-adapter-sequences-1000000002694-08.pdf

seq_7 = 'CAAGCAGAAGACGGCATACGAGAT %s GTCTCGTGGGCTCGG'
seq_5 = 'AATGATACGGCGACCACCGAGATCTACAC %s TCGTCGGCAGCGTC'

data_i7="""
TCGCCTTA N701 TAAGGCGA
CTAGTACG N702 CGTACTAG
TTCTGCCT N703 AGGCAGAA
GCTCAGGA N704 TCCTGAGC
AGGAGTCC N705 GGACTCCT
CATGCCTA N706 TAGGCATG
GTAGAGAG N707 CTCTCTAC
CCTCTCTG N708 CAGAGAGG
AGCGTAGC N709 GCTACGCT
CAGCCTCG N710 CGAGGCTG
TGCCTCTT N711 AAGAGGCA
TCCTCTAC N712 GTAGAGGA
"""

data_i5 = """
TAGATCGC [N/S/E]501 TAGATCGC GCGATCTA
CTCTCTAT [N/S/E]502 CTCTCTAT ATAGAGAG
TATCCTCT [N/S/E]503 TATCCTCT AGAGGATA
AGAGTAGA [N/S/E]504 AGAGTAGA TCTACTCT
GTAAGGAG [N/S/E]505 GTAAGGAG CTCCTTAC
ACTGCATA [N/S/E]506 ACTGCATA TATGCAGT
AAGGAGTA [N/S/E]507 AAGGAGTA TACTCCTT
CTAAGCCT [N/S/E]508 CTAAGCCT AGGCTTAG
GCGTAAGA [N/S/E]517 GCGTAAGA TCTTACGC
"""

for line in data_i7.split("\n"):
    tokens = line.strip().split()
    if len(tokens) == 0:
        continue
    tmp_i7_seq = tokens[0]
    tmp_i7_name = tokens[1]
    print(">Nextera_%s" % tmp_i7_name)
    print(seq_7 % tmp_i7_seq)

for line in data_i5.split("\n"):
    tokens = line.strip().split()
    if len(tokens) == 0:
        continue
    tmp_i5_seq = tokens[0]
    tmp_i5_name = 'N' + tokens[1].split(']')[1]
    print(">Nextera_%s" % tmp_i5_name)
    print(seq_5 % tmp_i5_seq)
