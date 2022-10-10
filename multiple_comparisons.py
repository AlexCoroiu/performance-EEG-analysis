# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:01:37 2022

@author: User
"""

#setup
import mne
import scipy.stats
import preparation as prep
import constants as c
import numpy as np
import pandas as pd
import math
import file_manager as fm
#load prepped data

#test mean == 0, 2 sided
#for each time x electrode
#default treshold corresponding to 0.05 p-value

def multiple_comparison(data):
    print('Data\n', data)
    #reshape data into (time x channel) on participant
    #format wide
    data = data.pivot(index=['time','channel'], 
                      columns='part')
    print('Data Pivoted\n', data)
    
    #ttest
    t_stats, p_vals = scipy.stats.ttest_1samp(data, 
                                              popmean = 0, 
                                              axis = 1,
                                              alternative = 'two-sided')

    #results df
    data['p_val'] = p_vals 
    data = data.droplevel('part', axis = 1)
    results = data[['p_val']]
    results = results.reset_index()
    print('Results Indexed\n',results)
    return results

    
def bonferroni(results):
    reject, pval_corrected = mne.stats.bonferroni_correction(results['p_val'], 
                                                             alpha = c.SIGNIFICANCE)
    results['bonferroni_reject'] = reject

    return results
    

def crit_p_correction(results, crit_p):
    reject = [ p < crit_p for p in results['p_val']]
    results['crit_p_reject'] = reject
    
    return results


def window(results):
    windows = results['time'].unique()
    nr_windows = len(windows)
    electrodes = results['channel'].unique()
    nr_electrodes = len(electrodes)
    
    # print('Nr. windows', nr_windows)
    # print('Nr. electrodes', nr_electrodes)
    
    #crit p correction
    crit_p = math.sqrt(c.SIGNIFICANCE/((nr_windows-1)*nr_electrodes))
    print('Critical P-Value', crit_p)
    results = crit_p_correction(results, crit_p)
    
    #window correction
    
    #create window x electrode matrix
    matrix = results.pivot(index = 'time',
                            columns = 'channel',
                            values = 'crit_p_reject'
                            )
    
    window_matrix = matrix.copy(deep = True)

    last_window = nr_windows-1
    
    #false if no true neighbour
    for e in electrodes:
        if not ((matrix.at[windows[0], e] == True) 
            and (matrix.at[windows[1], e] == True)):
            window_matrix.at[windows[0], e] = False
        
        for i in range(1, last_window - 1):
            if not ((matrix.at[windows[i], e] == True) 
                and ((matrix.at[windows[i-1], e] == True 
                or matrix.at[windows[i+1], e] == True))):
                window_matrix.at[windows[i], e] = False 
                
        if not ((matrix.at[windows[last_window], e] == True) 
            and (matrix.at[windows[last_window - 1], e] == True)):
            window_matrix.at[windows[last_window], e] = False
                
    #back to long format
    window_results = window_matrix.melt(ignore_index = False,
                                         value_name = 'window_reject')
    window_results = window_results.reset_index()
    print('Window Results Melted and Indexed\n', window_results)
    
    #add as column to results
    results = pd.merge(results, window_results, how = 'inner',
                       left_on = ['time', 'channel'],
                       right_on = ['time', 'channel'])
    print('Results Merged\n', results)
    
    return results

def test_condition(window_size, density, local, cond, correction):         
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #load prepped data
    data = prep.load_test_dfs(window_size, density, local) 
    data_cond = data[cond]

    results = multiple_comparison(data_cond)
    
    if correction == 'bonferroni':
        b_results = bonferroni(results)  
        b_results = b_results[b_results['bonferroni_reject'] == True]
        #save
        dataframe_file = dataset + '\\' + cond + '_b.csv'
        b_results.to_csv(dataframe_file, index = False)

    elif correction == 'window':
        w_results = window(results)
        w_results = w_results[w_results['window_reject'] == True]
        #save
        dataframe_file = dataset + '\\' + cond + '_w.csv'
        w_results.to_csv(dataframe_file, index = False)
                
def test(correction):
    dataset = fm.ANALYSED_DIR
    fm.do_dir(dataset)
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    test_condition(w,d,l,cond,correction)
                    
def test_window():
    test('window')
                    
def test_bonferroni():
    test('bonferroni')
                                        
#test_condition(0.02, 64, False, 'vs_left', 'window')
    