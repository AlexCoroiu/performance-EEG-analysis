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

    #cluster contains at least one point in expected signal
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
    
    (TN, FP, FN, TP) = confusion_matrix.ravel()
      
    #edge cases precision
    if FP == 0 and TP == 0: #no cases predicted postive
        precision = 1
    else:
        precision = TP/(TP+FP)
        
    #edge case recall
    #hit rate (doesn't make sense when there are is no positive data)
    if FN == 0 and TP == 0: #no positives in the input data
        recall = 1
    else:
        recall = TP/(TP+FN)
        
    if precision == 0 and recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall/(precision + recall)
    
    #edge case type I error rate
    if FP == 0 and TN == 0: # no negatives in input data
        type_I_ER = 0
    else:
        type_I_ER = FP/(FP+TN) #statistical significance (false positive rate)
    
    #edge case type II error
    if FN == 0 and TP == 0: #no positives in input data
        type_II_ER = 0
    else:
        type_II_ER = FN/(FN+TP) #statistical power (false negative rate)
    
    return (TN, FP, FN, TP, precision, recall, f1, type_I_ER, type_II_ER)
        

#do calcualtions and add to data
def summary_results_mc(window_size,density,local,cond,method):

    analysed = load_analysed(window_size,density,local,cond,method)
    
    #total tests
    total = len(analysed)
    
    #crit_p
    crit_p_val = analysed['crit_p_val'].values[0]
    
    #CONFUSION MATRIX & METRICS
    analysed['expected'] = true_signal_mc(analysed)
    
    (TN_count, FP_count, FN_count, TP_count, 
     precision, recall, F1,
     type_I_error, type_II_error) = get_metrics(analysed['expected'],
                                                analysed['significant'])
                                          
    positives = TP_count + FP_count
    global_significant =  (positives > (total*c.SIGNIFICANCE)) #!!!                         
    
    return [window_size, density, local, 
            cond, method, 
            crit_p_val, total, positives, global_significant,
            TP_count, FP_count, TN_count, FN_count,
            precision, recall, F1, type_I_error, type_II_error] 


def summary_results_cp(window_size,density,local,cond):
    
    analysed = load_analysed(window_size,density,local,cond,'cp')
    
    #covnert data_points to list type
    analysed['data_points'] = analysed['data_points'].apply(literal_eval)
    
    #total clusters
    total = len(analysed)
    
    #crit_p
    crit_p_val = analysed['crit_p_val'].values[0] # == c.SIGNIFICANCE always
    
    #CONFUSION MATRIX LOCAL
    analysed['expected'] = true_signal_cp(analysed)
    
    (TN_count, FP_count, FN_count, TP_count, 
     precision, recall, F1,
     type_I_error, type_II_error) = get_metrics(analysed['expected'],
                                          analysed['significant'])
    
    positives = TP_count + FP_count
    global_significant = (positives > 0)
                                          
    #save
    return [window_size, density, local, 
            cond, 'cp',
            crit_p_val, total,  positives, global_significant,
            TP_count, FP_count, TN_count, FN_count,
            precision, recall, F1, type_I_error, type_II_error ] 
    
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
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'precision', 'recall', 'F1',
                                        'type_I_ER', 'type_II_ER'])

    dataframe_file = dataset + '\\results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
def results_mc_window():
    return results_mc('mc_w')
    
def results_mc_bonferroni():
    return results_mc('mc_b')

    
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
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'precision', 'recall', 'F1',
                                        'type_I_ER', 'type_II_ER'])
    
    dataframe_file = dataset + '\\results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))
    