# -*- coding: utf-8 -*-
"""

@author: User
"""
import file_manager as fm
import constants as c

import simulation
import processing

import preparation
import multiple_testing
import cluster_permutations

import results

import pandas as pd

# SIMULATE-ANALYSE-CUMMULATE DATA
def run_data():
    simulation.simulate()
    processing.process()
    preparation.prepare()
      
def run_methods():
    multiple_testing.test_window()
    multiple_testing.test_bonferroni()
    cluster_permutations.test()

def run_results():
    res_dfs = []
    res_dfs.append(results.results_mt_window())
    res_dfs.append(results.results_mt_bonferroni())
    res_dfs.append(results.results_cp())
    
    #concat all results
    res = pd.concat(res_dfs, axis=0)
    #print('res df\n', res)
    return res
    
def run_dataset(amplitude, noise_filter, band_pass_filtering):
    
    #SETUP
    #file structure
    fm.set_up(amplitude, noise_filter, band_pass_filtering)
    
    #constants  
    c.set_up(amplitude, noise_filter, band_pass_filtering)
    
    print('...RUNNING', amplitude, noise_filter, band_pass_filtering)

    #RUN 
    # run_data()
    # run_methods()
    res = run_results()
    
    return res

# run_dataset((60,30), (0.1,-0.1,0.02), True)

#RUN ALL DATASETS
    
#I think better here, to see celarly the role and workings of the setup functions
amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]

def run():
    results = []
    for amp in amplitudes:
        for nf in noise_filters:
            for bpf in band_pass_filtering:
                res = run_dataset(amp, nf, bpf)
                
                res['amplitude'] = str(amp)
                res['noise'] = "high" if (nf[0] == 0.1) else "low" 
                res['band_pass'] = bpf #str(bpf)
                
                results.append(res) 
                
    #save cummulated results to df
    results_df = pd.concat(results, axis=0)
    
    columns = ['amplitude', 'noise', 'band_pass',
                'window_size', 'time_interval',
                'density', 'location', 
                'condition', 'method', 
                'crit_p_val', 'total',
                'positives', 'global_significant',
                'TP', 'FP', 'TN', 'FN',
                'type_I_ER', 'type_II_ER']

    results_df = results_df[columns]
    
    #print(results_df.isnull().sum().sum()) #check for NaN

    dataframe_file = 'results.csv'
    results_df.to_csv(dataframe_file, index = False)

run()
#exploration.explore() #needs setup beforehand
