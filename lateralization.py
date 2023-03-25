# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

import file_manager as fm
import constants as c
import processing as pross
import multiple_testing as mt
import cluster_permutations as cp
import results as res
import statistics_summary as stats
import pandas as pd
import numpy as np
from ast import literal_eval

pd.options.mode.chained_assignment = None  # default='warn'

#PREPARE

#channels by hemipshere
CHANNELS_86_LEFT = ['Fp1',  
                    'AF9', 'AF7', 'AF5', 'AF3', 'AF1', 
                    'F9', 'F7', 'F5', 'F3', 'F1', 
                    'FT9', 'FT7', 'FC5', 'FC3', 'FC1', 
                    'T9', 'T7', 'C5', 'C3', 'C1', 
                    'TP9', 'TP7', 'CP5', 'CP3', 'CP1',
                    'P9', 'P7', 'P5', 'P3', 'P1', 
                    'PO9', 'PO7', 'PO5', 'PO3', 'PO1', 
                    'O1',  
                    'O9' ]
CHANNELS_86_RIGHT = ['Fp2', 
                    'AF10', 'AF8', 'AF6', 'AF4', 'AF2',
                    'F10', 'F8', 'F6', 'F4', 'F2', 
                    'FT10', 'FT8', 'FC6', 'FC4', 'FC2', 
                    'T10', 'T8', 'C6', 'C4', 'C2',
                    'TP10', 'TP8', 'CP6', 'CP4', 'CP2', 
                    'P10', 'P8', 'P6', 'P4', 'P2', 
                    'PO10', 'PO8', 'PO6', 'PO4', 'PO2', 
                    'O2', 
                    'O10']

CHANNELS_86_PAIRS = list(zip(CHANNELS_86_LEFT, CHANNELS_86_RIGHT))

LATERALIZATION = 'lateralization'
conditions = ['baseline', 'vs']

#get electrode pair
def get_pair(row):
    channel = row['channel']
    pair = next(filter(lambda p: channel in p, CHANNELS_86_PAIRS), None)
    return pair

#get hemisphere of electrode
def get_hemi(row):
    channel = row['channel']
    nr = int(channel[-1])
    
    return 'left' if nr % 2 == 1 else 'right'

#calculate alteralization betwen left and right hemipshere
def get_lat(row):
    condition = row['condition']
    left = row['left']
    right = row['right']
    
    lat = None
    
    if condition == 'vs_right':
        lat = left - right
    else: #vs_left and baseline
        lat = right - left
        
    return lat

#check if correct pair
def check_pair(row, electrodes):
    (left, right) = row['pair']
    
    return (left in electrodes) and (right in electrodes)
    #check if left & right are in electrodes
    
#prepare lateralization dataset for analysis
def prepare_test_df(df, window_size, time, density, local):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.PREPARATION_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #select time windows
    df = df[df['time'] % window_ms == 0]
    
    if time:
        df = df[(df['time'] >= c.TEST_INTERVAL_MIN) & 
                (df['time'] <= c.TEST_INTERVAL_MAX)]

    #select electrodes
    electrodes = c.DENSITY[density]
    
    if local:
        electrodes = list(set(electrodes) & set(c.CHANNELS_VISUAL)) #intersection

    df['electrodes'] = df.apply(lambda row: check_pair(row, electrodes), axis = 1)
    
    df = df[df['electrodes'] == True]
    
    df = df.drop(columns = ['electrodes'])

    #save
    for cond in conditions:
        columns = ['part','time','pair', cond]
        df_cond = df[columns]
        dataframe_file = dataset + '\\lat_' + cond + '.csv'
        df_cond.to_csv(dataframe_file, index = False)

