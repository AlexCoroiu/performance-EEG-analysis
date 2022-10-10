# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:45:01 2022

@author: User
"""

import os.path
import mne
import random
import pandas as pd

    
#MNE DATA

#sample subject
SAMPLE_DATA_PATH = mne.datasets.sample.data_path()
SUBJECTS_DIR = SAMPLE_DATA_PATH + '\subjects'
SUBJECT = 'sample'
        
#get signal location labels
def do_label(annotation, region):
    label = mne.read_labels_from_annot(SUBJECT, 
                                       annotation,
                                       subjects_dir = SUBJECTS_DIR,
                                       regexp = region,
                                       verbose = False)[0]
    return label

#get and create signal source file
def do_src(file, new):
    src = None
    if new: #create new
        src = mne.setup_source_space(subject = SUBJECT,
                                     subjects_dir = SUBJECTS_DIR)
        mne.write_source_spaces(file, src, overwrite = True)
    else: #load existing from file
        src = mne.read_source_spaces(file)
        
    return src

#get and create forward solution file
def do_fwd(file, new, trans, src, info):
    fwd = None
    if new: #create new
        bem_surf = mne.make_bem_model(subject = SUBJECT,
                                      subjects_dir = SUBJECTS_DIR)
                                      #default conductivity (0.3, 0.006, 0.3) 
                                      
        bem = mne.make_bem_solution(bem_surf)
        
        fwd = mne.make_forward_solution(info = info,
                                        src = src,
                                        trans = trans,
                                        meg = False,
                                        bem = bem)
                                        
        
        mne.write_forward_solution(file, fwd, overwrite = True)
    else: #load existing from file
        fwd = mne.read_forward_solution(file)
        
    return fwd

#get or create variables file

def do_vars(file, new, nr_parts, events, event_names, 
                part_dist, event_dist):
    gen_vars = None
     
    if new: #create new variable data
        gen_vars = [] #(part x non_baseline_events)
        for p in range(nr_parts):
            part_nr = p + 1
            
            part_var = random.gauss(part_dist[0],
                                     part_dist[1])
    
            for event in events:
                event_time = event[0]
                event_id = event[2]
                condition = event_names[event_id]
                if condition != 'baseline': #for vs_right, vs_left
                
                    #latency
                    event_var = random.gauss(event_dist[0],
                                             event_dist[1])
                    
                    var = part_var + event_var
                    
                    gen_vars.append([part_nr, part_var, 
                                     event_time, condition, event_var,
                                     var])
                            
        #save
        gen_vars_df = pd.DataFrame(data = gen_vars, 
                                   columns = ['part', 'part_var', 
                                              'time','condition',
                                              'event_var', 'var'])
        
        gen_vars_df.to_csv(file, index = False)
               
    else: #load existing from file
        gen_vars = pd.read_csv(file)
        
    return gen_vars
    
#RUN VARIABLES
#FILE STRUCTURE
   
DATA_DIR = ""

#simulation
SIMULATION_DIR = ""
RAWS_DIR = ""

# processing
PROCESSING_DIR = ""
EPOS_DIR = ""
EVOS_DIR = ""
EVO_DFS_DIR = ""

# preparation
PREPARATION_DIR = ""
DATA_POINTS = ""

#analysis & results
ANALYSED_DIR = ""

def do_dir(dataset):
    if not os.path.exists(dataset):
        os.mkdir(dataset)

def set_up(amplitude, noise_filter, band_pass_filtering):
    
    dataset = ('data_amp' + str(amplitude[0]) + str(amplitude[1]) 
               +'_noise' + str(noise_filter[0]) 
               + '_filter' + str(band_pass_filtering))
    
    dirs = globals()
    
    dirs['DATA_DIR'] = dataset
    do_dir(DATA_DIR)

    # simulation
    dirs['SIMULATION_DIR'] = DATA_DIR + '\\' + "simulated"
    dirs['RAWS_DIR'] = SIMULATION_DIR + '\\' + "raws"
    
    # processing
    dirs['PROCESSING_DIR'] = DATA_DIR + '\\' + "processed"
    dirs['EPOS_DIR'] = PROCESSING_DIR + '\\' + "epos"
    dirs['EVOS_DIR'] = PROCESSING_DIR + '\\' + "evos"
    dirs['EVO_DFS_DIR'] = PROCESSING_DIR + '\\' + "evo_dfs"
    
    # preparation
    dirs['PREPARATION_DIR'] = DATA_DIR + '\\' + "prepared"
    #dirs['DATA_POINTS'] = DATA_DIR + '\\' + "dps"
    
    # analysis
    dirs['ANALYSED_DIR'] = DATA_DIR + '\\' + "analysed"
    
    # results