# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 18:19:05 2022

@author: User

"""

import file_manager as fm
import constants as c
import pandas as pd
import os

def load_analysed(window_size, density, local, cond, test):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file = dataset + '\\' + cond + '_' + test + '.csv'
    analysed = pd.read_csv(dataframe_file)
              
    return analysed

def summary_results(w,d,l,cond,t):
    analysed = load_analysed(w,d,l,cond, t)
    
    t_count = len(analysed)
    ch_count = len(analysed['channel'].unique())
    t_count = len(analysed['time'].unique())
    
    w = int(w*1000)
    return [w,d,l,cond, t, ch_count, t_count, t_count]
    
def results():
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    result = summary_results(w,d,l,cond,'w')
                    results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'density', 'local', 
                                        'condition', 'test', 'channel_count', 
                                        'time_count','total_count'])
    
    dataframe_file = dataset + '\\results.csv'
    results_df.to_csv(dataframe_file, index = False)
                    
#print(summary_results(0.02,86, True, 'baseline', 'w'))

#TODO restructure results data 
#(windoes size, electrodes number, electrodes positions, sig data points # / test cond) 
#--> for each entry have a separate table with (count, time, location)


            
        
    
