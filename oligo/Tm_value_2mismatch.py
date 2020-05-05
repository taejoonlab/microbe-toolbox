#!/usr/bin/env python3
import os
import hyb_models as hyb

NA = ['A','T','G','C']
filename_test = os.path.join(os.path.dirname(__file__), 'test.oligo')
with open(filename_test, 'r') as f_list:
	print("#salt_conc=50, dna_conc=250")
	print("SeqID\tOligoSeq\tIDT_Tm\tCalcTm\tCalcPNATm\t1mismatch_MaxTm\t1mismatch_MaxPNATm\t2mismatch_MaxTm\t2mismatch_MaxPNATm")
	for line in f_list:
		if line.startswith('#'):
			continue
		tokens = line.strip().split()
		tmp_seq = tokens[1]
		tmp_c_seq = hyb.complement(tmp_seq)
		tmp_Tm = hyb.calc_Tm(seq=tmp_seq, c_seq=tmp_c_seq)
		tmp_PnaTm = hyb.adjust_Tm_DnaPna(tmp_Tm, tmp_seq)
		one_mismatch_MaxTm = 0
		one_mismatch_MaxPNATm = 0
		two_mismatch_MaxTm = 0
		two_mismatch_MaxPNATm = 0
		for first_mis in range(1,len(tmp_c_seq)-2):
			for NA_f in NA:
				one_mis_seq = tmp_c_seq[:first_mis]+NA_f+tmp_c_seq[first_mis+1:]
				if one_mis_seq == tmp_c_seq:
					continue
				one_mis_Tm = hyb.calc_Tm(seq=tmp_seq, c_seq=one_mis_seq)
				one_mis_PnaTm = hyb.adjust_Tm_DnaPna(one_mis_Tm, tmp_seq)
				if one_mis_Tm > one_mismatch_MaxTm:
						one_mismatch_MaxTm = one_mis_Tm
				if one_mis_PnaTm > one_mismatch_MaxPNATm:
						one_mismatch_MaxPNATm = one_mis_PnaTm
				for NA_s in NA:
					for second_mis in range(first_mis+2,len(tmp_c_seq)):
						two_mis_seq = one_mis_seq[:second_mis]+NA_s+one_mis_seq[second_mis+1:]
						if two_mis_seq == one_mis_seq:
							continue
						two_mis_Tm = hyb.calc_Tm(seq=tmp_seq, c_seq=two_mis_seq)
						two_mis_PnaTm = hyb.adjust_Tm_DnaPna(two_mis_Tm, tmp_seq)
						if two_mis_Tm > two_mismatch_MaxTm:
								two_mismatch_MaxTm = two_mis_Tm
						if two_mis_PnaTm > two_mismatch_MaxPNATm:
								two_mismatch_MaxPNATm = two_mis_PnaTm
		print("%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" %
              (tokens[0], tmp_seq, float(tokens[2]), tmp_Tm, tmp_PnaTm,
               one_mismatch_MaxTm,one_mismatch_MaxPNATm,two_mismatch_MaxTm,two_mismatch_MaxPNATm))
