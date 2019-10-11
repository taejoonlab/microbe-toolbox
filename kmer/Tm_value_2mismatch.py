#!/usr/bin/env python2
import math
import sys
import os
import Tm_value_2mismatch_matrix

def salt_correction(Na=0, K=0, Tris=0, Mg=0, dNTPs=0, seq=None, seq_GC=0):
	corr = 0
	Mon = Na + K + Tris / 2.0  
	mg = Mg * 1e-3 
	mon = Mon * 1e-3

	a, b, c, d = 3.92, -0.911, 6.26, 1.42
	e, f, g = -48.2, 52.5, 8.31
	if dNTPs > 0:
		dntps = dNTPs * 1e-3
		ka = 3e4
		mg = (-(ka * dntps - ka * mg + 1.0) + math.sqrt((ka * dntps - ka * mg + 1.0) ** 2 + 4.0 * ka * mg)) / (2.0 * ka)
	if Mon > 0:
		R = math.sqrt(mg) / mon
		if R < 0.22:
			corr = (4.29 * seq_GC / 100 - 3.95) * 1e-5 * math.log(mon) + 9.40e-6 * math.log(mon) ** 2
			return corr
		elif R < 6.0:
			a = 3.92 * (0.843 - 0.352 * math.sqrt(mon) * math.log(mon))
			d = 1.42 * (1.279 - 4.03e-3 * math.log(mon) - 8.03e-3 * math.log(mon) ** 2)
			g = 8.31 * (0.486 - 0.258 * math.log(mon) + 5.25e-3 * math.log(mon) ** 3)
	corr = (a + b * math.log(mg) + (seq_GC / 100) * (c + d * math.log(mg)) + (1 / (2.0 * (len(seq) - 1))) * (e + f * math.log(mg) + g * math.log(mg) ** 2)) * 1e-5
	return corr

def tm_main(seq,c_seq):
	seq_GC = (seq.count('C')+seq.count('G'))*100.0/len(seq)
	tmp_seq = seq
	tmp_cseq = c_seq
	delta_h = 0
	delta_s = 0
	d_h = 0
	d_s = 1

	left_tmm = tmp_cseq[:2][::-1] + '/' + tmp_seq[:2][::-1]
	if left_tmm in Tm_value_2mismatch_matrix.tmm_table:
		delta_h += Tm_value_2mismatch_matrix.tmm_table[left_tmm][d_h]
		delta_s += Tm_value_2mismatch_matrix.tmm_table[left_tmm][d_s]
		tmp_seq = tmp_seq[1:]
		tmp_cseq = tmp_cseq[1:]
	right_tmm = tmp_seq[-2:] + '/' + tmp_cseq[-2:]
	if right_tmm in Tm_value_2mismatch_matrix.tmm_table:
		delta_h += Tm_value_2mismatch_matrix.tmm_table[right_tmm][d_h]
		delta_s += Tm_value_2mismatch_matrix.tmm_table[right_tmm][d_s]
		tmp_seq = tmp_seq[:-1]
		tmp_cseq = tmp_cseq[:-1]

	delta_h += nn_table['init'][d_h]
	delta_s += nn_table['init'][d_s]

	if not seq_GC == 0:
		delta_h += nn_table['init_oneG/C'][d_h]
		delta_s += nn_table['init_oneG/C'][d_s]
	else:		
		delta_h += nn_table['init_allA/T'][d_h]
		delta_s += nn_table['init_allA/T'][d_s]

	if seq.startswith('T'):
		delta_h += nn_table['init_5T/A'][d_h]
		delta_s += nn_table['init_5T/A'][d_s]
	if seq.endswith('A'):
		delta_h += nn_table['init_5T/A'][d_h]
		delta_s += nn_table['init_5T/A'][d_s]

	ends = seq[0] + seq[-1]
	AT = ends.count('A') + ends.count('T')
	GC = ends.count('G') + ends.count('C')
	delta_h += nn_table['init_A/T'][d_h] * AT
	delta_s += nn_table['init_A/T'][d_s] * AT
	delta_h += nn_table['init_G/C'][d_h] * GC
	delta_s += nn_table['init_G/C'][d_s] * GC

	#interal mismatch
	for basenumber in range(len(tmp_seq) - 1):
		neighbors = tmp_seq[basenumber:basenumber + 2] + '/' + tmp_cseq[basenumber:basenumber + 2]
		if neighbors in Tm_value_2mismatch_matrix.imm_table:
			delta_h += Tm_value_2mismatch_matrix.imm_table[neighbors][d_h]
			delta_s += Tm_value_2mismatch_matrix.imm_table[neighbors][d_s]
		elif neighbors[::-1] in Tm_value_2mismatch_matrix.imm_table:
			delta_h += Tm_value_2mismatch_matrix.imm_table[neighbors[::-1]][d_h]
			delta_s += Tm_value_2mismatch_matrix.imm_table[neighbors[::-1]][d_s]
		elif neighbors in nn_table:
			delta_h += nn_table[neighbors][d_h]
			delta_s += nn_table[neighbors][d_s]
		elif neighbors[::-1] in nn_table:
			delta_h += nn_table[neighbors[::-1]][d_h]
			delta_s += nn_table[neighbors[::-1]][d_s]

	k = (dnac1 - (dnac2 / 2.0)) * 1e-9
	R = 1.987
	melting_temp = (1000 * delta_h) / (delta_s + (R * (math.log(k)))) - 273.15

	corr = salt_correction(Na=int(Na), K=int(K), Tris=int(Tris), Mg=int(Mg), dNTPs=int(dNTPs), seq=seq, seq_GC = seq_GC)
	# Tm = 1/(1/Tm + corr)
	melting_temp = (1 / (1 / (melting_temp + 273.15) + corr) - 273.15)

	return melting_temp

seq = str(raw_input('Sequence : '))
table_name = str(raw_input('Thermodynamic lookup tables (DNA1,DNA2,DNA3,DNA4, RNA1,RNA2,RNA3, RNA_DNA1) default DNA4 : ') or 'DNA4')	#DNA4
dnac2 = int(raw_input('Concentration of 16S rRNA in bacteria[nM] default 137.8 : ') or 137.8)	#137.8
dnac1 = int(raw_input('Concentration of Probe[nM] default 500 : ') or 500) #500
Na = int(raw_input('Concentration of Na[mM] default 600 : ') or 600) #600
K = int(raw_input('Concentration of K[mM] default 0: ') or 0) #0
Tris = int(raw_input('Concentration of Tris[mM] default 0: ') or 0) #0
Mg = int(raw_input('Concentration of Mg[mM] default 0: ') or 0) #0
dNTPs = int(raw_input('Concentration of dNTPs[mM] default 0: ') or 0) #0

exec("%s = %s" % ('nn_table','Tm_value_2mismatch_matrix.'+table_name))
tm_list = list()
c_seq = seq.replace('G','c').replace('C','g').replace('A','t').replace('T','a').upper()
perfect = tm_main(seq,c_seq)
NA = ['A','T','G','C']
for f_i in range(1,len(seq)-2):
	for NA_n in NA:
		tmp_seq = c_seq[:f_i]+NA_n+c_seq[f_i+1:]
		for f_s in range(f_i+1,len(seq)):
			input_seq = tmp_seq[:f_s]+NA_n+tmp_seq[f_s+1:]
			melting_temp = tm_main(seq,input_seq)
			tm_list.append(melting_temp)

print 'Perfect match: '+str(perfect)+'\n'+'Tm interval : '+str(min(tm_list))+' to '+str(max(tm_list))
