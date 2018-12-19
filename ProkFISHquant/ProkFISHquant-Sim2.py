#!/usr/bin/env python3
import random
import numpy as np

count_sampling = 100

total_cell_count_list = [1000, 5000, 10000, 50000, 100000]

upper_95ci_idx = int(count_sampling*0.95)
lower_95ci_idx = int(count_sampling*0.05)

for sp1_percent in [0.01, 0.05]:
#for sp1_percent in [0.1, 0.25, 0.5, 0.75, 0.9]:
    # sp1_percent = 0.1
    sp2_percent = 1.0 - sp1_percent

    for total_num_cells in total_cell_count_list:
        sp1_cell_narray = np.zeros(int(total_num_cells * sp1_percent))
        sp2_cell_narray = np.ones(int(total_num_cells * sp2_percent))
        cell_list = list(sp1_cell_narray) + list(sp2_cell_narray)

        random.shuffle(cell_list)

        range_cell_count = range(10, min(5000, total_num_cells), 10)

        tmp_count_good = 0
        for tmp_cell_count in range_cell_count:
            y_list = []
            for i in range(0, count_sampling):
                imaged_cell_list = random.sample(list(cell_list),
                                                 tmp_cell_count)
                tmp_sp1_percent = imaged_cell_list.count(0)/tmp_cell_count
                y_list.append(tmp_sp1_percent)

            y_list_sorted = sorted(y_list)
            tmp_upper_95ci = y_list_sorted[upper_95ci_idx]
            tmp_lower_95ci = y_list_sorted[lower_95ci_idx]
            tmp_95ci = tmp_upper_95ci - tmp_lower_95ci

            # print(total_num_cells, tmp_cell_count,
            #       tmp_upper_95ci, tmp_lower_95ci, tmp_95ci)
            # if upper_95ci_list[-1] < sp1_percent*1.1 and \
            #   lower_95ci_list[-1] > sp1_percent*0.9:
            if tmp_95ci < 0.03:
                tmp_count_good += 1
            else:
                tmp_count_good = 0

            if tmp_count_good >= 3:
                break

        print(total_num_cells, sp1_percent, tmp_count_good,
              tmp_cell_count, "%.4f" % tmp_upper_95ci,
              "%.4f" % tmp_lower_95ci, "%.4f" % tmp_95ci)
