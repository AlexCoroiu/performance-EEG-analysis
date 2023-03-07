# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

#setup
import mne
import numpy as np
import file_manager as fm
import pandas as pd
import constants as c
import preparation as prep


#make electrode adjacency matrix
def get_channel_adjacency(electrodes):
    #chnnel positions in 2D
    adjacency, channels = mne.channels.find_ch_adjacency(c.INFO, 'eeg')
    
    #select only used electrodes
    e_ids = [channels.index(e) for e in electrodes]
    adjacency = adjacency[e_ids][:, e_ids]
    #print(adjacency)
    
    return adjacency


#run cluster permutation method
def cluster_permutations(data):
    #get unique windows and electrodes from data
    windows = data['time'].unique()
    nr_windows = len(windows)
    electrodes = data['channel'].unique()
    nr_electrodes = len(electrodes)
    
    shape = (c.NR_PARTICIPANTS, nr_windows, nr_electrodes)
    
    #electrode adjacency matrix
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
    
    t_stats, clusters, p_val_clusters, max_results = mne.stats.spatio_temporal_cluster_1samp_test(X = data_array, 
                                                                                                  adjacency = adjacency,
                                                                                                  out_type = 'mask')
   
    #print('Clusters\n', clusters)
    #print('P_vals\n', p_val_clusters)
    
    results = []
    
    #cluster id lists
    cluster_ids = range(len(clusters))
    
    for cluster_id in cluster_ids:
        
        cluster = clusters[cluster_id]
        
        #print(cluster.shape)
        shape = (nr_windows*nr_electrodes, 1)
        
        #relate to time and channel
        cluster_df = pd.DataFrame(data = cluster,
                                  index = windows,
                                  columns = electrodes)
        
        cluster_df.index.names = ['time']

        #print(cluster_df) #matrix
        
        #select data_points in cluster
        cluster_name = 'cluster_' + str(cluster_id+1)
        cluster_df = cluster_df.melt(ignore_index = False,
                                     var_name = 'channel',
                                     value_name = cluster_name)
        
        cluster_df = cluster_df.reset_index()
        
        cluster_df = cluster_df[cluster_df[cluster_name] == True]
        
        cluster_df = cluster_df[['time', 'channel']]
        
        #print(cluster_df)
        
        data_points = cluster_df.values.tolist()
        
        #print(cluster_name, data_points)
        
        #significance
        
        p_val = p_val_clusters[cluster_id]
        
        crit_p_val = c.SIGNIFICANCE
        
        significant =  p_val < crit_p_val
        
        results.append([cluster_name, data_points, p_val, crit_p_val, significant])
        
        cluster_id += 1
    
    results_df = pd.DataFrame(results, 
                              columns =['cluster', 'data_points', 
                                        'p_val', 'crit_p_val', 'significant'])
    
    return results_df
    

#run method for a specific dataset
def test_condition(window_size, time, density, local, cond):
    window_ms = int(window_size*1000)
    dir_name = 'win' + str(window_ms) + '_time' + str(time) + '_dens' + str(density) + '_loc' + str(local)
    dataset = fm.ANALYSED_DIR + '\\' + dir_name
    fm.do_dir(dataset)
    
    #load prepped data
    data = prep.load_test_dfs(window_size, time, density, local) 
    #for all test conditions
    data_cond = data[cond]

    results = cluster_permutations(data_cond)
    #save
    dataframe_file = dataset + '\\' + cond + '_cp.csv'
    results.to_csv(dataframe_file, index = False)
    
#run for all datasets
def test():       
    dataset = fm.ANALYSED_DIR
    fm.do_dir(dataset)
    
    for w in c.WINDOW_SIZE:
        for t in c.TIME_INTERVAL:
            for d in c.DENSITY.keys():
                for l in c.LOCAL:
                    for cond in c.TEST_CONDITIONS:
                        print('...TESTING CP',w,t,d,l,cond)
                        test_condition(w,t,d,l,cond)  

# fm.set_up((80,40), (0.2,-0.2,0.04), True) 
# c.set_up((80,40), (0.2,-0.2,0.04), True)
# test_condition(0.004, 86, False, 'vs_left')
    
