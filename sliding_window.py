# -*- coding: utf-8 -*-
"""
Created on Mon May  9 11:53:22 2022

@author: User
"""

#%% setup
import mne
import constants as c
import numpy as np
import math
import pandas as pd
import processing
from scipy import stats
import os

#%% functions

## VARIABLES
cond1 = 'baseline'
cond2 = 'visual_right'

electrodes = c.CHANNELS_64
window_size = c.TIME_WINDOW_MED
time = c.CONDITION_TIME

time_windows = time/window_size

print(time, window_size, time_windows)

sig = c.SIGNIFICANCE

crit_p = math.sqrt(sig/((time_windows-1)*len(electrodes)))

print(crit_p)

test = "sliding_window_64_all"

#TODO see hwo to split test/condition 

results_dir = c.DATA_DIR + '\\' + test

# TEST ASSUMPTIONS

#1. independent observations: NO, 
#spatial smearing (signal at 2 electrodes is influenced by the same source)

#2. normal distribution (DV)

#box plots, violin plots
#histograms

#stats.shapiro(df['value' for condition])

#3. no outliers

# MULTIVARIATE TEST

# 1 test for each combination of time x electrode x part
# between conditions
# data from participants (within participant difference)

def create_ttest_results(dps):
    data = []
    
    for dp, dp_values in dps.items():
        ttest = stats.ttest_rel(dp_values[cond1], 
                                      dp_values[cond2])
    
        time = dp[0]
        channel = dp[1]
        
        data_entry = [time, channel, ttest[1]]
        data.append(data_entry)
        # results = results.append({
        #     'time': time,
        #     'channel': channel,
        #     'p_val': ttest[1]}, #only pvalue, not the t statistic
        #     ignore_index = True)
        
    results = pd.DataFrame(data)
    results.columns = ['time', 'channel', 'p_val']
    dataframe_file = results_dir + '\\results' + '.csv'
    results.to_csv(dataframe_file)
    
    
def load_ttest_results():
    
    dataframe_file = results_dir + '\\results' + '.csv'
    results = pd.read_csv(dataframe_file)
    
    return results
 
#-----------------------

def save_matrix(name, matrix):
    
    dataframe_file = results_dir + '\\' + name + '.csv'
    matrix.to_csv(dataframe_file, index = False)
    
def load_matrix(name):
    
    dataframe_file = results_dir + '\\' + name + '.csv'
    matrix = pd.read_csv(dataframe_file)
    
    # time (250) x electrode (86)
    
    return matrix

#-------------------------------
def create_matrix(results):
    matrix = results.pivot(index = 'time', 
                    columns='channel', 
                    values='p_val')
    matrix = matrix.reset_index()
    save_matrix('matrix', matrix)
    

def select_windows(matrix, window_size):
    windowed_matrix = matrix.copy(deep = True)
    
    windowed_matrix.drop(windowed_matrix[
        (windowed_matrix['time'] % window_size) != 0 ].index, inplace=True)
    
    save_matrix('windowed_matrix', windowed_matrix)
    
def select_electrodes(matrix, electrodes):
    density_matrix = matrix.copy(deep = True)
    
    channels = list(set(matrix.columns) - set(['time']))
    extra_electrodes = list(set(channels) - set(electrodes))
    
    density_matrix.drop(columns = extra_electrodes, inplace = True)
    save_matrix('density_matrix', density_matrix)
    
def create_crit_p_matrix(matrix):
    crit_p_matrix = matrix.copy(deep = True)
    
    channels = list(set(matrix.columns) - set(['time'])) #except 'time'
    times = matrix.index
    
    for time in times:
        for channel in channels:
            if matrix.at[time, channel] <= crit_p:
                crit_p_matrix.at[time, channel] = 1
            else:
                crit_p_matrix.at[time, channel] = 0
    
    save_matrix('crit_p_matrix', crit_p_matrix)
    
def slide_window(matrix):
    sliding_matrix = matrix.copy(deep = True)
    
    channels = list(set(matrix.columns) - set(['time'])) #except 'time'
    times = matrix.index
    
    last_time_i = len(times)-1
    
    for channel in channels:
        if not ((matrix.at[times[0], channel] == 1) 
            and (matrix.at[times[1], channel] == 1)):
            sliding_matrix.at[times[0], channel] = 0
        
        for i in range(1, last_time_i -1):
            if not ((matrix.at[times[i], channel] == 1) 
                and ((matrix.at[times[i-1], channel] == 1 
                or matrix.at[times[i+1], channel] == 1))):
                sliding_matrix.at[times[i], channel] = 0 
                
        if not ((matrix.at[times[last_time_i], channel] == 1) 
            and (matrix.at[times[last_time_i -1], channel] == 1)):
            sliding_matrix.at[times[last_time_i], channel] = 0
            
    save_matrix('sliding_matrix', sliding_matrix)
                
            
# def create sliding_window(matrix):
#     sliding_window = matrix.copy(deep = True)
    
#     for index, row in matrix.iterow():
#         if ()
        

    
#%% ANALYSIS

def analyse():
    #load
    dataframe = processing.load_evo_concat_df()
    dps = processing.load_data_points(dataframe)
    
    #analyze
    create_ttest_results(dps)
    results = load_ttest_results()
    create_matrix(results)
    matrix = load_matrix('matrix')
    print(matrix)
    select_windows(matrix, c.TIME_WINDOW_MED*1000)
    windowed_matrix = load_matrix('windowed_matrix')
    print(windowed_matrix)
    select_electrodes(windowed_matrix, electrodes)
    density_matrix = load_matrix('density_matrix')
    print(density_matrix)
    create_crit_p_matrix(density_matrix)
    crit_p_matrix = load_matrix('crit_p_matrix')
    print(crit_p_matrix)
    slide_window(crit_p_matrix)
    sliding_matrix = load_matrix('sliding_matrix')
    print(sliding_matrix)

analyse()

