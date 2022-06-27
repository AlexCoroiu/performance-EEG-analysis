# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:05:18 2022

@author: User
"""

import pandas as pd
import os

def load_results(dataset):
    dataframe_file = dataset + '\\results.csv'
    results = pd.read_csv(dataframe_file)
    return results
    
def concat_results():
    path = "."
    datasets = [subdir.name for subdir in os.scandir(path) 
                if (subdir.is_dir() and subdir.name.startswith("data_")) ]
    #print(datasets)    
    
    results_list = []
    for dataset in datasets:
        results = load_results(dataset)

        #add columns to df
        sim_vars = dataset.split('_')
        amp = sim_vars[1].replace('amp', '')
        noise = sim_vars[2].replace('noise', '')
        
        #print(amp, noise)
        results['amp'] = amp
        results['noise'] = noise
        
        #add to results list
        results_list.append(results)
        
    #concat into new df
    results_df = pd.concat(results_list)
    #save
    dataframe_file = 'concat_results.csv'
    results_df.to_csv(dataframe_file, index = False)
        
        
concat_results()