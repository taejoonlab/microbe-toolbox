#!/usr/bin/env python3
import sys
import gzip
import re

#filename_SILVA = 'SILVA_132_SSURef_tax_silva.U-to-T.fa.gz'
filename_SILVA_fa = sys.argv[1]
filename_base = filename_SILVA_fa.split('_tax_silva')[0]

f_annot = open('%s_v2.fa' % filename_base, 'w')
f_uncultured = open('%s_uncultured.fa' % filename_base, 'w')
f_not_prok = open('%s_not_prok.fa' % filename_base, 'w')
f_unknown = open('%s_unknown.fa' % filename_base, 'w')

seq_type = 'unknown'

f_silva = open(filename_SILVA_fa, 'r')
if filename_SILVA_fa.endswith('.gz'):
    f_silva = gzip.open(filename_SILVA_fa, 'rt')
for line in f_silva:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        (tmp_id, tmp_kingdom) = tmp_h.split(';')[0].split()
        tmp_genus = tmp_h.split(';')[-2].replace(' ', '_').replace('\'', '*')
        tmp_species = tmp_h.split(';')[-1].replace(' ', '_').replace('\'', '*')
        if tmp_species.find('_') > 1:
            tmp_species = '_'.join(tmp_species.split('_')[:2])

        if tmp_kingdom == 'Bacteria':
            if tmp_h.find('uncultured') >= 0 or tmp_h.find('metagenome') >= 0:
                f_uncultured.write('>%s\n' % tmp_h)
                seq_type = 'uncultured'

            elif len(re.findall('\d', tmp_genus)) > 0 \
                    or tmp_genus.startswith('Clade_') \
                    or tmp_genus.find('[') >= 0 \
                    or tmp_species == 'unidentified' \
                    or tmp_species == 'bacterium' \
                    or re.match(r'^[a-z]', tmp_genus):
                f_unknown.write('>%s\n' % tmp_h)
                seq_type = 'unknown'

            else:
                f_annot.write(">%s|%s\n" % (tmp_species, tmp_id))
                seq_type = 'annot'

        else:
            f_not_prok.write('>%s\n' % tmp_h)
            seq_type = 'no_prok'

    else:
        tmp_line = line.strip().upper().replace('U', 'T')
        if seq_type == 'annot':
            f_annot.write('%s\n' % tmp_line)
        elif seq_type == 'uncultured':
            f_uncultured.write('%s\n' % tmp_line)
        elif seq_type == 'unknown':
            f_unknown.write('%s\n' % tmp_line)
        elif seq_type == 'no_prok':
            f_not_prok.write('%s\n' % tmp_line)
        else:
            sys.stderr.write('Error: %s\n' % tmp_h)
f_silva.close()
