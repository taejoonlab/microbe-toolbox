#!/usr/bin/env python3
import sys

filename_fa = sys.argv[1]
filename_RDPcls = sys.argv[2]

annot_list = dict()
f_RDPcls = open(filename_RDPcls, 'r')
for line in f_RDPcls:
    tokens = line.strip().split("\t")
    if len(tokens) < 23:
        continue

    seq_id = tokens[0]
    tmp_family = tokens[17].replace(' ', '_')
    tmp_family_score = float(tokens[19])
    tmp_genus = tokens[20].replace(' ','_')
    tmp_genus_score = float(tokens[22])
    annot_list[seq_id] = 'f=%s:%.2f|g=%s:%.2f' % (tmp_family, tmp_family_score, tmp_genus, tmp_genus_score)
f_RDPcls.close()

f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_annot = 'f=Unknown:0.00|g=Unknown:0.00'
        if tmp_h in annot_list:
            tmp_annot = annot_list[tmp_h]
        print(">%s|%s" % (tmp_h, tmp_annot))
    else:
        print(line.strip())
f_fa.close()
