#!/usr/bin/env python3
import sys
import gzip

filename_base = sys.argv[1]
output_name = sys.argv[2]

filename_fq1 = '%s_R1.raw.fastq.gz' % filename_base
filename_fq2 = '%s_R2.raw.fastq.gz' % filename_base
filename_out = '%s_Ptags.fa' % filename_base

divide_Ns = 'NNNNNN'

f_fq1 = open(filename_fq1, 'r')
if filename_fq1.endswith('.gz'):
    f_fq1 = gzip.open(filename_fq1, 'rt')

f_fq2 = open(filename_fq2, 'r')
if filename_fq2.endswith('.gz'):
    f_fq2 = gzip.open(filename_fq2, 'rt')

rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}


def revcomp(tmp_seq):
    return ''.join([rc[x] for x in tmp_seq[::-1]])


tag2freq = dict()
for line in f_fq1:
    if line.startswith('@'):
        h1 = line.strip().split()[0]
        nseq1 = next(f_fq1).strip()
        h1_tmp = next(f_fq1)
        qseq1 = next(f_fq1)

        h2 = next(f_fq2).strip().split()[0]
        nseq2 = next(f_fq2).strip()
        h2_tmp = next(f_fq2)
        qseq2 = next(f_fq2)

        if h1 != h2:
            sys.stderr.write('Error : %s != %s\n' % (h1, h2))
            break

        if nseq1.count('N') > 0 or nseq2.count('N') > 0:
            continue

        tmp_tag = '%s %s %s' % (nseq1, divide_Ns, revcomp(nseq2))
        if tmp_tag not in tag2freq:
            tag2freq[tmp_tag] = 0
        tag2freq[tmp_tag] += 1
f_fq1.close()
f_fq2.close()

sum_freq = sum(tag2freq.values())
tag_idx = 1
f_out = open(filename_out, 'w')
for tmp_tag in sorted(tag2freq.keys(), key=tag2freq.get, reverse=True):
    tmp_pct_tag = '%d_%d' % (tag2freq[tmp_tag], sum_freq)
    tmp_h = '%s.%08d|%s' % (output_name, tag_idx, tmp_pct_tag)
    if tag2freq[tmp_tag] > 5:
        sys.stderr.write('%s\n' % tmp_h)
    f_out.write('>%s\n%s\n' % (tmp_h, tmp_tag))
    tag_idx += 1
f_out.close()
