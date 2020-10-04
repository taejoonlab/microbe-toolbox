#!/usr/bin/env python3
import sys

seq_list = dict()
f_cons = open('GTDB_r89.GENUS_cons.fa', 'r')
for line in f_cons:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        seq_list[tmp_h] = ''
    else:
        seq_list[tmp_h] += line.strip()
f_cons.close()

p_files = dict()
c_files = dict()
o_files = dict()
f_files = dict()
#d__Bacteria;p__Acidobacteriota;c__Acidobacteriae;o__2-12-FULL-54-10;f__2-12-FULL-54-10;g__2-02-FULL-61-28;s__2-02-FULL-61-28
f_list = open('bac120_taxonomy_r89.list', 'r')
for line in f_list:
    tmp_phylum = ''
    tmp_class = ''
    tmp_ofder = ''
    tmp_family = ''
    tmp_genus = ''

    tokens = line.strip().split(";")
    for tmp in tokens:
        if tmp.startswith('p__'):
            tmp_phylum = tmp.replace('p__', '').split('_')[0]
        elif tmp.startswith('c__'):
            tmp_class = tmp.replace('c__', '')
        elif tmp.startswith('o__'):
            tmp_order = tmp.replace('o__', '')
        elif tmp.startswith('f__'):
            tmp_family = tmp.replace('f__', '')
        elif tmp.startswith('g__'):
            tmp_genus = tmp.replace('g__', '')
        
    #print(tmp_genus, tmp_family, tmp_order, tmp_class, tmp_phylum)
    #print(tmp_phylum)

    tmp_genus_id = '%s_GENUS.cons' % tmp_genus
    if tmp_genus_id in seq_list:
        if tmp_phylum not in p_files:
            p_files[tmp_phylum] = []
        p_files[tmp_phylum].append(">%s\n%s\n" % (tmp_genus_id, seq_list[tmp_genus_id]))
        
        if tmp_class not in c_files:
            c_files[tmp_class] = []
        c_files[tmp_class].append(">%s\n%s\n" % (tmp_genus_id, seq_list[tmp_genus_id]))
        
        if tmp_order not in o_files:
            o_files[tmp_order] = []
        o_files[tmp_order].append(">%s\n%s\n" % (tmp_genus_id, seq_list[tmp_genus_id]))
        
        if tmp_family not in f_files:
            f_files[tmp_family] = []
        f_files[tmp_family].append(">%s\n%s\n" % (tmp_genus_id, seq_list[tmp_genus_id]))
f_list.close()

f_others = open('GTDB_r89.p_OTHERS.fa', 'w')
for tmp_id, tmp_list in p_files.items():
    if len(tmp_list) > 1:
        f = open('GTDB_r89.p_%s.fa' % tmp_id, 'w')
        for tmp in tmp_list:
            f.write("%s" % tmp)
        f.close()
    else:
        for tmp in tmp_list:
            f_others.write("%s" % tmp)
f_others.close()
