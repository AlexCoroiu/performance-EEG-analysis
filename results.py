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

def extract_actual(predicted):
    predicted_count = len(predicted)
    
    #actual positives found in predicted values
    #expected time interval
    positives = predicted[(predicted['time'] <= c.SIG_INTERVAL_MAX) &
                          (predicted['time'] >= c.SIG_INTERVAL_MIN)] #must use bit wise boolean logic operators
    
    #expected electrode location
    positives = positives[positives['channel'].isin(c.CHANNELS_VISUAL)]
    
    positives_count = len(positives)
    
    #actual negatives found in predicted values
    negatives_count = predicted_count - positives_count 
    
    return (predicted_count, positives_count, negatives_count)

#do calcualtions and add to data
def summary_results_mc(window_size,density,local,cond,method):

    #TODO diff way to calcualte total and crit p val
    #total tests performed
    window_ms = int(window_size*1000)
    time = math.floor((c.TEST_INTERVAL_MAX - c.TEST_INTERVAL_MIN)/window_ms) #rounded down
    electrodes =  density
    if local:
        electrodes = c.DENSITY[density]
        electrodes = len(list(set(electrodes) & set(c.CHANNELS_VISUAL)))

    total = time * electrodes

    #CONFUSION MATRIX
    analysed = load_analysed(window_size,density,local,cond,method)
    
    #significant test results
    predicted_positive = analysed[analysed['significant'] == True] 
    P_count, TP_count, FP_count = extract_actual(predicted_positive)
    
    #non significant test results
    predicted_negative = analysed[analysed['significant'] == False]   
    N_count, FN_count, TN_count = extract_actual(predicted_negative) 
    
    #METRICS 
    
    #precision
    if P_count != 0:
        precision = TP_count/P_count
    else:
        precision = 0
        
    #TODO other metrics
    
    return [window_size, density, local, cond, method, total, 
            P_count, TP_count, FP_count, 
            N_count, TN_count, FN_count,
            precision] 


#TODO total clusters, TN, FN
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
    
    #TN
    
    #FN
    
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
                                        'total_P','TP', 'FP', 
                                        'total_N', 'TN', 'FN',
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
                                        'total_P','TP', 'FP', 
                                        'precision'])

    
    dataframe_file = dataset + '\\results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#print(summary_results(0.02,86, True, 'baseline', 'w'))





    
