# -*- coding: utf-8 -*-
"""

@author: User
"""
import file_manager as fm
import constants as c

import simulation
import processing

import preparation
import multiple_comparisons
import cluster_permutations

import results

import pandas as pd

# SIMULATE-ANALYSE-CUMMULATE DATA
def run_data():
    simulation.simulate()
    processing.process()
    preparation.prepare()
     
def run_methods():
    multiple_comparisons.test_window()
    multiple_comparisons.test_bonferroni()
    cluster_permutations.test()
    
def run_results():
    res = []
    res.extend(results.results_mc_window())
    res.extend(results.results_mc_bonferroni())
    #res.extend(results.results_cp())
    return res
    
def run_dataset(amplitude, noise_filter, band_pass_filtering):
    
    #SETUP
    #file structure
    fm.set_up(amplitude, noise_filter, band_pass_filtering)
    
    #constants  
    c.set_up(amplitude, noise_filter, band_pass_filtering)

    #RUN 
    #run_data()
    #run_methods()
    res = run_results()
    
    return res

    
#run_dataset((60,30), (0.1,-0.1,0.02), True)

#RUN ALL DATASETS
    
#TODO see where to declare these variables ranges (here or in the constants file)
#I think betetr here, to see celarly the role and workings of the setup functions
amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]
    
def run():
    final_results = []
    for amp in amplitudes:
        for nf in noise_filters:
            for bpf in band_pass_filtering:
                res = run_dataset(amp, nf, bpf)
                
                #TODO append with extra vars for all
                res['amplitude'] = amp
                res['noise_filter'] = nf
                res['band_pass'] = bpf
                
                final_results.append(res) 
                
    #save cummulated results to df
    results_df = pd.DataFrame(results, 
                              columns =['amplitude', 'noise_filter', 'band_pass',
                                        'window_size', 'density', 'location', 
                                        'condition', 'method', 'total', 
                                        'total_significant', 'TP', 'FP', 
                                        'precision'])
    
    dataframe_file = 'final_results.csv'
    results_df.to_csv(dataframe_file, index = False)

run()
#exploration.explore() #needs setup beforehand