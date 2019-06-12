#!/usr/bin/env python3
import sys
import numpy as np

filename_txt = sys.argv[1]
sample_name = filename_txt.split('_')[1]

#sample_list = ['feces','T00','T02','T04','T05','T06','T07','T08','T09','T10','T11','T12']
sample_list = ['T00','T02','T04','T05','T06','T07','T08','T09','T10','T11','T12']

ppm_feces_list = []
ppm_T0_list = []
ppm_other_list = []
ppm_total_list = []

ppm_EC_feces_list = []
ppm_EC_T0_list = []
ppm_EC_other_list = []
ppm_EC_total_list = []

sum_feces = 0
f_txt = open(filename_txt, 'r')
for line in f_txt:
    if line.startswith('#'):
        continue

    tokens = line.strip().split("\t")
    genus = tokens[0]

    ppm_list = [int(x) for x in tokens[1:-1]]
    ppm_sum = sum(ppm_list)
    ppm_feces = ppm_list[0]
    ppm_T0 = ppm_list[1]
    ppm_T2 = ppm_list[2]

    sum_feces += ppm_feces

    if len(ppm_total_list) == 0:
        ppm_total_list = [0 for x in ppm_list]
        ppm_EC_total_list = [0 for x in ppm_list]
    
    if ppm_feces > ppm_sum * 0.9:
        if len(ppm_feces_list) == 0:
            ppm_feces_list = ppm_list
            ppm_total_list = np.add(ppm_total_list, ppm_list)
        else:
            ppm_feces_list = np.add(ppm_feces_list, ppm_list)
            ppm_total_list = np.add(ppm_total_list, ppm_list)
    
    elif ppm_T0 > 0 or ppm_T2 > 0:
        if len(ppm_T0_list) == 0:
            ppm_T0_list = ppm_list
            ppm_total_list = np.add(ppm_total_list, ppm_list)
        else:
            ppm_T0_list = np.add(ppm_T0_list, ppm_list)
            ppm_total_list = np.add(ppm_total_list, ppm_list)
    
    else:
        if len(ppm_other_list) == 0:
            ppm_other_list = ppm_list
            ppm_total_list = np.add(ppm_total_list, ppm_list)
        else:
            ppm_other_list = np.add(ppm_other_list, ppm_list)
            ppm_total_list = np.add(ppm_total_list, ppm_list)
    
    if genus.find('Escherichia') >= 0:
        if ppm_feces > ppm_sum * 0.9:
            if len(ppm_EC_feces_list) == 0:
                ppm_EC_feces_list = ppm_list
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)
            else:
                ppm_EC_feces_list = np.add(ppm_EC_feces_list, ppm_list)
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)
        
        elif ppm_T0 > 0 or ppm_T2 > 0:
            if len(ppm_EC_T0_list) == 0:
                ppm_EC_T0_list = ppm_list
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)
            else:
                ppm_EC_T0_list = np.add(ppm_EC_T0_list, ppm_list)
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)
        
        else:
            if len(ppm_EC_other_list) == 0:
                ppm_EC_other_list = ppm_list
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)
            else:
                ppm_EC_other_list = np.add(ppm_EC_other_list, ppm_list)
                ppm_EC_total_list = np.add(ppm_EC_total_list, ppm_list)


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,6))
x_list = range(0, len(ppm_feces_list))

ax1 = fig.add_subplot(1,2,1)
ax1.plot(x_list, ppm_total_list, label='Total')
ax1.plot(x_list, ppm_T0_list, label='T0+T2')
ax1.plot(x_list, ppm_other_list, label='Other')
ax1.plot(x_list, ppm_feces_list, label='Feces')

ax1.set_xticks(x_list)
ax1.set_xticklabels(sample_list)
ax1.grid()
ax1.legend(ncol=2)
ax1.set_title('%s_total' % sample_name)

ax2 = fig.add_subplot(1,2,2)
ax2.plot(x_list, ppm_EC_total_list, label='Total')
ax2.plot(x_list, ppm_EC_T0_list, label='T0+T2')
ax2.plot(x_list, ppm_EC_other_list, label='Other')
if len(ppm_EC_feces_list) > 0:
    ax2.plot(x_list, ppm_EC_feces_list, label='Feces')

ax2.set_xticks(x_list)
ax2.set_xticklabels(sample_list)
ax2.grid()
ax2.legend(ncol=2)
ax2.set_title('%s_ECOLI' % sample_name)

plt.show()
#plt.savefig('%s.pdf' % sample_name)
