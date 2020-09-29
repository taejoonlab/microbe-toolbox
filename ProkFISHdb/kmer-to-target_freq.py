#!/usr/bin/env python3
import sys
import os

kmer_len = 20
max_mismatch = 2

dirname_kmer = 'kmer_SPECIES.GTDB_r89'
filename_out = '%d%s.target_freq' % (kmer_len, dirname_kmer)

kmer_freq = dict()
for tmp_filename in os.listdir(dirname_kmer):
    if not tmp_filename.endswith('%dmer' % kmer_len):
        continue

    sys.stderr.write('Read %s\n' % tmp_filename)
    tmp_genus = tmp_filename.split('.')[0]

    f = open(os.path.join(dirname_kmer, tmp_filename), 'r')
    for line in f:
        tokens = line.strip().split()
        tmp_oligo = tokens[0]
        if tmp_oligo not in kmer_freq:
            kmer_freq[tmp_oligo] = []
        kmer_freq[tmp_oligo].append(tmp_genus)
    f.close()

oligo_sorted = sorted(kmer_freq.keys())
oligo_matches = dict()
tmp_word_len = int(kmer_len / 4)
for i in range(0, len(oligo_sorted)):
    oligo_i = oligo_sorted[i]
    sys.stderr.write('Oligo %s\n' % oligo_i)

    for j in range(i+1, len(oligo_sorted)):
        oligo_j = oligo_sorted[j]
        count_mismatch = 0

        for k in range(0, kmer_len, tmp_word_len):
            if oligo_i[k:k+tmp_word_len] != oligo_j[k:k+tmp_word_len]:
                count_mismatch += 1

        if count_mismatch > max_mismatch:
            continue
        
        count_mismatch2 = 0
        for p in range(0, kmer_len):
            if oligo_i[p] != oligo_j[p]:
                count_mismatch2 += 1
            if count_mismatch2 > max_mismatch:
                count_mismatch2 = max_mismatch + 1
                break
        
        if count_mismatch2 <= max_mismatch :
            if oligo_i not in oligo_matches:
                oligo_matches[oligo_i] = dict()
            oligo_matches[oligo_i][oligo_j] = max_mismatch
            if oligo_j not in oligo_matches:
                oligo_matches[oligo_j] = dict()
            oligo_matches[oligo_j][oligo_i] = max_mismatch

f_out = open(filename_out, 'w')
for tmp_oligo in oligo_sorted:
    tmp_count = len(kmer_freq[tmp_oligo])
    tmp_list = ','.join(sorted((kmer_freq[tmp_oligo])))
    tmp_match_count = 0
    tmp_match_list = 'NA'
    if tmp_oligo in oligo_matches:
        tmp_match_count = len(oligo_matches[tmp_oligo].keys())
        tmp_match_list = ','.join(sorted(oligo_matches[tmp_oligo].keys()))
    f_out.write("%s\t%d\t%s\t%d\t%s\n" % (tmp_oligo, tmp_count, tmp_match_list, tmp_match_count, tmp_list))
f_out.close()
