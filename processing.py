# -*- coding: utf-8 -*-

import mne
import constants as c
import numpy as np
import pandas as pd
import os

def load_raws():
    dataset = c.RAWS_DIR
    raws = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        
        #raw
        raw_file = dataset + '\\' + part + '_eeg.fif'
        raw_part = mne.io.read_raw(raw_file, preload = True) #preloading for filtering
        raws.append(raw_part)
    
    return raws
    
def create_epos(raws):
    dataset = c.EPOS_DIR
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        raw_part = raws[p]
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
    dataset = c.EPOS_DIR
    epos = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        #epoched
        epoched_file =  dataset + '\\' + part + '_epo.fif'
        epoched_part = mne.read_epochs(epoched_file)
        epos.append(epoched_part)
    
    return epos

    
def create_evos(epos):
    dataset = c.EVOS_DIR
    
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        epo_part = epos[p]
        
        evoked_part = []
          
        for event in c.EVENT_NAMES:
            
            condition = epo_part[event]
            
            #evoked data
            evoked = condition.average() #average or gfp
            
            evoked_part.append(evoked)
        
        evoked_file = dataset + '\\' + part + '_ave.fif'
        mne.write_evokeds(evoked_file, evoked_part)
    
def load_evos():
    dataset = c.EVOS_DIR
    evos = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        #evoked
        evoked_file =  dataset + '\\' + part + '_ave.fif'
        evoked_part = mne.read_evokeds(evoked_file)
        evos.append(evoked_part)
        
    return evos

def create_evo_dfs(evos):
    # (part, condition, time, electrode, value)
    dataset = c.EVO_DFS_DIR
    
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    
    for p in range(c.NR_PARTICIPANTS):
        nr = str(p + 1)
        part = "part" + nr
        evo_part = evos[p]
        
        dfs = []
        
        for evo in evo_part:
            
            df = evo.to_data_frame(long_format = True)
            condition = evo.comment
            df['part'] = nr
            df['condition'] = condition
            columns = ['part', 'condition', 'time', 'channel', 'value']
            df = df[columns]
            
            dfs.append(df)
        
        
        dataframe = pd.concat(dfs, axis=0)
        #print(dataframe.columns)
        
        #save
        dataframe_file = dataset + '\\' + part + '.csv'
        dataframe.to_csv(dataframe_file)
    
def load_evo_dfs():
    dataset = c.EVO_DFS_DIR
    evo_dfs = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        
        evo_df_file = dataset +  '\\' + part + '.csv'
        evo_df_part = pd.read_csv(evo_df_file)
        
        evo_dfs.append(evo_df_part)
    
    return evo_dfs
    
def create_evo_concat_df(evo_dfs):
    dataset = c.DATA_DIR
    
    evo_dataframe = pd.concat(evo_dfs, axis=0)
    dataframe_file = dataset + '\\evo_concat_df' + '.csv'
    evo_dataframe.to_csv(dataframe_file, index = False)
    
def load_evo_concat_df():
    dataset = c.DATA_DIR
    
    dataframe_file = dataset + '\\evo_concat_df' + '.csv'
    evo_dataframe = pd.read_csv(dataframe_file)
    
    return evo_dataframe

#DATA PROCESSING

def process():
    raws = load_raws()
    
    create_epos(raws)
    epos = load_epos()
    
    create_evos(epos)
    evos = load_evos()
    
    create_evo_dfs(evos)
    evo_dfs = load_evo_dfs()
    
    create_evo_concat_df(evo_dfs)
    #evo_concat_df = load_evo_concat_df()
    
    
process()


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    