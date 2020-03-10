import json
import math
import os


def adjust_Tm_DnaPna(tmp_Tm, tmp_PNA_oligo):
    # Regression coefficients from Giesen, et al., (1998)
    c0 = 20.79
    c1 = 0.83
    c2 = -26.13
    c3 = 0.44

    tmp_length = len(tmp_PNA_oligo)
    tmp_oligo_upper = tmp_PNA_oligo.upper()
    tmp_pyrimidine = tmp_oligo_upper.count('C') + tmp_oligo_upper.count('T')

    return c0 + c1*tmp_Tm + c2*tmp_pyrimidine/tmp_length + c3*tmp_length


def complement(tmp_seq):
    rc = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join([rc[x] for x in tmp_seq])


def get_nn_param(hyb_type='DnaDna'):
    filename_param = os.path.join(os.path.dirname(__file__),
                                  '%s.json' % hyb_type)
    with open(filename_param, 'r') as f_param:
        nn_param = json.loads(f_param.read())
    return nn_param


def nn_list(tmp_oligo, tmp_c_oligo):
    rv = []
    for i in range(0, len(tmp_oligo)-1):
        tmp_nn1 = tmp_oligo[i:i+2]
        tmp_c_nn1 = tmp_c_oligo[i:i+2]
        tmp_nn = '%s/%s' % (tmp_nn1, tmp_c_nn1)
        rv.append(tmp_nn)
    return rv


# Salt correction
def salt_corr_factor(salt_conc=50, pct_GC=50):
    salt_conc = salt_conc * 1e-3
    salt_corr = (4.29 * pct_GC / 100 - 3.95) * 1e-5 * math.log(salt_conc)
    salt_corr += 9.40e-6 * math.log(salt_conc) ** 2
    return salt_corr


# salt_conc: mM
# dna_conc: nM
def calc_Tm(seq='', c_seq='', hyb_type='DnaDna', salt_conc=50, dna_conc=250):
    if len(seq) == 0:
        return -1

    nn_param = get_nn_param(hyb_type)
    tmp_oligo_GC = (seq.count('G') + seq.count('C'))
    tmp_oligo_GCpct = tmp_oligo_GC * 100.0 / len(seq)

    sum_deltaH = 200.0
    sum_deltaS = -5.7

    # Terminal AT penalty
    if seq[0] in ['A', 'T']:
        sum_deltaH += 2200
        sum_deltaS += 6.9

    if seq[-1] in ['A', 'T']:
        sum_deltaH += 2200
        sum_deltaS += 6.9

    for tmp_nn in nn_list(seq, c_seq):
        if tmp_nn in nn_param['deltaH']:
            sum_deltaH += nn_param['deltaH'][tmp_nn]
            sum_deltaS += nn_param['deltaS'][tmp_nn]

    Ct = ((dna_conc + dna_conc) / 4) * 1e-9
    const_R = 1.987
    tm_raw = sum_deltaH / (sum_deltaS + const_R * math.log(Ct)) - 273.15

    tmp_salt_corr = salt_corr_factor(salt_conc, tmp_oligo_GCpct)
    tm_corr = (1 / (1 / (tm_raw + 273.15) + tmp_salt_corr) - 273.15)
    return tm_corr
