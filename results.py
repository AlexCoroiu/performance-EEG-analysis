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
def summary_results_mc(window_size,density,local,cond,method):

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
    

def summary_results_cp(window_size,density,local,cond):
    
    sig = load_analysed(window_size,density,local,cond,'cp')
    
    #sig cluster count
    clusters = list(set(sig.columns.tolist()) - set(['time', 'channel']))
    sig_count = len(clusters)
    
    #TP
    tp_clusters = []
    for clust in clusters:
        cluster_df = sig[['time','channel',clust]]
        
        #retain only cluster vars
        cluster_df = cluster_df[cluster_df[clust] == True]
        
        #add only columns which contain true positives for vals in signal criteria
        cluster_df = cluster_df[(cluster_df['time'] <= c.SIG_INTERVAL_MAX) &
                                (cluster_df['time'] >= c.SIG_INTERVAL_MIN)]
        cluster_df = cluster_df[cluster_df['channel'].isin(c.CHANNELS_VISUAL)]
        
        #if there is any sig data point in the cluster, consider it a true positive
        if cluster_df.shape[0] > 0:
            tp_clusters.append(clust)
        
    tp_count = len(tp_clusters)
    
    #FP
    fp_count = sig_count - tp_count
    
    #precision
    if sig_count != 0:
        precision = tp_count/sig_count
    else:
        precision = 0
    
    total = None
    return [window_size, density, local, cond, 'cp', total, 
            sig_count, tp_count, fp_count, precision] 
    

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
                                        'condition', 'method', 'total', 
                                        'total_significant','TP', 'FP', 
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
                                        'condition', 'method', 'total', 
                                        'total_significant','TP', 'FP', 
                                        'precision'])

    
    dataframe_file = dataset + '\\results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))

#TODO electrodes positions, timeframe "clusters"?





    
