#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')

import sys
import pandas as pd
import numpy as np
import skbio.diversity as sd

print(sd.get_alpha_diversity_metrics())
print(sd.get_beta_diversity_metrics())

filename_summary = sys.argv[1]
data_name = filename_summary.split('.')[0]
summary_tbl = pd.read_csv(filename_summary, sep='\t', index_col=0, header=0).transpose()

alpha_div = sd.alpha_diversity('observed_otus', summary_tbl.values, summary_tbl.index)
print(list(alpha_div))

idx_list = summary_tbl.index
beta_div = sd.beta_diversity('braycurtis', summary_tbl.values, summary_tbl.index)
print(beta_div)
beta_div_list = []
for i in range(0,len(summary_tbl.index)-1):
    print(idx_list[i], idx_list[i+1], beta_div[i+1,i])
    beta_div_list.append(beta_div[i+1, i])


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(12,6))

x_list = summary_tbl.index

ax1 = fig.add_subplot(1,2,1)
ax1.bar(range(0,len(x_list)), list(alpha_div))
ax1.set_xticks(range(0,len(x_list)))
ax1.set_xticklabels(x_list)
ax1.set_ylabel('Alpha Diversity (observed_otus)')
ax1.set_title(data_name)

ax2 = fig.add_subplot(1,2,2)
ax2.bar(range(1,len(x_list)-1), list(beta_div_list)[:-1])
ax2.set_xticks([x+0.5 for x in range(0,len(x_list)-1)])
ax2.set_xticklabels(x_list[:-1])
ax2.set_ylabel('Beta Diversity (Bray-Curtis)')

plt.savefig('%s.diversity.pdf' % data_name)
#plt.show()
