#!/usr/bin/env python3
import sys

filename_fasta = sys.argv[1]
filename_ipcress_out = sys.argv[2]

seq_list = dict()
f_fa = open(filename_fasta, 'r')
for line in f_fa:
    if line.startswith('>'):
        seq_h = line.strip().lstrip('>').split()[0]
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append(line.strip())
f_fa.close()


def revcomp(tmp_seq):
    rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    return ''.join([rc[x] for x in tmp_seq[::-1]])


f_ipcress_out = open(filename_ipcress_out, 'r')
for line in f_ipcress_out:
    if not line.startswith('ipcress:'):
        continue
    tokens = line.strip().split()
    seq_id = tokens[1].split(':filter')[0]
    amp_len = int(tokens[3])
    start_pos = int(tokens[5])
    end_pos = int(tokens[8])
    seq_dir = tokens[10]

    if seq_id not in seq_list:
        sys.stderr.write('Not available. %s\n' % seq_id)
        continue

    tmp_seq = ''.join(seq_list[seq_id])
    tmp_amplicon = tmp_seq[start_pos-1:start_pos+amp_len].upper()
    if len(set(tmp_amplicon)) > 4:
        sys.stderr.write('Error: %s\n' % seq_id)
        continue

    if seq_dir == 'revcomp':
        tmp_amplicon = revcomp(tmp_amplicon)

    tmp_h = '%s:%d-%d' % (seq_id, start_pos, start_pos+amp_len)
    print(">%s\n%s" % (tmp_h, tmp_amplicon))
f_ipcress_out.close()
