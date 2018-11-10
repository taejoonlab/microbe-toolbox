#!/usr/bin/env python3
import os
import sys

usage_mesg = 'Usage: %s <filename_psl> <filenmae_src_fa>' % (__file__)

is_error = -1
if len(sys.argv) != 2:
    is_error = 1
    sys.stderr.write('Argument Error.\n')
    sys.stderr.write(usage_mesg + "\n")
    sys.exit(1)

# A PSL file mapped on ILMN adapter sequences
filename_psl = sys.argv[1]

# A FASTA file for mapping
filename_fa = sys.argv[2]

if not os.access(filename_psl, os.R_OK) or not os.access(filename_fa, os.R_OK):
    sys.stderr.write('Not available.\n')
    sys.stderr.write(usage_mesg + "\n")
    sys.exit(1)

adapter_list = dict()
f_psl = open(filename_psl, 'r')
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
count_i5_single = 0
count_i7_single = 0
count_pair = 0

amplicon_idx = 1
amplicon_list = dict()
for seq_id in adapter_list.keys():
    tmp_pos_list = sorted(adapter_list[seq_id].keys())
    if len(tmp_pos_list) == 1:
        tmp_pos = tmp_pos_list[0]
        tmp_bc = list(adapter_list[seq_id][tmp_pos].keys())[0]

        if tmp_bc.startswith('Nextera_N5'):
            count_i5_single += 1
        if tmp_bc.startswith('Nextera_N7'):
            count_i7_single += 1

    elif len(tmp_pos_list) == 2:
        tmp_pos1 = tmp_pos_list[0]
        tmp_pos2 = tmp_pos_list[1]
        tmp_adapter1 = adapter_list[seq_id][tmp_pos1]
        tmp_adapter2 = adapter_list[seq_id][tmp_pos2]
        tmp_bc1 = sorted(tmp_adapter1.keys(), key=tmp_adapter1.get)[-1]
        tmp_bc2 = sorted(tmp_adapter2.keys(), key=tmp_adapter2.get)[-1]
        tmp_pos2 += 47
        if tmp_bc1.startswith('Nextera_N5') \
                and tmp_bc2.startswith('Nextera_N7'):
            tmp_h = '%s-%s-%08d' % (tmp_bc1, tmp_bc2, amplicon_idx)
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
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>').split()[0]
        if tmp_h in amplicon_list:
            is_print = 1
            print(">%s" % amplicon_list[tmp_h]['header'])
        else:
            is_print = 0
    elif is_print > 0:
            tmp_start = amplicon_list[tmp_h]['start']
            tmp_end = amplicon_list[tmp_h]['end']
            print(line.strip()[tmp_start:tmp_end])

print(count_pair, count_i7_single, count_i5_single, count_others)
