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

def create_concat_epo(epos):
    dataset = c.DATA_DIR

    concat_epo = mne.concatenate_epochs(epos)
    concat_epo_file =  dataset + '\\concat' + '_epo.fif'
    concat_epo.save(concat_epo_file, overwrite = True)
    
def load_concat_epo():
    dataset = c.DATA_DIR
    
    concat_epo_file =  dataset + '\\concat' + '_epo.fif'
    concat_epo = mne.read_epochs(concat_epo_file)
    
    return concat_epo
    
def create_epo_dfs(epos):
    # (part, condition, epoch, time, electrode, value)
    dataset = c.EPO_DFS_DIR
    
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    
    for p in range(c.NR_PARTICIPANTS):
        nr = str(p + 1)
        part = "part" + nr
        epo_part = epos[p]
        
        #save epoched as pandas dataframe
        dataframe = epo_part.to_data_frame(long_format = True)
        
        #print(dataframe.columns)
    
        dataframe['part'] = nr
        columns = ['part', 'condition', 'epoch', 'time', 'channel', 'value']
        dataframe = dataframe[columns]
        
        #save
        dataframe_file = dataset + '\\' + part + '.csv'
        dataframe.to_csv(dataframe_file)
    
def load_epo_dfs():
    dataset = c.EPO_DFS_DIR
    
    epo_dfs = []
    
    for p in range(c.NR_PARTICIPANTS):
        part = "part" + str(p + 1)
        
        epo_df_file = dataset +  '\\' + part + '.csv'
        epo_df_part = pd.read_csv(epo_df_file)
        
        epo_dfs.append(epo_df_part)
    
    return epo_dfs

def create_epo_concat_df(epo_dfs):
    dataset = c.DATA_DIR
    
    epo_dataframe = pd.concat(epo_dfs, axis=0) #very computationally heavy
    dataframe_file = dataset + '\\epo_dataframe' + '.csv'
    epo_dataframe.to_csv(dataframe_file)
    
    
def load_epo_concat_df():
    dataset = c.DATA_DIR
    
    dataframe_file = dataset + '\\epo_dataframe' + '.csv'
    epo_dataframe = pd.read_csv(dataframe_file, index = False)
    
    return epo_dataframe
    
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
    dataframe_file = dataset + '\\evo_dataframe' + '.csv'
    evo_dataframe.to_csv(dataframe_file, index = False)
    
def load_evo_concat_df():
    dataset = c.DATA_DIR
    
    dataframe_file = dataset + '\\evo_dataframe' + '.csv'
    evo_dataframe = pd.read_csv(dataframe_file)
    
    return evo_dataframe

def create_avg_evo(concat_epo):
    #create concatanated evokeds - population average
    dataset = c.DATA_DIR
    avg_evo = []
    
    for event in c.EVENT_NAMES:
            
        condition = concat_epo[event]
        
        #evoked data
        evoked = condition.average() #average or gfp
        
        avg_evo.append(evoked)
    
    avg_evo_file = dataset + '\\avg' + '_ave.fif'
    mne.write_evokeds(avg_evo_file, avg_evo)

def load_avg_evo():
    dataset = c.DATA_DIR
    
    avg_evo_file =  dataset + '\\avg' + '_ave.fif'
    avg_evo = mne.read_evokeds(avg_evo_file)
    
    return avg_evo

def create_avg_df(avg_evo):
    # (condition, time, electrode, value)
    
    dataset = c.DATA_DIR
    dfs = []
    
    for evoked in avg_evo:
        df = evoked.to_data_frame(long_format = True)
        condition = evoked.comment
        df['condition'] = condition
        columns = ['condition', 'time', 'channel', 'value']
        df = df[columns]
        dfs.append(df)
        
    dataframe = pd.concat(dfs, axis=0)
    dataframe_file = dataset + '\\avg_df' + '.csv'
    dataframe.to_csv(dataframe_file)
    
def load_avg_df():
    dataset = c.DATA_DIR
    
    dataframe_file = dataset + '\\avg_df' + '.csv'
    avg_dataframe = pd.read_csv(dataframe_file)
    
    return avg_dataframe

def create_data_points(dataframe):
    
    data_points = dataframe[['time','channel']].drop_duplicates()
    
    dataset = c.DATA_POINTS
    if not os.path.exists(dataset):
        os.mkdir(dataset)

    #part x condition x time x electrode
    print(dataframe.head(5))
    print(dataframe.tail(5))
    
    #re-shape dataframe
    #part | time | condition | baseline | visual-left | visual-right
    wide_dataframe = dataframe.pivot(index=['part','time', 'channel'], 
                    columns='condition', 
                    values='value')
    
    print(wide_dataframe.head(5))
    print(wide_dataframe.tail(5))
    
    #descriptives
    wide_dataframe[c.EVENT_NAMES].describe()
    
    #split by time x electrode
    grouped_dataframe = wide_dataframe.groupby(by = ['time','channel'])
    print(grouped_dataframe.head(5))
    print(grouped_dataframe.tail(5))

    
    split_df = {}
    
    for i,row in data_points.iterrows():
        dp = (row['time'],row['channel'])
        group = grouped_dataframe.get_group(dp)
        split_df[dp] = group
    
    print(split_df)
    
    for dp in split_df:
        dataframe_file = dataset + '\\' + str(dp[0]) + "_" + dp[1] + '.csv'
        split_df[dp].to_csv(dataframe_file)
        
def load_data_points(dataframe):

    data_points = dataframe[['time','channel']].drop_duplicates()
    
    dataset = c.DATA_POINTS
    
    dps = {}
    
    for i,row in data_points.iterrows():
        dp = (row['time'],row['channel'])
        dp_file =  dataset + '\\' + str(dp[0]) + "_" + dp[1] + '.csv'
        dp_values = pd.read_csv(dp_file)
        dps[dp] = dp_values
    
    return dps
    

#%%PROCESSING

def process():
    raws = load_raws()
    
    create_epos(raws)
    epos = load_epos()
    
    create_concat_epo(epos)
    concat_epo = load_concat_epo()
    
    create_epo_dfs(epos)
    epo_dfs = load_epo_dfs()
    
    #create_epo_concat_df(epo_dfs) #computationally heavy
    
    create_evos(epos)
    evos = load_evos()
    
    create_evo_dfs(evos)
    evo_dfs = load_evo_dfs()
    
    create_evo_concat_df(evo_dfs)
    
    create_avg_evo(concat_epo)
    avg_evo = load_avg_evo()
    
    create_avg_df(avg_evo)
    
    dataframe = load_evo_concat_df()
    create_data_points(dataframe)
    

process()


    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    