#!/usr/bin/env python3
import sys
import gzip

filename_fa = sys.argv[1]
kmer_len = 15

filename_base = filename_fa.replace('.cons_seq.fa', '').replace('.gz','')
filename_out = '%s.cons_%dmer' % (filename_base, kmer_len)

f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')
cons_h = f_fa.readline().strip()
cons_seq = f_fa.readline().strip()
f_fa.close()


def check_kmer(tmp_kmer):
    rv = {'GC_pct': 0.0, 'hetero_pct': 0.0}

    tmp_GC_count = 0
    tmp_hetero_count = 0
    for tmp_n in tmp_kmer:

        if tmp_n in ['G', 'C', 'g', 'c']:
            tmp_GC_count += 1

        if tmp_n not in ['A', 'T', 'G', 'C']:
            tmp_hetero_count += 1

    tmp_GC_pct = tmp_GC_count * 100.0 / len(tmp_kmer)
    tmp_hetero_pct = tmp_hetero_count * 100.0 / len(tmp_kmer)
    return {'GC_pct': tmp_GC_pct, 'hetero_pct': tmp_hetero_pct}

kmer_freq = dict()
for i in range(0, len(cons_seq) - kmer_len):
    tmp_kmer = cons_seq[i:i+kmer_len]
    rv_kmer = check_kmer(tmp_kmer)
    if rv_kmer['GC_pct'] > 60 or rv_kmer['GC_pct'] < 40:
        continue
    if rv_kmer['hetero_pct'] > 0:
        continue
    if tmp_kmer[0] in ['A', 'T'] or tmp_kmer[-1] in ['A', 'T']:
        continue
    if tmp_kmer not in kmer_freq:
        kmer_freq[tmp_kmer] = 1
    kmer_freq[tmp_kmer] += 1

f_out = open(filename_out, 'w')
for tmp_kmer in sorted(kmer_freq.keys(), key=kmer_freq.get):
    f_out.write('%s\t%d\n' % (tmp_kmer, kmer_freq[tmp_kmer]))
f_out.close()
