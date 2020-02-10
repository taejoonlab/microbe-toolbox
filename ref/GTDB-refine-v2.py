#!/usr/bin/env python3
import sys
import gzip

# Input: fna files from GTDB
filename_fna = sys.argv[1]

seq_list = dict()
f_fna = open(filename_fna, 'r')
if filename_fna.endswith('.gz'):
    f_fna = gzip.open(filename_fna, 'rt')

for line in f_fna:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_id = tmp_h.split()[0]
        tmp_sp_name = tmp_h.split(';')[-1].split('[')[0].strip()
        tmp_sp_name = tmp_sp_name.replace('s__', '')
        tmp_sp_name = tmp_sp_name.replace(' ', '_')

        tmp_h = ">%s|%s" % (tmp_id, tmp_sp_name)
        seq_list[tmp_h] = []
    else:
        seq_list[tmp_h].append(line.strip())
f_fna.close()

# Set the sequence length criteria based on the mode.
mode_len = 1537
min_len = mode_len - 40
max_len = mode_len + 40

for tmp_h in sorted(seq_list.keys()):
    tmp_seq = ''.join(seq_list[tmp_h])

    if len(tmp_seq) < min_len:
        continue
    if len(tmp_seq) > max_len:
        continue

    print(">%s\n%s" % (tmp_h, tmp_seq))
