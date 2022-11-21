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
    crit_p_val = c.SIGNIFICANCE/(len(results))
    results['crit_p_val'] = crit_p_val #save crit p value
    
    reject, pval_corrected = mne.stats.bonferroni_correction(results['p_val'], 
                                                             alpha = c.SIGNIFICANCE)
    results['bonferroni_reject'] = reject

    return results
    

def crit_p_correction(results, nr_windows, nr_electrodes):
    crit_p = math.sqrt(c.SIGNIFICANCE/((nr_windows-1)*nr_electrodes))
    results['crit_p_val'] = crit_p #save crit p value
    
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
    results = crit_p_correction(results, nr_windows, nr_electrodes)
    
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

def test_condition(window_size, time, density, local, cond, correction):         
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #load prepped data
    data = prep.load_test_dfs(window_size, time, density, local) 
    data_cond = data[cond]

    results = multiple_comparison(data_cond)
    
    if correction == 'bonferroni':
        b_results = bonferroni(results)  
        b_results['significant'] = b_results['bonferroni_reject'] #null hypothesis was rejected
        #save
        dataframe_file = dataset + '\\' + cond + '_mc_b.csv'
        b_results.to_csv(dataframe_file, index = False)

    elif correction == 'window':
        w_results = window(results)
        w_results['significant'] = w_results['window_reject'] #null hypothesis was rejected
        #save
        dataframe_file = dataset + '\\' + cond + '_mc_w.csv'
        w_results.to_csv(dataframe_file, index = False)
                
def test(correction):
    dataset = fm.ANALYSED_DIR
    fm.do_dir(dataset)
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in c.TEST_CONDITIONS:
                        test_condition(w,t,d,l,cond,correction)
                    
def test_window():
    test('window')
                    
def test_bonferroni():
    test('bonferroni')
                                        
#test_condition(0.02, 64, False, 'vs_left', 'window')
    