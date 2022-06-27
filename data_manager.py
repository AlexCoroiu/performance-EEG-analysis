# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:45:01 2022

@author: User
"""

import os.path
import mne

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

def set_up(dataset):
    
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

