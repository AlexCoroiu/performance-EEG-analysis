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

def load_analysed(window_size, time, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file = dataset + '\\' + cond + '_' + method + '.csv'
    analysed = pd.read_csv(dataframe_file)
              
    return analysed

def true_signal_mc(data, cond):
    #actual positive data units found in data
    if "baseline" in cond:
        #no local positives expected
        expected = [False for _ in data['significant']]
    
    else:
        #expected time interval & visual electrodes
    
        expected = np.where((data['time'] <= c.SIG_INTERVAL_MAX) &
                            (data['time'] >= c.SIG_INTERVAL_MIN) &
                            data['channel'].isin(c.CHANNELS_VISUAL),
                            True, False) #must use bit wise boolean logic operators

    return expected

def true_signal_cp(data, cond):
    
    if "baseline" in cond:
        #no local positives expected for any data unit
        expected = [False for _ in data['significant']]

    else:
        #cluster contains at least one point in expected signal
        expected = [any(((datapoint[0] <= c.SIG_INTERVAL_MAX) and #time
                         (datapoint[0] >= c.SIG_INTERVAL_MIN) and #time
                         datapoint[1] in c.CHANNELS_VISUAL) #channel
                        for datapoint in cluster_dps) 
                    for cluster_dps in data['data_points']]
    
    return expected

def get_metrics(expected, found):

    #confusion matrix    
    confusion_matrix = sklearn.metrics.confusion_matrix(expected,
                                                        found, 
                                                        labels = [False, True])
    
    (TN, FP, FN, TP) = confusion_matrix.ravel()
    
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
    
    return (TN, FP, FN, TP, type_I_ER, type_II_ER)
        
#precision, recall and F1 dont make sense to emasure this dataset

#do calcualtions and add to data
def summary_results_mc(window_size,time,density,local,cond,method):

    analysed = load_analysed(window_size,time,density,local,cond,method)
    
    #total tests
    total = len(analysed)
    
    #crit_p
    crit_p_val = analysed['crit_p_val'].values[0]
    
    #CONFUSION MATRIX & METRICS
    analysed['expected'] = true_signal_mc(analysed,cond)
    
    (TN_count, FP_count, FN_count, TP_count, 
     type_I_error, type_II_error) = get_metrics(analysed['expected'],
                                                analysed['significant'])
                                          
    positives = TP_count + FP_count
    # global_significant = (positives > 0) #any true positive test
    global_significant =  (positives > (total*c.SIGNIFICANCE)) #5% true positive tests                      
    
    return [window_size, time, density, local, 
            cond, method, 
            crit_p_val, total, positives, global_significant,
            TP_count, FP_count, TN_count, FN_count,
             type_I_error, type_II_error] 


def summary_results_cp(window_size,time,density,local,cond):
    
    analysed = load_analysed(window_size,time,density,local,cond,'cp')
    
    #covnert data_points to list type
    analysed['data_points'] = analysed['data_points'].apply(literal_eval)
    
    #crit_p
    crit_p_val = c.SIGNIFICANCE
    
    #total clusters
    total = len(analysed)
        
    #what if there are no clusters identified
    if total > 0:
        #CONFUSION MATRIX LOCAL
        analysed['expected'] = true_signal_cp(analysed,cond)
        
        (TN_count, FP_count, FN_count, TP_count, 
         type_I_error, type_II_error) = get_metrics(analysed['expected'],
                                              analysed['significant'])
        
        positives = TP_count + FP_count
        global_significant = (positives > 0) #any positive cluster
                                              
        #save
        return [window_size, time, density, local, 
                cond, 'cp',
                crit_p_val, total, positives, global_significant,
                TP_count, FP_count, TN_count, FN_count,
                type_I_error, type_II_error] 
    else:
        return [window_size, time, density, local, 
                cond, 'cp',
                crit_p_val, total, 0, False,
                0, 0, 0, 0,
                0, 0] 

        
    
#multiple comaprisons results for all method params
def results_mc(method):
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in c.TEST_CONDITIONS:
                        print('...RESULTS MC',w,t,d,l,cond,method)
                        result = summary_results_mc(w,t,d,l,cond,method)
                        results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'time_interval',
                                        'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val', 'total', 
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'type_I_ER', 'type_II_ER'])

    dataframe_file = dataset + '\\results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
def results_mc_window():
    return results_mc('mc_w')
    
def results_mc_bonferroni():
    return results_mc('mc_b')

    
#cluster permutations results
def results_cp(): #redundant code but oh well
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in c.TEST_CONDITIONS:
                        print('...RESULTS CP',w,t,d,l,cond)
                        result = summary_results_cp(w,t,d,l,cond)
                        results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'time_interval',
                                        'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val','total',
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'type_I_ER', 'type_II_ER'])
    
    dataframe_file = dataset + '\\results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))
    