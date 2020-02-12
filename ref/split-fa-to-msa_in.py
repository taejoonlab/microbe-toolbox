#!/usr/bin/env python3
import os
import sys

filename_fa = 'GTDBr89_ssu_v3.fa'

filename_query = 'query_species.list'

dir_name = 'msa'

f_query = open(filename_query, 'r')
for q_species in f_query:
    q_species = q_species.strip()
    q_genus = q_species.split('_')[0]

    is_genus_print = 0
    is_species_print = 0

    skip_genus = -1
    skip_species = -1

    filename_genus = '%s/%s_GENUS.msa_in.fa' % (dir_name, q_genus)
    if os.access(filename_genus, os.R_OK):
        sys.stderr.write('%s exists. Skip.\n' % filename_genus)
        skip_genus = 1
    else:
        sys.stderr.write('Write %s\n' % filename_genus)
        f_genus = open(filename_genus, 'w')

    filename_species = '%s/%s.msa_in.fa' % (dir_name, q_species)
    if os.access(filename_species, os.R_OK):
        sys.stderr.write('%s exists. Skip.\n' % filename_species)
        is_species = 1
    else:
        sys.stderr.write('Write %s\n' % filename_species)
        f_species = open(filename_species, 'w')

    f_fa = open(filename_fa, 'r')
    for line in f_fa:
        if line.startswith('>'):
            tmp_species = line.strip().lstrip('>').split('|')[0]
            tmp_genus = tmp_species.split('_')[0]

            if tmp_species == q_species:
                is_species_print = 1
                if skip_species < 0:
                    f_species.write('%s\n' % line.strip())
                if skip_genus < 0:
                    f_genus.write('%s\n' % line.strip())

            elif tmp_genus == q_genus:
                is_genus_print = 1
                is_species_print = 0
                if skip_genus < 0:
                    f_genus.write('%s\n' % line.strip())

            else:
                is_species_print = 0
                is_genus_print = 0

        elif is_species_print > 0:
            if skip_species < 0:
                f_species.write('%s\n' % line.strip())
            if skip_genus < 0:
                f_genus.write('%s\n' % line.strip())

        elif is_genus_print > 0:
            if skip_genus < 0:
                f_genus.write('%s\n' % line.strip())
    f_fa.close()