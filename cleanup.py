# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:33:27 2022

@author: Alexandra
"""

import file_manager as fm
import constants as c
import pandas as pd
import os

def rename_analysed(window_size, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file_old = dataset + '\\lateralization_' + cond + '_' + method + '.csv'
    dataframe_file_new = dataset + '\\lat_' + cond + '_' + method + '.csv'
    try: 
        os.rename(dataframe_file_old, dataframe_file_new)
    except:
        print('no file')
    
    

amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]


for amp in amplitudes:
    for nf in noise_filters:
        for bpf in band_pass_filtering: 
            #SETUP
            #file structure
            fm.set_up(amp, nf, bpf)
            
            #constants  
            c.set_up(amp, nf, bpf)
            
            for w in c.WINDOW_SIZE:
                for d in c.DENSITY.keys():
                    for l in c.LOCAL:
                        for cond in ['vs']:
                            rename_analysed(w, d, l, cond, 'mc_w')
                            rename_analysed(w, d, l, cond, 'mc_b')
                            

def remove_results( cond, method):
    dataset = fm.DATA_DIR
    
    dataframe_file_old = dataset + '\\results_lat_' + method + '.csv'
    try: 
        os.remove(dataframe_file_old)
    except:
        print('no file')
    
    

amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]


for amp in amplitudes:
    for nf in noise_filters:
        for bpf in band_pass_filtering: 
            #SETUP
            #file structure
            fm.set_up(amp, nf, bpf)
            
            #constants  
            c.set_up(amp, nf, bpf)
            
            for cond in ['lat','ERP']:
                remove_results(cond, 'mc_w')
                remove_results(cond, 'mc_b')
                
def remove_analyzed(window_size, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    
    dataframe_file_old = dataset + '\\lateralization_' + cond +  method + '.csv'
    try: 
        os.remove(dataframe_file_old)
    except:
        print('no file')
    
    

amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]


for amp in amplitudes:
    for nf in noise_filters:
        for bpf in band_pass_filtering: 
            #SETUP
            #file structure
            fm.set_up(amp, nf, bpf)
            
            #constants  
            c.set_up(amp, nf, bpf)
            
            for w in c.WINDOW_SIZE:
                for d in c.DENSITY.keys():
                    for l in c.LOCAL:
                        for cond in ['vs']:
                            remove_analyzed(w, d, l, cond, 'mc_w')
                            remove_analyzed(w, d, l, cond, 'mc_b')    
                            
def remove_prepared(window_size, density, local, cond, method):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.PREPARATION_DIR + '\\' + dir_name
    
    dataframe_file_old = dataset + '\\lateralization_' + cond +  '.csv'
    try: 
        os.remove(dataframe_file_old)
    except:
        print('no file')
    
    

amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]


for amp in amplitudes:
    for nf in noise_filters:
        for bpf in band_pass_filtering: 
            #SETUP
            #file structure
            fm.set_up(amp, nf, bpf)
            
            #constants  
            c.set_up(amp, nf, bpf)
            
            for w in c.WINDOW_SIZE:
                for d in c.DENSITY.keys():
                    for l in c.LOCAL:
                        for cond in ['baseline','vs']:
                            remove_prepared(w, d, l, cond, 'mc_w')
                            remove_prepared(w, d, l, cond, 'mc_b')                              