#!/usr/bin/env python3
import sys
import gzip

filename_fa = '88_otus.ILMN_V34.fa.gz'
filename_list = '88_otu_taxonomy.txt'

filename_annot_fa = '88_otus.ILMN_V34_annot.fa'
filename_missed_fa = '88_otus.ILMN_V34_missed.fa'

#370251	k__Bacteria; p__Proteobacteria; c__Gammaproteobacteria; o__Oceanospirillales; f__Endozoicimonaceae; g__Endozoicomonas; s__montiporae
#2562098	k__Bacteria; p__Firmicutes; c__Bacilli; o__Bacillales; f__Bacillaceae; g__Bacillus; s__foraminis
#370253	k__Bacteria; p__Firmicutes; c__Clostridia; o__Clostridiales; f__Ruminococcaceae; g__Faecalibacterium; s__prausnitzii

id2name = dict()
f_list = open(filename_list, 'r')
for line in f_list:
    tokens = line.strip().split()
    seq_id = tokens[0]
    tmp_g = tokens[-2].rstrip(';').lstrip('g__')
    tmp_s = tokens[-1].rstrip(';').lstrip('s__')
    if tmp_g == '' or tmp_s == '':
        continue
    sp_name = '%s_%s' % (tmp_g, tmp_s)
    id2name[seq_id] = sp_name
f_list.close()

f_fa = open(filename_fa, 'r')
if filename_fa.endswith('.gz'):
    f_fa = gzip.open(filename_fa, 'rt')

f_annot = open(filename_annot_fa, 'w')
f_missed = open(filename_missed_fa, 'w')

is_print = -1
for line in f_fa:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')

        tmp_tokens = tmp_h.split(':')
        tmp_id = tmp_tokens[0]
        tmp_pos_str = tmp_tokens[-1]
        tmp_id = tmp_id.replace('.gene','')

        if tmp_id in id2name:
            tmp_pos_list = [int(x) for x in tmp_pos_str.split('-')]
            tmp_len = tmp_pos_list[1] - tmp_pos_list[0]
            # print(">%s|%s %s" % (id2name[tmp_id], tmp_id, tmp_h))
            f_annot.write(">%s|len=%d|%s\n" % (id2name[tmp_id], tmp_len, tmp_id))
            is_print = 1
        else:
            f_missed.write('>%s\n' % tmp_h)
            is_print = -1
    else:
        if is_print > 0:
            f_annot.write('%s\n' % line.strip())
        else:
            f_missed.write('%s\n' % line.strip())
f_fa.close()

f_annot.close()
f_missed.close()
