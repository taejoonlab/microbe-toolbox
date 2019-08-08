#!/usr/bin/env python3
import sys
import os
import gzip

filename_tbl = 'NCBI_RefSeq.prok_genomes.2019_08.tsv'

f_tbl = open(filename_tbl, 'r')
for line in f_tbl:
    if line.startswith('#'):
        continue

    tokens = line.strip().split("\t")
    sp_name = "_".join(tokens[0].split()[:2])
    path_refseq = tokens[-1].replace('ftp://','')
    tmp_genome_id = os.path.basename(path_refseq)
    for tmp_filename in os.listdir(path_refseq):
        if tmp_filename.find('rna_from_genomic.fna.gz') >= 0:
            f_fa = gzip.open(os.path.join(path_refseq, tmp_filename), 'rt')
            for line in f_fa:
                if line.startswith('>'):
                    tmp_h = line.strip().lstrip('>')
                    if tmp_h.find('16S') >= 0:
                        tmp_locus = 'unknown'
                        for tmp in tmp_h.split():
                            if tmp.startswith('[locus_tag'):
                                tmp_locus = tmp.split('=')[1].rstrip(']')
                        print(">%s|%s %s" % (tmp_locus, sp_name, tmp_genome_id))
                        is_print = 1
                    else:
                        is_print = 0
                elif is_print > 0:
                    print(line.strip())
            f_fa.close()

f_tbl.close()
