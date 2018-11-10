#!/usr/bin/env python3
import os
import sys
import re
import gzip

len_adapter_N5 = 51
len_adapter_N7 = 47

usage_mesg = 'Usage: %s <filename_psl> <filenmae_src_fa>' % (__file__)

is_error = -1
if len(sys.argv) != 3:
    is_error = 1
    sys.stderr.write('Argument Error (%d).\n' % len(sys.argv))
    sys.stderr.write(usage_mesg + "\n")
    sys.exit(1)

# A PSL file mapped on ILMN adapter sequences
filename_psl = sys.argv[1]

# A FASTA file for mapping
filename_fa = sys.argv[2]
filename_base = re.sub(r'.(fa|fasta|fa.gz|fasta.gz)$', '', filename_fa)

if not os.access(filename_psl, os.R_OK) or not os.access(filename_fa, os.R_OK):
    sys.stderr.write('Not available.\n')
    sys.stderr.write(usage_mesg + "\n")
    sys.exit(1)

adapter_list = dict()
f_psl = open(filename_psl, 'r')
if filename_psl.endswith('.gz'):
    f_psl = gzip.open(filename_psl, 'rt')

for line in f_psl:
    tokens = line.strip().split("\t")
    if len(tokens) < 20:
        continue
    if tokens[8] not in ['+', '-']:
        continue

    match_len = int(tokens[0])
    seq_id = tokens[9]
    seq_start = int(tokens[11].split(',')[0])
    seq_end = int(tokens[12].split(',')[0])
    barcode_id = tokens[13]

    if seq_id not in adapter_list:
        adapter_list[seq_id] = dict()
    if seq_start not in adapter_list[seq_id]:
        adapter_list[seq_id][seq_start] = dict()
    adapter_list[seq_id][seq_start][barcode_id] = match_len
f_psl.close()

count_others = 0
count_N5_single = 0
count_N7_single = 0
count_pair = 0

amplicon_idx = 1
amplicon_list = dict()
for seq_id in adapter_list.keys():
    tmp_pos_list = sorted(adapter_list[seq_id].keys())
    if len(tmp_pos_list) == 1:
        tmp_pos = tmp_pos_list[0]
        tmp_bc = list(adapter_list[seq_id][tmp_pos].keys())[0]

        if tmp_bc.startswith('Nextera_N5'):
            count_N5_single += 1
        if tmp_bc.startswith('Nextera_N7'):
            count_N7_single += 1

    elif len(tmp_pos_list) == 2:
        tmp_pos1 = tmp_pos_list[0]
        tmp_pos2 = tmp_pos_list[1]
        tmp_adapter1 = adapter_list[seq_id][tmp_pos1]
        tmp_adapter2 = adapter_list[seq_id][tmp_pos2]
        tmp_bc1 = sorted(tmp_adapter1.keys(), key=tmp_adapter1.get)[-1]
        tmp_bc2 = sorted(tmp_adapter2.keys(), key=tmp_adapter2.get)[-1]
        if tmp_bc1.startswith('Nextera_N5') \
                and tmp_bc2.startswith('Nextera_N7'):
            tmp_h = 'S%08d-%s-%s' % (amplicon_idx, tmp_bc1, tmp_bc2)
            tmp_h = tmp_h.replace('Nextera_', '')
            amplicon_idx += 1
            amplicon_list[seq_id] = {'header': tmp_h,
                                     'start': tmp_pos1,
                                     'end': tmp_pos2}
            count_pair += 1
        else:
            count_others += 1
    else:
        count_others += 1

is_print = 0
tmp_h = ''
tmp_start = 0
tmp_end = 0
f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')

f_amplicon = open('%s.amplicons.fa' % filename_base, 'w')
f_N5 = open('%s.N5.fa' % filename_base, 'w')
f_N7 = open('%s.N7.fa' % filename_base, 'w')
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>').split()[0]
        if tmp_h in amplicon_list:
            is_print = 1
            f_amplicon.write(">%s" % amplicon_list[tmp_h]['header'] + "\n")
            f_N5.write(">%s" % amplicon_list[tmp_h]['header'] + "\n")
            f_N7.write(">%s" % amplicon_list[tmp_h]['header'] + "\n")
        else:
            is_print = 0
    elif is_print > 0:
            tmp_seq = line.strip()

            tmp_start = amplicon_list[tmp_h]['start']
            f_N5.write(tmp_seq[tmp_start:tmp_start+len_adapter_N5] + "\n")

            tmp_end = amplicon_list[tmp_h]['end']
            f_N7.write(tmp_seq[tmp_end:tmp_end+len_adapter_N7] + "\n")

            tmp_start = amplicon_list[tmp_h]['start'] + len_adapter_N5
            f_amplicon.write(tmp_seq[tmp_start:tmp_end] + "\n")
f_N5.close()
f_N7.close()
f_amplicon.close()

print("Paired = %d" % count_pair)
print("SingleN7 = %d, SingleN5 = %d" % (count_N7_single, count_N5_single))
print("Other = %d" % count_others)