#prepare all datasets
def prepare():
    dataset = fm.PREPARATION_DIR 
    fm.do_dir(dataset)

    df = pross.load_evo_df()
        
    #select post stimulus time interval 0 to 500
    df = df[df['time'] >= 0]

    #assign pair
    df['pair'] = df.apply(get_pair, axis = 1)
    
    #remove center
    df = df.dropna(subset = ['pair'])
    
    #left/right
    df['hemi'] = df.apply(get_hemi, axis = 1)

    #pivot accordign to hemi
    df = df.pivot(index=['part', 'time', 'condition', 'pair'], 
                columns= 'hemi', 
                values= 'value')
    df = df.reset_index() #always has to reset otherwise index column cannot be accessed

    #calcualte diff
    df['lateralization'] = df.apply(get_lat, axis = 1)

    #remove baseline
    # df = df[df['condition'] != 'baseline'] #keep base in!

    #format accordign to condition
    df = df.pivot(index=['part','time', 'pair'], 
                                    columns='condition', 
                                    values= 'lateralization')
    df = df.reset_index()

    #calcualte avg
    df['vs'] = (df['vs_left'] + df['vs_right'])/2

    df = df.drop(columns = ['vs_left', 'vs_right'])

    #prepare cond dfs
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    print('...PREPARING',w, t, d, l )
                    prepare_test_df(df, w, t, d, l)

#load prepared lateralization data
def load_test_df(window_size, time, density, local):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.PREPARATION_DIR + '\\' + dir_name
    
    loaded = {}
    
    for cond in conditions:
        dataframe_file = dataset + '\\lat_' + cond + '.csv'
        prepared = pd.read_csv(dataframe_file)
        
        loaded[cond] = prepared
        
    return loaded
         
#ANALYZE    

#analyse one lateralization dataset with all methods
def test_lateralization(window_size, time, density, local, cond):         
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #load prepped data
    data = load_test_df(window_size, time, density, local) 
    data_cond = data[cond]
    
    #renamed from pair
    data_cond = data_cond.rename({'pair': 'channel'}, axis = "columns")
    
    #extract electrodes from one side
    #(C3,C4) --> C4 (take right hemi as per formula)
    pairs = data_cond['channel'].apply(literal_eval)
    electrodes = [pair[1] for pair in pairs]
    data_cond['channel'] = electrodes


    #mt
    mt_results = mt.multiple_testing(data_cond)
    
    #w
    w_results = mt.window(mt_results)
    w_results['significant'] = w_results['window_reject'] #null hypothesis was rejected
    #save
    dataframe_file = dataset + '\\lat_' + cond + '_mt_w.csv'
    w_results.to_csv(dataframe_file, index = False)
    
    #b
    b_results = mt.bonferroni(mt_results)
    b_results['significant'] = b_results['bonferroni_reject'] #null hypothesis was rejected
    #save
    dataframe_file = dataset + '\\lat_' + cond + '_mt_b.csv'
    b_results.to_csv(dataframe_file, index = False)
    
    
    #cp
    cp_results = cp.cluster_permutations(data_cond)  
    #save
    dataframe_file = dataset + '\\lat_' + cond + '_cp.csv'
    cp_results.to_csv(dataframe_file, index = False)
    
#analyse all datasets
def test():
    dataset = fm.ANALYSED_DIR
    fm.do_dir(dataset)
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in conditions:
                        print('...TESTING',w,t,d,l,cond)
                        test_lateralization(w,t,d,l,cond)
                    
#RESULTS

#multiple testing results for all datasets
def results_mt(method):
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in conditions:
                        lat_cond = 'lat_' + cond
                        print('...RESULTS MT',w,t,d,l,lat_cond)
                        result = res.summary_results_mt(w,t,d,l,lat_cond,method)
                        results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'time_interval',
                                        'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val', 'total', 
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'type_I_ER', 'type_II_ER'])

    dataframe_file = dataset + '\\lat_results_' + method + '.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 

def results_mt_window():
    return results_mt('mt_w')

def results_mt_bonferroni():
    return results_mt('mt_b')


