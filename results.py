# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:19:05 2022

@author: User

"""

import file_manager as fm
import constants as c
import pandas as pd
import math

def load_analysed(window_size, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file = dataset + '\\' + cond + '_' + method + '.csv'
    analysed = pd.read_csv(dataframe_file)
              
    return analysed

#do calcualtions and add to data
def summary_results(window_size,density,local,cond,method):

    #total tests performed
    window_ms = int(window_size*1000)
    time = math.floor((c.TEST_INTERVAL_MAX - c.TEST_INTERVAL_MIN)/window_ms) #rounded down
    electrodes =  density
    if local:
        electrodes = c.DENSITY[density]
        electrodes = len(list(set(electrodes) & set(c.CHANNELS_VISUAL)))

    total = time * electrodes
    
    #significant tests
    sig = load_analysed(window_size,density,local,cond,method)
    sig_count = len(sig)
    
    #TP
    #expected time interval
    tp = sig[(sig['time'] <= c.SIG_INTERVAL_MAX) &
             (sig['time'] >= c.SIG_INTERVAL_MIN)] #must use bti wise boolean logic operators
    
    #expected electrode location
    tp = tp[tp['channel'].isin(c.CHANNELS_VISUAL)]
    
    tp_count = len(tp)
    
    #FP
    fp_count = sig_count - tp_count 
    fp_count = 0
    
    #precision
    if sig_count != 0:
        precision = tp_count/sig_count
    else:
        precision = 0
    

    return [window_size, density, local, cond, method, total, 
            sig_count, tp_count, fp_count, precision] 
    
#do for all in dataset

#multiple comaprisons results
def results_mc(method):
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    result = summary_results(w,d,l,cond,method)
                    results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'density', 'location', 
                                        'condition', 'method', 'total', 
                                        'total_significant','TP', 'FP', 
                                        'precision'])

    
    dataframe_file = dataset + '\\results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df #for future list operatiosn (e.g. extend)
    
def results_mc_window():
    return results_mc('w')
    
def results_mc_bonferroni():
    return results_mc('b')
    
#cluster permutations resutls
#TODO how to combine mc wiht cp results?
#def results_cp():
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))

#TODO electrodes positions, timeframe "clusters"?





    
