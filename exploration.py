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

# SIMULATION statistics: amplitude & latency (part + event var)

def sim_var_statistics(gen_vars):
    
    for var, data in gen_vars.items():
        #population level
        print(data['var'].describe())
        
        #condition level
        print(data.groupby('condition')['var'].describe())
        
        #event level
        print(data.groupby('time')['var'].describe())
        
        #participant level
        print(data.groupby('part')['var'].describe())
    
def sim_var_vizualization(gen_vars):
    
    for var, data in gen_vars.items():
        #density plots condition
        plot = sb.displot(data, x = 'var', row = 'condition')
        plt.show()

        #violin plots participant
        plot = sb.violinplot(data = data,
                      x = 'part', y = 'var')
        plt.show()
        
        #violin plots condition x participant
        plot = sb.FacetGrid(data, row = 'condition')
        plot = plot.map(sb.violinplot,
                 data = data,
                 x = 'part', y = 'var')
        plt.show()
        
        #violing plots event x participant
    
def explore_sim_variables():
    gen_vars = {'amplitude': c.AMP_VARS, 
                'latency': c.LAT_VARS}
    sim_var_statistics(gen_vars)
    sim_var_vizualization(gen_vars)

#DATAFRAME statistics

#population level 

#participant level

#condition level

#VIZUALIZATION HELPERS

#sphere for topographies
def make_topo_sphere(epoched): #digital montage for each participant
    montage = epoched.get_montage()
    # print(montage)
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
    sphere = make_topo_sphere(epos[part]) #based on 1st part
    
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
                            ch_type = 'eeg')
        
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
    
    mne_part_level(0, raws, epos, evos) #part 1
    
def explore():
    explore_sim_variables()
    #explore_mne()
    

explore()
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    