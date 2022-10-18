# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:05:18 2022

@author: User
"""

import pandas as pd
import os
import sklearn.metrics
import seaborn as sb

#load final results

def load_final_results():
    dataframe_file = 'final_results.csv'
    data = pd.read_csv(dataframe_file)
    
    return data

def group_stats(data, i_var, d_var):
    grouped = data.groupby(i_var)
    print(grouped[d_var].describe())

#print(load_final_results())

data = load_final_results()

#SUMAMRY STATISTICS
group_stats(data, 'method', 'F1')

#EXPLORATION VARIABLES

#filter for window method
data_w = data[data['method'] == 'w']

#amplitude
group_stats(data_w, 'amplitude', 'F1')
#noise filter
group_stats(data_w, 'noise_filter', 'F1')
#window size
group_stats(data_w, 'window_size', 'F1')
#density
group_stats(data_w, 'density', 'F1')
#location
group_stats(data_w, 'location', 'F1')
#bandpass
group_stats(data_w, 'band_pass', 'F1')
#condition
group_stats(data_w, 'condition', 'F1')

#much betetr at detecting signal then at detecting baseline or difference
#TODO per condition
#TODO type I, type II error 
#(probs a lot of false positives in baselien and a lot of false negatives in diff)

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

