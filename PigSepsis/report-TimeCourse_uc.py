#!/usr/bin/env python3
import sys

filename_uc = sys.argv[1]
filename_out = '%s_report.txt' % filename_uc

clusters = dict()
f_uc = open(filename_uc, 'r')
for line in f_uc:
    tokens = line.strip().split("\t")
    tmp_id = tokens[8]
    seed_id = tokens[9]
    if tokens[0] == 'H':
        if seed_id not in clusters:
            clusters[seed_id] = []
        clusters[seed_id].append(tmp_id)
f_uc.close()

def parse_header(tmp_str):
    tmp_tokens = tmp_str.split('|')
    if len(tmp_tokens) != 4:
        return {'count': 0, 'genus': 'Unknown', 'genus_score': 0, 'sample': 'Unknown'}
    tmp_count = int(tmp_tokens[1].split('_')[0])
    tmp_genus = tmp_tokens[3].split('=')[1].split(':')[0]
    tmp_genus_score = float(tmp_tokens[3].split(':')[1])
    tmp_sample = tmp_tokens[0].split('.')[0].split('+')[1]
    rv = {'count': tmp_count, 'genus': tmp_genus, 'genus_score': tmp_genus_score, 'sample': tmp_sample}
    return rv

sample_list = ['feces', 'T00', 'T02', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10', 'T11', 'T12']
#sample_list = ['T00', 'T02', 'T04', 'T05', 'T06', 'T07', 'T08', 'T09', 'T10', 'T11', 'T12']

freq_list = dict()
freq_sum_list = dict()
for tmp_s in sample_list:
    freq_sum_list[tmp_s] = 0

for tmp_s_id in clusters.keys():
    tmp_s_header = parse_header(tmp_s_id)
    tmp_s_count = tmp_s_header['count']
    tmp_s_genus = tmp_s_header['genus']
    tmp_s_score = tmp_s_header['genus_score']
    tmp_s_sample = tmp_s_header['sample']
    #if tmp_s_score < 0.8:
    #    continue
    
    tmp_good_count = tmp_s_count
    tmp_bad_count = 0
    tmp_sample_freq = dict()
    for tmp_s in sample_list:
        tmp_sample_freq[tmp_s] = 0
    tmp_sample_freq[tmp_s_sample] += tmp_s_count

    for tmp_h_id in clusters[tmp_s_id]:
        tmp_h_header = parse_header(tmp_h_id)
        tmp_h_count = tmp_h_header['count']
        tmp_h_genus = tmp_h_header['genus']
        tmp_h_score = tmp_h_header['genus_score']
        tmp_h_sample = tmp_h_header['sample']
        if tmp_h_score < 0.8:
            continue

        if tmp_h_genus == tmp_s_genus:
            tmp_good_count += tmp_h_count
            tmp_sample_freq[tmp_h_sample] += tmp_h_count
        else:
            tmp_bad_count += tmp_h_count
    
    tmp_count = tmp_good_count + tmp_bad_count

    tmp_bad_ratio = tmp_bad_count*1.0/tmp_count
    if tmp_bad_ratio > 0.05:
        continue
    
    for tmp_s in sample_list:
        freq_sum_list[tmp_s] += tmp_sample_freq[tmp_s]

    freq_list[tmp_s_id] = {'genus': tmp_s_genus, 'freq': tmp_sample_freq}
    #tmp_sample_freq_str = '\t'.join(['%d'%tmp_sample_freq[x] for x in sample_list])
    #print("%s\t%s\t%s" % (tmp_s_genus, tmp_sample_freq_str, tmp_s_id))

#print(freq_sum_list)

## single read for all samples
ppm_cutoff = sum([1000000.0/freq_sum_list[x] for x in sample_list])

sys.stderr.write('Write %s\n' % filename_out)

f_out = open(filename_out, 'w')
#f_out.write('#PPM cutoff: %.2f\n' % ppm_cutoff)
total_count_str = '\t'.join(['%s=%d'%(x, freq_sum_list[x]) for x in sample_list])
#f_out.write('#TotalCount: %s\n' % total_count_str)
#f_out.write('#Genus\t%s\tSeedID\n' % ('\t'.join(['ppm.%s'%x for x in sample_list])))
f_out.write('Genus\t%s\n' % ('\t'.join(['ppm.%s'%x for x in sample_list])))
genus_count = dict()
for tmp_s_id in sorted(freq_list.keys()):
    tmp_freq = freq_list[tmp_s_id]['freq']
    tmp_genus = freq_list[tmp_s_id]['genus']
    tmp_ppm_freq_list = [int(tmp_freq[x]*1000000.0/freq_sum_list[x]) for x in sample_list]
    
    sum_ppm_freq = sum(tmp_ppm_freq_list)
    if sum_ppm_freq < ppm_cutoff:
        continue
    
    if tmp_genus not in genus_count:
        genus_count[tmp_genus] = 1
    else:
        genus_count[tmp_genus] += 1

    tmp_freq_str = "\t".join(['%d'%x for x in tmp_ppm_freq_list])
    tmp_genus_str = '%s_%03d' % (tmp_genus, genus_count[tmp_genus])
    #f_out.write('%s\t%s\t%s\n' % (tmp_genus, tmp_freq_str, tmp_s_id))
    f_out.write('%s\t%s\n' % (tmp_genus_str, tmp_freq_str))
f_out.close()
