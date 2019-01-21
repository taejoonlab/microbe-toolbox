#!/usr/bin/env python3
import sys
import gzip

filename_mapseq = sys.argv[1]
filename_base = filename_mapseq.replace('.mapseq_out', '')

min_cf = 0

f_mapseq = open(filename_mapseq, 'r')
if filename_mapseq.endswith('.gz'):
    f_mapseq = gzip.open(filename_mapseq, 'rt')

h_version = f_mapseq.readline().strip()
h_tokens = f_mapseq.readline().strip().split("\t")

tax_list = ['Phylum', 'Class', 'Genus', 'Species']
idx_list = dict()
count_list = dict()
for tmp_tax in tax_list:
    idx_list[tmp_tax] = h_tokens.index(tmp_tax)
    count_list[tmp_tax] = {'low_cf': 0}

for line in f_mapseq:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    ptag_id = tokens[0]
    ptag_count = int(ptag_id.split('|')[1].split('_')[0])

    for tmp_tax in tax_list:
        tmp_name = tokens[idx_list[tmp_tax]].replace(' ', '_')
        tmp_cf = float(tokens[idx_list[tmp_tax]+1])

        if tmp_cf > min_cf:
            if tmp_name not in count_list[tmp_tax]:
                count_list[tmp_tax][tmp_name] = 0
            count_list[tmp_tax][tmp_name] += ptag_count
        else:
            count_list[tmp_tax]['low_cf'] += ptag_count
f_mapseq.close()


def report_count(tmp_filename, tmp_count):
    low_count = 0
    total_count = sum(tmp_count.values())

    f_out = open(tmp_filename, 'w')
    f_out.write('#tax: %s\n' % tmp_tax)
    f_out.write('#TaxName\tRawCount\tNormPCT\n')
    for tmp in sorted(tmp_count.keys(), key=tmp_count.get, reverse=True):
        if tmp == 'low_cf':
            continue

        tmp_pct = tmp_count[tmp]*100.0/total_count
        if tmp_pct < 0.5:
            low_count += tmp_count[tmp]
        else:
            f_out.write("%s\t%d\t%.2f\n" % (tmp, tmp_count[tmp], tmp_pct))

    f_out.write("LowCount\t%d\t%.2f\n" %
                (low_count, low_count*100.0/total_count))
    f_out.write("LowCF\t%d\t%.2f\n" %
                (tmp_count['low_cf'], tmp_count['low_cf']*100.0/total_count))
    f_out.close()


for tmp_tax in tax_list:
    filename_out = '%s.%s.mapseq_tax_tbl' % (filename_base, tmp_tax)
    report_count(filename_out, tmp_tax, count_list[tmp_tax])
