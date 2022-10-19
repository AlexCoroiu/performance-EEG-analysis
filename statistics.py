# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:05:18 2022

@author: User
"""

import pandas as pd
import os
import sklearn.metrics
import seaborn as sb
import numpy as np
from results import get_metrics

#load final results
def load_final_results():
    dataframe_file = 'final_results.csv'
    data = pd.read_csv(dataframe_file)
    
    return data

def group_stats(data, i_var, d_var):
    grouped = data.groupby(i_var)
    print(grouped[d_var].describe())
    

data = load_final_results()

data['expected'] = np.where(data['condition'] == 'baseline', False, True)

#(TN, FP, FN, TP, precision, recall, F1)
results = get_metrics(data['expected'], 
                      data['global_significant'])

print(results)

#SUMAMRY STATISTICS

#general per method 
group_stats(data, 'method', 'F1')
group_stats(data, 'method', 'global_significan')

# ==> cluster permutation precision is better but the result is less exact (?)

#EXPLORATION VARIABLES

#filter for window method
data_w = data[data['method'] == 'w']

#condition
group_stats(data_w, 'condition', 'global_significant')


group_stats(data_w, 'condition', 'F1')
# ==> much betetr at detecting signal then at detecting baseline or difference

i_vars = ['amplitude', 'noise_filter', 'band_pass',
          'window_size', 'density', 'location' ]

d_vars = ['F1', 'FP' , "FN"]

for d in d_vars:
    print("\n", d, "\n")
    for i in i_vars:
        group_stats(data_w, i, d)

#TODO per condition
#(probs a lot of false positives in baseline 
#and a lot of false negatives in diff)

#data_w.plot.scatter(x='crit_p_val', y = 'F1')

sb.lmplot(x='crit_p_val', y = 'F1', data = data_w, fit_reg = True)
sb.lmplot(x='total', y = 'F1', data = data_w, fit_reg = True)
sb.lmplot(x='total', y = 'crit_p_val', data = data_w, fit_reg = True)

#as the number of tests increases the crit_p_value decreases
#lower crit p val => lower F1

sb.lmplot(x='crit_p_val', y = 'FP', data = data_w, fit_reg = True)
sb.lmplot(x='crit_p_val', y = 'FN', data = data_w, fit_reg = True)

#higher crit_p_val => lower FP (type I) and especially lower FN (type II)

#STATISTICAL TESTS

