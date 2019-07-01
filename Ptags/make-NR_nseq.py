#!/usr/bin/env python3
import sys
import re

filename_fa = sys.argv[1]
filename_base = re.sub(r'.[A-z]*fa[sta]*', '', filename_fa)

seq_list = dict()
seq_h = ''

f_seq = open(filename_fa, 'r')
for line in f_seq:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>')
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_seq.close()

seq_map = dict()
for tmp_h in seq_list.keys():
    tmp_seq = ''.join(seq_list[tmp_h])
    if tmp_seq not in seq_map:
        seq_map[tmp_seq] = []
    seq_map[tmp_seq].append(tmp_h)

count_unique = 0
count_multi = 0

rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}


def revcomp(tmp_seq):
    # Assign 'N' for nucleotide other than A,T,G,C
    return ''.join(rc[x] for x in re.sub(r'[^ATGC]', 'N', tmp_seq)[::-1])


exc_list = dict()
f_nr = open('%s_NR.fa' % filename_base, 'w')
f_nr_log = open('%s_NR.log' % filename_base, 'w')
for tmp_seq in seq_map.keys():
    tmp_rc_seq = revcomp(tmp_seq)
    tmp_h_list = seq_map[tmp_seq]
    if tmp_rc_seq in seq_map:
        tmp_h_list += seq_map[tmp_rc_seq]
        exc_list[tmp_rc_seq] = 1

    if tmp_seq in exc_list:
        continue

    tmp_h = sorted(tmp_h_list)[0]
    tmp_count = len(tmp_h_list)
    f_nr.write('>%s %d\n%s\n' % (tmp_h, tmp_count, tmp_seq))
    if len(tmp_h_list) > 1:
        f_nr_log.write('%s <- %s\n' % (tmp_h, ';'.join(tmp_h_list)))
        count_multi += 1
    else:
        count_unique += 1

f_nr_log.write('#total seq: %d\n' % len(seq_list))
f_nr_log.write('#total nr seq: %d\n' % len(seq_map))
f_nr_log.write('#unique seq: %d, redundant seq:%d\n' %
               (count_unique, count_multi))
f_nr_log.close()
f_nr.close()
