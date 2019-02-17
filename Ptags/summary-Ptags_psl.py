#!/usr/bin/env python3
import sys
import gzip

filename_psl = sys.argv[1]
filename_out = filename_psl.replace('_psl','')+'_summary'

f_psl = open(filename_psl, 'r')
if filename_psl.endswith('.gz'):
    f_psl = gzip.open(filename_psl, 'rt')
    filename_out = filename_psl.replace('_psl.gz','')+'_summary'

q_list = dict()
for line in f_psl:
    tokens = line.strip().split("\t")
    if not tokens[0].isdigit():
        continue
    
    len_match = int(tokens[0])
    len_mismatch = int(tokens[1])
    count_q_gap = int(tokens[4])
    len_q_gap = int(tokens[5])
    count_t_gap = int(tokens[6])
    len_t_gap = int(tokens[7])

    q_id = tokens[9]
    q_len = int(tokens[10])
    t_id = tokens[13]
    t_len = int(tokens[14])
    
    if q_id not in q_list:
        q_list[q_id] = dict()
    q_list[q_id][t_id] = {'match':len_match, 'mismatch': len_mismatch, 'q_len':q_len}
f_psl.close()

#294	5	0	0	1	6	1	166	+	
#PigSepsis20181016_feces.00000004|38_39770	305	0	305	
#Escherichia-Shigella_MPGT01000001.4520103.4521658:343-807	465	0	465	
#2	150,149,	0,156,	0,316,

genus_count_list = dict()
for tmp_q in q_list.keys():
    match_len_list = [tmp_tv['match'] for tmp_tv in q_list[tmp_q].values()]
    best_match_len = sorted(match_len_list)[-1]

    t_genus_list = []
    for tmp_t in q_list[tmp_q].keys():
        if q_list[tmp_q][tmp_t]['match'] == best_match_len:
            t_genus_list.append(tmp_t.split('_')[0])
    
    tmp_q_count, tmp_total_count = tmp_q.split('|')[1].split('_')

    t_genus_str = '-'.join(sorted(list(set(t_genus_list))))
    if t_genus_str not in genus_count_list:
        genus_count_list[t_genus_str] = 0

    genus_count_list[t_genus_str] += int(tmp_q_count)

mapped_count = sum(genus_count_list.values())
sys.stderr.write('Write %s\n' % filename_out)
f_out = open(filename_out, 'w')
f_out.write("#Genus\tTotalCount\tMappedCount\tReadCount\tPercent\n")
for tmp_genus in sorted(genus_count_list.keys(), key=genus_count_list.get, reverse=True):
    #tmp_pct = genus_count_list[tmp_genus]*100.0/int(tmp_total_count)
    tmp_pct = genus_count_list[tmp_genus]*100.0/mapped_count

    f_out.write("%s\t%d\t%d\t%d\t%.3f\n" %\
        (tmp_genus, int(tmp_total_count), mapped_count, genus_count_list[tmp_genus], tmp_pct))
f_out.close()
