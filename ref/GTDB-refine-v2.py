#!/usr/bin/env python3
import sys
import os

rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}


def revcomp(tmp_seq):
    return ''.join([rc[x] for x in tmp_seq[::-1]])


filename_vulgar = sys.argv[1]
filename_fa = '%s.fa' % filename_vulgar.split('.')[1]
filename_out = filename_fa.replace('_v2.fa', '') + '_v3.fa'
filename_log = filename_fa.replace('_v2.fa', '') + '_v3.log'

if not os.access(filename_fa, os.R_OK):
    sys.stderr.write('%s is not available. Check it first\n' % filename_fa)
    sys.exit(1)

str_info = dict()
f_vulgar = open(filename_vulgar, 'r')
for line in f_vulgar:
    tokens = line.strip().split()
    str_info[tokens[5]] = tokens[8]
f_vulgar.close()

seq_list = dict()
f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        seq_list[tmp_h] = []
    else:
        seq_list[tmp_h].append(line.strip())
f_fa.close()

f_out = open(filename_out, 'w')
f_log = open(filename_log, 'w')
for tmp_h in sorted(seq_list.keys()):
    tmp_seq = ''.join(seq_list[tmp_h])
    if tmp_h not in str_info:
        sys.stderr.write('Not available: %s\n' % tmp_h)
        f_log.write('Not available: %s\n' % tmp_h)
        continue

    tmp_residual = set(tmp_seq) - set(['A', 'T', 'G', 'C', 'N'])
    for tmp_r in list(tmp_residual):
        tmp_seq = tmp_seq.replace(tmp_r, 'N')

    if str_info[tmp_h] == '+':
        f_out.write(">%s\n%s\n" % (tmp_h, tmp_seq))
    elif str_info[tmp_h] == '-':
        f_out.write(">%s\n%s\n" % (tmp_h, revcomp(tmp_seq)))
f_out.close()
f_log.close()
