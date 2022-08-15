# -*- coding: utf-8 -*-

import mne
import constants as c
import numpy as np
import pandas as pd
import os
import data_manager as dtm

def load_raws():
    dataset = dtm.RAWS_DIR
    raws = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        
        #raw
        raw_file = dataset + '\\' + part + '_eeg.fif'
        raw_part = mne.io.read_raw(raw_file, preload = True) #preloading for filtering
        raws.append(raw_part)
    
    return raws
    
def create_epos(raws):
    dataset = dtm.EPOS_DIR
    dtm.do_dir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        raw_part = raws[p]
        if c.BAND_PASS_FILTERING:
            raw_part = raw_part.filter(c.FILTER[0],c.FILTER[1]) #band pass
        #print(raw_part)    
        
        #epoched (add event times)
        epoched_part = mne.Epochs(raw_part, 
                            events = c.EVENTS,
                            event_id = c.EVENT_IDS, 
                            proj = False,
                            baseline = c.BASELINE, #baseline correction
                            tmin = c.T_MIN, tmax = c.T_MAX)
        
        epoched_file = dataset + '\\' + part + '_epo.fif'
        
        epoched_part.save(epoched_file, overwrite = True)


def load_epos():
    dataset = dtm.EPOS_DIR
    epos = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        #epoched
        epoched_file =  dataset + '\\' + part + '_epo.fif'
        epoched_part = mne.read_epochs(epoched_file)
        epos.append(epoched_part)
    
    return epos

    
def create_evos(epos):
    dataset = dtm.EVOS_DIR
    dtm.do_dir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        epo_part = epos[p]
        
        evoked_part = []
          
        for cond in c.CONDITIONS:

            evoked_cond = epo_part[cond].average() #average or gfp
            evoked_part.append(evoked_cond)
        
        evoked_file = dataset + '\\' + part + '_ave.fif'
        mne.write_evokeds(evoked_file, evoked_part)
    
def load_evos():
    dataset = dtm.EVOS_DIR
    evos = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        #evoked
        evoked_file =  dataset + '\\' + part + '_ave.fif'
        evoked_part = mne.read_evokeds(evoked_file)
        evos.append(evoked_part)
        
    return evos

def create_evo_df(evos):
    # (part, condition, time, electrode, value)
    dataset = dtm.PROCESSING_DIR
    
    evo_dfs = []
    
    for p in range(c.NR_PARTICIPANTS):
        nr = str(p + 1)
        evo_part = evos[p]
        
        part_dfs = []
        
        for evo in evo_part:
            
            df = evo.to_data_frame(long_format = True)
            condition = evo.comment
            df['part'] = nr
            df['condition'] = condition
            columns = ['part', 'condition', 'time', 'channel', 'value']
            df = df[columns]
            
            part_dfs.append(df)
        
        part_dataframe = pd.concat(part_dfs, axis=0)
        #print(dataframe.columns)
        
        evo_dfs.append(part_dataframe)
        
    evo_dataframe = pd.concat(evo_dfs, axis=0)
    dataframe_file = dataset + '\\evo_concat_df' + '.csv'
    evo_dataframe.to_csv(dataframe_file, index = False)
    

def load_evo_df():
    dataset = dtm.PROCESSING_DIR
    
    dataframe_file = dataset + '\\evo_concat_df' + '.csv'
    evo_dataframe = pd.read_csv(dataframe_file)
    
    return evo_dataframe

#DATA PROCESSING

def process():
    dataset = dtm.PROCESSING_DIR
    dtm.do_dir(dataset)
    
    raws = load_raws()
    
    create_epos(raws)
    epos = load_epos()
    
    create_evos(epos)
    evos = load_evos()

    create_evo_df(evos)
    
    


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    