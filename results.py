# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:19:05 2022

@author: User

"""

import file_manager as fm
import constants as c
import pandas as pd
import numpy as np
import sklearn.metrics
from ast import literal_eval

def load_analysed(window_size, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file = dataset + '\\' + cond + '_' + method + '.csv'
    analysed = pd.read_csv(dataframe_file)
              
    return analysed

def true_signal_mc(data):
    #actual positives found in predicted values
    #expected time interval & visual electrodes

    expected = np.where((data['time'] <= c.SIG_INTERVAL_MAX) &
                        (data['time'] >= c.SIG_INTERVAL_MIN) &
                        data['channel'].isin(c.CHANNELS_VISUAL),
                        True, False) #must use bit wise boolean logic operators

    return expected

def true_signal_cp(data):

    expected = [any(((datapoint[0] <= c.SIG_INTERVAL_MAX) and #time
                     (datapoint[0] >= c.SIG_INTERVAL_MIN) and #time
                     datapoint[1] in c.CHANNELS_VISUAL) #channel
                    for datapoint in data_points) 
                for data_points in data['data_points']]
    
    return expected


def get_metrics(expected, found):
    #confusion matrix
    confusion_matrix = sklearn.metrics.confusion_matrix(expected,
                                                        found, 
                                                        labels = [False, True])
    
    (TN_count, FP_count, FN_count, TP_count) = confusion_matrix.ravel()
    
    #metrics
    precision = sklearn.metrics.precision_score(expected,found, zero_division = 0)
    
    return (TN_count, FP_count, 
            FN_count, TP_count, 
            precision)
    

#do calcualtions and add to data
def summary_results_mc(window_size,density,local,cond,method):

    analysed = load_analysed(window_size,density,local,cond,method)
    
    #total tests
    total = len(analysed)
    
    #crit_p
    crit_p_val = analysed['crit_p_val'].values[0]
    
    #CONFUSION MATRIX & METRICS
    analysed['expected'] = true_signal_mc(analysed)
    
    (TN_count, FP_count, 
     FN_count, TP_count, 
     precision) = get_metrics(analysed['expected'],
                 analysed['significant'])
    
    return [window_size, density, local, 
            cond, method, 
            crit_p_val, total, 
            TP_count, FP_count, 
            TN_count, FN_count,
            precision] 


def summary_results_cp(window_size,density,local,cond):
    
    analysed = load_analysed(window_size,density,local,cond,'cp')
    
    #covnert data_points to list type
    analysed['data_points'] = analysed['data_points'].apply(literal_eval)
    
    #total clusters
    total = len(analysed)
    
    #crit_p
    crit_p_val = analysed['crit_p_val'].values[0] # == c.SIGNIFICANCE always
    
    #CONFUSION MATRIX
    analysed['expected'] = true_signal_cp(analysed)
    
    (TN_count, FP_count, 
     FN_count, TP_count, 
     precision) = get_metrics(analysed['expected'],
                 analysed['significant'])
    
    #save
    return [window_size, density, local, 
            cond, 'cp', 
            crit_p_val, total, 
            TP_count, FP_count, 
            TN_count, FN_count,
            precision] 
    
#multiple comaprisons results for all method params
def results_mc(method):
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    result = summary_results_mc(w,d,l,cond,method)
                    results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val', 'total', 
                                        'TP', 'FP', 
                                        'TN', 'FN',
                                        'precision'])

    
    dataframe_file = dataset + '\\results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
def results_mc_window():
    return results_mc('w')
    
def results_mc_bonferroni():
    return results_mc('b')

    
#cluster permutations resutls
def results_cp(): #redundant code but oh well
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    result = summary_results_cp(w,d,l,cond)
                    results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val','total', 
                                        'TP', 'FP',
                                        'TN', 'FN',
                                        'precision'])

    
    dataframe_file = dataset + '\\results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))
    
#TODO scikit metrics or own functions?