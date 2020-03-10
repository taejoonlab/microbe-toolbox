#!/usr/bin/env python3
import os
import hyb_models as hyb

# For single caclulation
# tmp_oligo = 'AACGGACGAGAAGCT'
# tmp_c_oligo = complement(tmp_oligo)
# rv_tm = calc_Tm(seq=tmp_oligo, c_seq=tmp_c_oligo)
# print("%s\t%.2f" % (tmp_oligo, rv_tm))


filename_test = os.path.join(os.path.dirname(__file__), 'test.oligo')
with open(filename_test, 'r') as f_list:
    print("SeqID\tOligoSeq\tIDT_Tm\tCalcTm\tCalcPNATm")
    for line in f_list:
        if line.startswith('#'):
            continue
        tokens = line.strip().split()
        tmp_seq = tokens[1]
        tmp_c_seq = hyb.complement(tmp_seq)
        tmp_Tm = hyb.calc_Tm(seq=tmp_seq, c_seq=tmp_c_seq)
        tmp_PnaTm = hyb.adjust_Tm_DnaPna(tmp_Tm, tmp_seq)
        print("%s\t%s\t%.2f\t%.2f\t%.2f" %
              (tokens[0], tmp_seq, float(tokens[2]), tmp_Tm, tmp_PnaTm))
