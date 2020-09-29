#!/usr/bin/env python3
import os
import sys
import gzip

filename_fa = sys.argv[1]
filename_base = filename_fa.replace('.msa_out.fa.gz', '')
filename_base = filename_base.replace('.msa_out.fa', '')
filename_base = os.path.basename(filename_base)

pct_cutoff = 97
chr_list = ['A', 'T', 'G', 'C', '-']

seq_list = dict()
h_list = []
f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        h_list.append(seq_h)
        seq_list[seq_h] = ''
    else:
        seq_list[seq_h] += line.strip()
f_fa.close()

seq_len = len(''.join(seq_list[h_list[0]]))
seq_size = len(seq_list)

chr_seq_list = dict()
chr_seq_list['N'] = [0 for i in range(0, seq_len)]
for tmp_chr in chr_list:
    chr_seq_list[tmp_chr] = [0 for i in range(0, seq_len)]

for tmp_h in h_list:
    for i in range(0, seq_len):
        tmp_chr = seq_list[tmp_h][i].upper()
        if tmp_chr in chr_seq_list:
            chr_seq_list[tmp_chr][i] += 1
        else:
            chr_seq_list['N'][i] += 1

f_score = open('%s.cons_score.txt' % filename_base, 'w')
f_seq = open('%s.cons_seq.fa' % filename_base, 'w')

cons_chr_list = []
f_score.write('# Input : %s\n' % filename_fa)
f_score.write("#Pos\tMaxChr\tMaxPct\t%s\t%s\n" % ('\t'.join(chr_list), 'N'))
for i in range(0, seq_len):
    max_chr = 'N'
    max_chr_count = 0
    chr_count_str_list = []
    for tmp_chr in chr_list + ['N']:
        chr_count_str_list.append('%d' % chr_seq_list[tmp_chr][i])
        if chr_seq_list[tmp_chr][i] > max_chr_count:
            max_chr_count = chr_seq_list[tmp_chr][i]
            max_chr = tmp_chr

    max_pct = int(max_chr_count*100.0 / seq_size)
    f_score.write('%d\t%s\t%d\t%s\n' %
                  (i, max_chr, max_pct, '\t'.join(chr_count_str_list)))

    if max_chr == '-':
        if max_pct > pct_cutoff:
            continue
        else:
            cons_chr_list.append('N')
    else:
        if max_pct > pct_cutoff:
            cons_chr_list.append(max_chr)
        else:
            cons_chr_list.append(max_chr.lower())

f_seq.write(">%s.cons\n%s" % (filename_base, ''.join(cons_chr_list)))
