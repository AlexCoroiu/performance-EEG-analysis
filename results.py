# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:19:05 2022

@author: User

"""

import file_manager as fm
import constants as c
import pandas as pd


#TODO load results here (from all 3 methods?) OR
# have separate laod fucntions in the separate method files from analysis 
# (as per structure up to analysis)
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
    time = (c.INTERVAL_MAX - c.INTERVAL_MIN)/window_ms #TODO make int with round down
    electrodes =  density
    if local:
        electrodes = c.DENSITY[density]
        electrodes = len(list(set(electrodes) & set(c.CHANNELS_VISUAL)))

    total = time * electrodes
    
    #significant tests
    analysed = load_analysed(window_size,density,local,cond,method)
    total_sig = len(analysed)
    
    #TP
    
    #TN
    
    #TODO add TP, TN, calcualte precision
    return [window_size, density, local, cond, method, total, total_sig] 
    
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
                              columns =['window_size', 'density', 'local', 
                                        'condition', 'method', 'total', 
                                        'total_significant'])
    """   
        , 'TP', 'FP', 
        'precision'
    """
    
    dataframe_file = dataset + '\\results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results #for future list operatiosn (e.g. extend)
    
def results_mc_window():
    return results_mc('w')
    
def results_mc_bonferroni():
    return results_mc('b')
    
#cluster permutations resutls
#def results_cp():
    
                    
#print(summary_results(0.02,86, True, 'baseline', 'w'))

#TODO restructure results data 
#(windoes size, electrodes number, electrodes positions, sig data points # / test cond) 
#--> for each entry have a separate table with (count, time, location)


#TODO how to combien reuslts from the 3 different methods?



    
