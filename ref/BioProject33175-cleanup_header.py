#!/usr/bin/env python3
import sys

filename_fa = sys.argv[1]

f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        tokens = line.strip().split()
        new_h = '%s|%s_%s' % (tokens[0], tokens[1], tokens[2])
        new_h = new_h.replace("'", '*')
        print(new_h)
    else:
        print(line.strip())
f_fa.close()
