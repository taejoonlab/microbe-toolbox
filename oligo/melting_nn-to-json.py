#!/usr/bin/env python3
import sys
import json

# Convert NN (Nearest-Neighbor) files from melting-4
# Original files under src/NNFILES/ directory have encoding issue,
# so copy & paste the data to new file before running this script.

filename_nn = sys.argv[1]

out_json = {'ref': '', 'deltaH': {}, 'deltaS': {}}

f_nn = open(filename_nn, 'r')
for line in f_nn:
    if line.startswith('/*'):
        continue

    if line.startswith("REF:"):
        out_json['ref'] = line.strip().lstrip('REF:')
        continue

    tokens = line.strip().split()
    if len(tokens) == 0:
        continue

    tmp_nn = tokens[0]
    if float(tokens[1]) == 99999.0:
        continue
    out_json['deltaH'][tmp_nn] = float(tokens[1])
    out_json['deltaS'][tmp_nn] = float(tokens[2])
f_nn.close()

print(json.dumps(out_json, sort_keys=True, indent=4))
