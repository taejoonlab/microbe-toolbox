#!/usr/bin/env python3
import sys
import gzip
import re

filename_SILVA = 'SILVA_132_SSURef_tax_silva.U-to-T.fa.gz'
filename_base = 'SILVA_132_SSURef'

f_annot = open('%s_annot.fa' % filename_base, 'w')
f_uncultured = open('%s_uncultured.fa' % filename_base, 'w')
f_not_prok = open('%s_not_prok.fa' % filename_base, 'w')
f_unknown = open('%s_unknown.fa' % filename_base, 'w')

seq_type = 'unknown'

f_silva = gzip.open(filename_SILVA, 'rt')
for line in f_silva:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        (tmp_id, tmp_kingdom) = tmp_h.split(';')[0].split()
        tmp_genus = tmp_h.split(';')[-2].replace(' ', '_')
        tmp_species = tmp_h.split(';')[-1].replace(' ', '_')

        if tmp_kingdom == 'Bacteria':
            if tmp_h.find('uncultured') >= 0 or tmp_h.find('metagenome') >= 0:
                f_uncultured.write('>%s\n' % tmp_h)
                seq_type = 'uncultured'

            elif len(re.findall('\d', tmp_genus)) > 0 \
                    or tmp_genus.startswith('Clade_') \
                    or tmp_genus.find('[') >= 0 \
                    or re.match(r'^[a-z]', tmp_genus):
                f_unknown.write('>%s\n' % tmp_h)
                seq_type = 'unknown'

            else:
                f_annot.write(">%s_%s %s\n" % (tmp_genus, tmp_id, tmp_species))
                seq_type = 'annot'

        else:
            f_not_prok.write('>%s\n' % tmp_h)
            seq_type = 'no_prok'

    else:
        if seq_type == 'annot':
            f_annot.write(line.strip() + "\n")
        elif seq_type == 'uncultured':
            f_uncultured.write(line.strip() + "\n")
        elif seq_type == 'unknown':
            f_unknown.write(line.strip() + "\n")
        elif seq_type == 'no_prok':
            f_not_prok.write(line.strip() + "\n")
        else:
            sys.stderr.write('Error: %s\n' % tmp_h)
f_silva.close()
