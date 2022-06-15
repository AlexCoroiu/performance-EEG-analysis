# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:36:41 2022

@author: User
"""

import constants as c
import pandas as pd
import data_manager as dtm
import processing as pross

def prepare_test_dfs(df, density, local):
    dir_name = 'dens' + str(density) + '_loc' + str(local)
    dataset = dtm.PREPARATION_DIR + '\\' + dir_name
    dtm.do_dir(dataset)
    
    #select electrodes
    electrodes = c.DENSITY[density]
    
    if local:
        electrodes = list(set(electrodes) & set(c.CHANNELS_VISUAL))
    
    channeled_df = df[df['channel'].isin(electrodes)] #shallow copy protection
    
    #split by test condition
    for cond in c.TEST_CONDITIONS:
        columns = ['part','time','channel', cond]
        cond_df = channeled_df[columns]
        
        #save
        dataframe_file = dataset + '\\' + cond + '.csv'
        cond_df.to_csv(dataframe_file, index = False)
    
    
def load_test_dfs(df, density, local):
    dir_name = 'dens' + density + '_loc' + local
    dataset = dtm.PREPARATION_DIR + '\\' + dir_name
    
    for cond in c.TEST_CONDITIONS:
        dataframe_file = dataset + '\\' + cond + '.csv'
        prepared = pd.read_csv(dataframe_file)
    
def prepare():
    dataset = dtm.PREPARATION_DIR 
    dtm.do_dir(dataset)
    
    df = pross.load_evo_df()
        
    #select post stimulus time interval
    post_stimulus_df = df[df['time']>=0]
    
    #format wide
    wide_df = post_stimulus_df.pivot(index=['part','time','channel'], 
                                    columns='condition', 
                                    values='value')
    
    #flatten heirarchical structure or extract from it
    wide_df = wide_df.reset_index()
    
    #calcualte difference between conditions into new column
    wide_df[c.LATERALIZATION] = wide_df['vs_right'] - wide_df['vs_left']

    print(wide_df.head(5))

    #prepare cond dfs
    for d in c.DENSITY.keys():
        for l in c.LOCAL:
            prepare_test_dfs(df, d, l)
        
        
        
        
        
        
        
    
    
    
    




