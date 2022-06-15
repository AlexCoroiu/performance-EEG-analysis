# -*- coding: utf-8 -*-


# setup
import mne
import constants as c
import simulation as sim
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import processing

# SIMULATION statistics: amplitude & latency

def sim_var_statistics(amplitudes, latencies):
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
    
def sim_var_vizualization(amplitudes, latencies):
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
    
def explore_sim_variables():
    #open files
    latencies, amplitudes = sim.load_generated_variables()
    sim_var_statistics()
    sim_var_vizualization()

#DATAFRAME statistics

#population level 

#participant level

#VISUALZIE

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

#times
PLOT_TIMES = np.arange(0.08, 0.28, 0.04)

#VIZUALIZE participant level

def mne_part_level(part, raws, epos, evos):
    #sphere model for topographic representation
    sphere = make_top_sphere(epos[part]) #based on 1st part
    
    raws[part].pick(picks = c.CHANNELS_OCCIPITAL).plot(duration = 4)
    
    epos[part].plot_psd()
    #epoched.plot_psd_topomap()
    
    avg_evo_conditions = dict(zip(c.CONDITIONS, evos[part]))
    
    for cond in c.CONDITIONS:
        
        #epoched data
        epochs_cond = epos[part][cond]
        
        epochs_cond.plot
    
        epochs_cond.plot_image(combine='mean')
    
    
        #evoked data
        evo_cond = avg_evo_conditions[cond]
        evo_cond.plot_topomap(times = PLOT_TIMES,
                            ch_type = 'eeg',
                            sphere = sphere)
        
        #evoked.plot(gfp = True)
        evo_cond.plot(picks = ['POz'], gfp=False)
        evo_cond.plot(picks = ['PO3'], gfp=False)
        evo_cond.plot(picks = ['PO4'], gfp=False)
        
    
    mne.viz.plot_compare_evokeds(evos[part],
                             legend='upper left', 
                             show_sensors='upper right')
    
    epos[part].pick(picks = c.CHANNELS_OCCIPITAL).plot(n_epochs = 4)

def explore_mne():
    #raws
    raws = processing.load_raws()
    
    #epos
    epos = processing.load_epos()
    
    #evos
    evos = processing.load_evos()
    
    mne_part_level(0, raws, epos, evos)
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    