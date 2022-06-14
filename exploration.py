# -*- coding: utf-8 -*-


#%% setup
import mne
import constants as c
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

#%% GENERATION statistics: amplitude & latency

#open files
def load_generation_statistics():
    dataset = c.DATA_DIR
    
    dataframe_file = dataset + '\\amplitudes' + '.csv'
    amplitudes = pd.read_csv(dataframe_file)
    
    dataframe_file = dataset + '\\latencies' + '.csv'
    latencies = pd.read_csv(dataframe_file)
    
    return amplitudes, latencies

amplitudes, latencies = load_generation_statistics()

def generation_statistics():
    print(amplitudes.head(5))
    print(latencies.head(5))

    #population level
    print(amplitudes['amplitude'].describe())
    print(latencies['latency'].describe())
    
    #condition level
    print(amplitudes.groupby('condition')['amplitude'].describe())
    print(latencies.groupby('condition')['latency'].describe())
    
    #participant level
    print(amplitudes.groupby('part')['amplitude'].describe())
    print(latencies.groupby('part')['latency'].describe())
    
#generation_statistics()
    
def generation_vizualization():
    #density plots condition
    sb.displot(latencies, x = 'latency', row = 'condition')
    plt.show()
    sb.displot(amplitudes, x = 'amplitude', row = 'condition')
    plt.show()
    
    #violin plots participant
    sb.violinplot(data = amplitudes,
                  x = 'part', y = 'amplitude')
    plt.show()
    
    sb.violinplot(data = latencies,
             x = 'part', y = 'latency')
    plt.show()
    
    
    #violin plots condition x participant
    plot = sb.FacetGrid(amplitudes, row = 'condition')
    plot.map(sb.violinplot,
             data = amplitudes,
             x = 'part', y = 'amplitude')
    plt.show()
    
    plot = sb.FacetGrid(latencies, row = 'condition')
    plot.map(sb.violinplot,
             data = latencies,
             x = 'part', y = 'latency')
    plt.show()
    
generation_vizualization()
    

#%% LOAD DATA

import processing

#raws
raws = processing.load_raws()

#epos
epos = processing.load_epos()

#evos
evos = processing.load_evos()

#epos_dfs
epo_dfs = processing.load_epo_dfs()

#evos_dfs
evo_dfs = processing.load_evo_dfs()
    
#load epoched dataframe 

#epo_dataframe = processing.load_epo_concat_df() #computationally heavy

#load evoked dataframe
evo_dataframe = processing.load_evo_concat_df()

#epo pop
concat_epos = processing.load_concat_epo()

#evo pop
avg_evo = processing.load_avg_evo()

#df pop
avg_df = processing.load_avg_df()

#%%DATAFRAME statistics

#population level 

#participant level


#-------------------------------------------




#---------------------------------------------

#%%VISUALZIE

#VIZUALIZATION HELPERS

#sphere for topographies
def make_top_sphere(epoched): #digital montage for each participant
    montage = epoched.get_montage()
    print(montage)
    ch_pos = montage.get_positions()['ch_pos']
    pos = np.stack([ch_pos[ch] for ch in c.MEASURE_ELECTRODES])
    radius = np.abs(pos[[2, 3], 0]).mean() #radius t7-t8
    x = pos[0, 0]
    y = pos[-1, 1]
    z = pos[:, -1].mean()
    sphere = (x,y,z,radius)
    return sphere

#sphere model for topographic representation
sphere = make_top_sphere(concat_epos)

#times
PLOT_TIMES = np.arange(0.08, 0.28, 0.04)

def mne_pop_level():
    concat_epos.plot_psd()
    #epoched.plot_psd_topomap()
    
    avg_evo_conditions = dict(zip(c.EVENT_NAMES, avg_evo))
    
    for event in c.EVENT_NAMES:
        
        #epohed data
        condition = concat_epos[event]
        
        condition.plot
    
        condition.plot_image(combine='mean')
    
    
        #evoked data
        condition = avg_evo_conditions[event]
        condition.plot_topomap(times = PLOT_TIMES,
                            ch_type = 'eeg',
                            sphere = sphere)
        
        #evoked.plot(gfp = True)
        condition.plot(picks = ['POz'], gfp=False)
        condition.plot(picks = ['PO3'], gfp=False)
        condition.plot(picks = ['PO4'], gfp=False)
        
    
    mne.viz.plot_compare_evokeds(avg_evo,
                             legend='upper left', 
                             show_sensors='upper right')


#VIZUALIZE participant level

def mne_part_level():
    i = 0 #part nr. 1
    
    raws[i].pick(picks = c.CHANNELS_OCCIPITAL).plot(duration = 2)
    
    epos[i].plot_psd()
    #epoched.plot_psd_topomap()
    
    avg_evo_conditions = dict(zip(c.EVENT_NAMES, evos[i]))
    
    for event in c.EVENT_NAMES:
        
        #epohed data
        condition = epos[i][event]
        
        condition.plot
    
        condition.plot_image(combine='mean')
    
    
        #evoked data
        condition = avg_evo_conditions[event]
        condition.plot_topomap(times = PLOT_TIMES,
                            ch_type = 'eeg',
                            sphere = sphere)
        
        #evoked.plot(gfp = True)
        condition.plot(picks = ['POz'], gfp=False)
        condition.plot(picks = ['PO3'], gfp=False)
        condition.plot(picks = ['PO4'], gfp=False)
        
    
    mne.viz.plot_compare_evokeds(evos[i],
                             legend='upper left', 
                             show_sensors='upper right')

# mne_pop_level()
# mne_part_level()
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    