#cluster permutation results
def results_cp(): #redundant code but oh well
    dataset = fm.DATA_DIR
    
    results = []
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in conditions:
                        lat_cond = 'lat_' + cond
                        print('...RESULTS CP',w,t,d,l,lat_cond)
                        result = res.summary_results_cp(w,t,d,l,lat_cond)
                        results.append(result)
                    
    results_df = pd.DataFrame(results, 
                              columns =['window_size', 'time_interval',
                                        'density', 'location', 
                                        'condition', 'method', 
                                        'crit_p_val','total',
                                        'positives', 'global_significant',
                                        'TP', 'FP', 'TN', 'FN',
                                        'type_I_ER', 'type_II_ER'])
    
    dataframe_file = dataset + '\\lat_results_cp.csv'
    results_df.to_csv(dataframe_file, index = False)
    
    return results_df 
    
#RUN

def run_dataset(amplitude, noise_filter, band_pass_filtering):
    
    #SETUP
    #file structure
    fm.set_up(amplitude, noise_filter, band_pass_filtering)
    
    #constants  
    c.set_up(amplitude, noise_filter, band_pass_filtering)

    print('...RUNNING',amplitude, noise_filter, band_pass_filtering)
    
    #RUN 
    prepare()
    test()
    
    res_dfs = []
    res_dfs.append(results_mt_window())
    res_dfs.append(results_mt_bonferroni())
    res_dfs.append(results_cp())
    
    #concat all results
    res = pd.concat(res_dfs, axis=0)
    
    return res

# run_dataset((60,30), (0.1,-0.1,0.02), True)

#RUN ALL DATASETS
    
amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]

def run():
    results_lat = []
    for amp in amplitudes:
        for nf in noise_filters:
            for bpf in band_pass_filtering:
                res = run_dataset(amp, nf, bpf)
                
                res['amplitude'] = str(amp)
                res['noise'] = "high" if (nf[0] == 0.1) else "low" 
                res['band_pass'] = bpf #str(bpf)
                
                results_lat.append(res) 
                
    #save cummulated results to df
    results_df = pd.concat(results_lat, axis=0)
    
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

    dataframe_file = 'results_lat.csv'
    results_df.to_csv(dataframe_file, index = False)

#STATISTICS
#load analysed results
def load_final_results():
    dataframe_file = 'results_lat.csv'
    data = pd.read_csv(dataframe_file)
    
    #remove tests where no clusters were identified (and print)
    #print('NO CLUSTERS FORMED', (data[data['total'] == 0]).shape[0])
    
    #print(data.shape[0])
    data = data[data['total'] > 0]
    #print(data.shape[0])
    
    return data

#calcualte statistics on results
def get_stats(): 
    
    # SETUP
    #load final results
    data = load_final_results()

    # expected global results
    data['expected'] = np.where(data['condition'] == 'lat_baseline', False, True) 
    
    methods = data['method'].unique()
    
    print(methods, data['condition'].unique())

    #splitting data
    methods = stats.split_data(data, 'method')

    #directories
    stats_dir = "statistics_lat"
    fm.do_dir(stats_dir)
    
    # stats 
    
    #between methods
    
    #local stats
    stats.compare_methods_conds_local(stats_dir, methods)
    
    #global metrics
    stats.compare_methods_conds_global(stats_dir, methods)
    
    #FDR
    stats.compare_FDR_conds_local(stats_dir, methods)

    #within methods & conditions (vars)
    
    
    for m_name, m_data in methods.items():
        
        #create directory
        stats_m_dir = stats_dir + '\\' + m_name
        fm.do_dir(stats_m_dir)
        
        for i in stats.independent_vars:

            #create directory
            stats_i_dir = stats_m_dir + '\\' + i
            fm.do_dir(stats_i_dir)
        
            mi_data = stats.split_data(m_data, i)
            
            #local stats
            stats.compare_vars_conds_local(stats_i_dir, mi_data, m_name, i)
            
            #global metrics
            stats.compare_vars_conds_global(stats_i_dir, mi_data, m_name, i)
            
            #FDR
            stats.compare_vars_FDR_conds_local(stats_i_dir, mi_data, m_name, i)
            
            #plots
            stats.plots_vars_conds_local(stats_i_dir, m_data, m_name, i)
            
            #testats
            #stats.test_diff_conds_local(stats_i_dir, m_data, m_name, i)

run()
get_stats()
