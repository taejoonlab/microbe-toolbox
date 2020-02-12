#!/usr/bin/env python3
import sys

filename_fa = sys.argv[1]

f_fa = open(filename_fa, 'r')

is_print = -1
f_log = open('%s.log' % filename_fa, 'w')
for line in f_fa:
    if line.startswith('>'):
        tokens = line.strip().lstrip('>').split()
        new_h = '>%s_%s|%s' % (tokens[1], tokens[2], tokens[0])
        new_h = new_h.replace("'", '*')
        if new_h.find('*') >= 0:
            is_print = -1
            f_log.write('%s\n' % (new_h))
        else:
            is_print = 1
            print(new_h)
    else:
        tmp_line = line.strip()
        if tmp_line == '':
            continue
        if is_print < 0:
            f_log.write('%s\n' % tmp_line)
        else:
            print(tmp_line)
f_fa.close()
f_log.close()
