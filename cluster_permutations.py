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

#load prepped data

window = 0.004
window_ms = int(window*1000)
t_max = int(c.T_MAX*1000)
nr_windows = int(t_max/window_ms) + 1
density = 86
electrodes = c.DENSITY[density]
local = False
data = prep.load_test_dfs(window, density, local)

#test mean == 0, 2 sided
#for each time x electrode

#chnnel positions in 2D
adjacency, channels = mne.channels.find_ch_adjacency(c.INFO, 'eeg')
#select only used electrodes
e_ids = [channels.index(e) for e in electrodes]
adjacency = adjacency[e_ids][:, e_ids]


#default treshold corresponding to 0.05 p-value
diff = data['difference']
print(diff.shape)
print(diff.head(1))

diff = diff.set_index(['part', 'time', 'channel'])
print(diff.shape)
print(diff.head(1))

diff = diff.to_numpy()
print(diff.shape)
print(diff[0])

shape = (c.NR_PARTICIPANTS, nr_windows, density)
diff = np.reshape(diff, shape)
print(diff.shape)
print(diff[0])
#t_results, clusters, P_val_clusters, max_results = mne.stats.spatio_temporal_cluster_1samp_test( X = diff, adjacency = adjacency)
                                                                                                

