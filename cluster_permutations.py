# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:33:27 2022

@author: User
"""

#setup
import mne
import numpy as np
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
    electrodes = data['channel'].unique()
    nr_windows = len(windows)
    nr_electrodes = len(electrodes)
    
    shape = (c.NR_PARTICIPANTS, nr_windows, nr_electrodes)
    
    #channel adjacency matrix
    adjacency = get_channel_adjacency(electrodes)

    #from dataframe to NP multidimensional array
    
    # print(data.shape)
    # print(data.head(nr_electrodes))
    data = data.set_index(['part', 'time', 'channel'])
    data_array = data.to_numpy()

    data_array = np.reshape(data_array, shape)
    # print(data_array.shape)
    # print(data_array[0][0])
    
    #test mean == 0, 2 sided
    #for each time x electrode
    #default treshold corresponding to 0.05 p-value
    

    t_results, clusters, p_val_clusters, max_results = mne.stats.spatio_temporal_cluster_1samp_test( X = data_array, adjacency = adjacency)
    
    #select significant clusters
    sig_clusters_ids = np.where(p_val_clusters < c.SIGNIFICANCE)[0]
    sig_clusters = [clusters[i] for i in sig_clusters_ids]
    t_sig_clusters = [t_results[c] for c in sig_clusters]
    
    #significant_points = cluster_pv.reshape(t_obs.shape).T < .05
    print(sig_clusters)
    print(t_sig_clusters)
    
    #visualize

def test():           

    #for all prepared data                                 
    window_size = 0.02
    density = 64
    local = True  
    
    #load prepped data
    data = prep.load_test_dfs(window_size, density, local) 
    #for all test conditions
    data_cond = data['vs_left']

    cluster_permutations(data_cond)
    
test()
    
    
