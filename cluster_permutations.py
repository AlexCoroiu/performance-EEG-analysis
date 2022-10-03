# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:33:27 2022

@author: User
"""

#setup
import mne
import numpy as np
import data_manager as dtm
import pandas as pd
import constants as c
import preparation as prep


def get_channel_adjacency(electrodes):
    #chnnel positions in 2D
    adjacency, channels = mne.channels.find_ch_adjacency(c.INFO, 'eeg')
    
    #select only used electrodes
    e_ids = [channels.index(e) for e in electrodes]
    adjacency = adjacency[e_ids][:, e_ids]
    #print(adjacency)
    
    return adjacency


def cluster_permutations(data):
    #get unique windows and electrodes from data
    windows = data['time'].unique()
    nr_windows = len(windows)
    electrodes = data['channel'].unique()
    nr_electrodes = len(electrodes)
    
    shape = (c.NR_PARTICIPANTS, nr_windows, nr_electrodes)
    
    #channel adjacency matrix
    adjacency = get_channel_adjacency(electrodes)

    #from dataframe to NP multidimensional array
    
    # print(data.shape)
    # print(data.head(nr_electrodes))
    data = data.set_index(['part', 'time', 'channel'])
    data_array = data.to_numpy()
    #print(data_array.shape)
    data_array = np.reshape(data_array, shape)
    #print(data_array.shape)
    # print(data_array[0][0])
    
    #test mean == 0, 2 sided
    #for each time x electrode
    #default treshold corresponding to 0.05 p-value
    

    t_stats, clusters, p_val_clusters, max_results = mne.stats.spatio_temporal_cluster_1samp_test( X = data_array, 
                                                                                                  adjacency = adjacency,
                                                                                                  out_type = 'mask')
    
    #select significant clusters
    sig_clusters_ids = np.where(p_val_clusters < c.SIGNIFICANCE)[0]
    sig_clusters = [clusters[i] for i in sig_clusters_ids]
    
    print(sig_clusters)
    
    results = pd.DataFrame(columns = ['time', 'channel'])
    print(results) #empty df

    i = 1

    for cluster in sig_clusters:
        print(cluster.shape)
        shape = (nr_windows*nr_electrodes, 1)
        
        cluster_df = pd.DataFrame(data = cluster,
                                  index = windows,
                                  columns = electrodes)
        
        cluster_df.index.names = ['time']

        #print(cluster_df) #matrix
        
        cluster_name = 'cluster' + str(i)
        cluster_df = cluster_df.melt(ignore_index = False,
                                     var_name = 'channel',
                                     value_name = cluster_name)
        i = i+1
    
        cluster_df = cluster_df[cluster_df[cluster_name] == True]
        
        print(cluster_df)
        
        #add as column to results
        results = pd.merge(results, cluster_df, how = 'outer', #union
                       left_on = ['time', 'channel'],
                       right_on = ['time', 'channel'])
        
    print(results)
        
    return results
        
    
    #return sig. cluster data points (times and electrodes)
    #dataframe format?
    

def test_condition(window_size, density, local, cond):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_dens' + str(density) + '_loc' + str(local)
    dataset = dtm.ANALYSED_DIR + '\\' + dir_name
    dtm.do_dir(dataset)
    
    #load prepped data
    data = prep.load_test_dfs(window_size, density, local) 
    #for all test conditions
    data_cond = data[cond]

    results = cluster_permutations(data_cond)
    #save
    dataframe_file = dataset + '\\' + cond + '_cp.csv'
    results.to_csv(dataframe_file, index = False)
    

def test():       
    dataset = dtm.ANALYSED_DIR
    dtm.do_dir(dataset)
    
    for w in c.WINDOW_SIZE:
        for d in c.DENSITY.keys():
            for l in c.LOCAL:
                for cond in c.TEST_CONDITIONS:
                    test_condition(w,d,l,cond)  

#test_condition(0.004, 86, False, 'difference')
    
