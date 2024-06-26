# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

# setup
import mne
import constants as c
import file_manager as fm
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import processing

#DATA PARAMETERS: amplitude & latency (participant & event level variability)

#summary statistics
def sim_var_statistics(data, exp_dir):
    
    exp_dir = exp_dir + '\\stats'
    fm.do_dir(exp_dir)

    #population level
    df = pd.DataFrame(data['var'].describe())
    dataframe_file = exp_dir + '\\pop_lvl.csv'
    df.to_csv(dataframe_file)
    
    #condition level
    df = pd.DataFrame(data.groupby('condition')['var'].describe())
    dataframe_file = exp_dir + '\\cond_lvl.csv'
    df.to_csv(dataframe_file)
    
    #event/trial level
    df = pd.DataFrame(data.groupby('time')['var'].describe())
    dataframe_file = exp_dir + '\\trial_lvl.csv'
    df.to_csv(dataframe_file)
    
    #participant level
    df = pd.DataFrame(data.groupby('part')['var'].describe())
    dataframe_file = exp_dir + '\\part_lvl.csv'
    df.to_csv(dataframe_file)

#plots  
def sim_var_vizualization(data, exp_dir):
    exp_dir = exp_dir + '\\plots'
    fm.do_dir(exp_dir)
    
    #density plots
    plot = sb.displot(data, x = 'var')
    fig = plot.fig
    file = exp_dir + '\\density.png'
    fig.savefig(file)
    fig.clear()
    
    #density plots condition
    plot = sb.displot(data, x = 'var', row = 'condition')
    fig = plot.fig
    file = exp_dir + '\\cond_density.png'
    fig.savefig(file)
    fig.clear()

    #violin plots participant
    plot = sb.violinplot(data = data, x = 'part', y = 'var')
    plt.xlabel('Participant', fontsize = 20)
    plt.ylabel('Deviation', fontsize = 20)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    fig = plot.figure
    file = exp_dir + '\\violin.png'
    fig = plot.get_figure()
    fig.set(figwidth = 16)
    fig.set(figheight = 6)
    fig.savefig(file)
    fig.clear()
    
    #violin plots condition x participant
    plot = sb.FacetGrid(data, row = 'condition')
    plot = plot.map(sb.violinplot,
                    data = data,
                    x = 'part', y = 'var')
    fig = plot.fig
    file = exp_dir + '\\cond_violin.png'
    fig.set(figwidth = 8)
    fig.savefig(file)
    fig.clear()
    
#exploration data parameters
def explore_sim_variables(exp_dir):
    gen_vars = {'amplitude': c.AMP_VARS, 
                'latency': c.LAT_VARS}
    
    for var, data in gen_vars.items():
        var_dir = exp_dir + '\\' + var
        fm.do_dir(var_dir)
        
        sim_var_statistics(data, var_dir)
        sim_var_vizualization(data, var_dir)

#SIMUALTION RESULTS

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
def mne_part_level(part, raws, epos, evos, exp_dir):
    #sphere model for topographic representation
    electrode = 'POz'
    sphere = make_topo_sphere(epos[part])
    
    plot = raws[part].pick(picks = c.CHANNELS_OCCIPITAL).plot(duration = 4)
    file = exp_dir + '\\raw.png'
    plot.savefig(file)
    plot.clf()
    
    plot = epos[part].plot(picks = c.CHANNELS_OCCIPITAL, n_epochs = 4)
    file = exp_dir + '\\epo.png'
    plot.savefig(file)
    plot.clf()
    
    plot = epos[part].plot_psd(sphere = sphere)
    file = exp_dir + '\\epo_psd.png'
    plot.savefig(file)
    plot.clf()
    
    plot = epos[part].plot_psd_topomap(sphere = sphere)
    file = exp_dir + '\\epo_psd_topo.png'
    plot.savefig(file)
    plot.clf()

    avg_evo_conditions = dict(zip(c.CONDITIONS, evos[part]))
    
    for cond in c.CONDITIONS:
        
        cond_dir = exp_dir + '\\' + cond
        fm.do_dir(cond_dir)
        
        #epoched data
        epochs_cond = epos[part][cond]
        
        plot = epochs_cond.plot(picks = c.CHANNELS_OCCIPITAL)
        file = cond_dir + '\\epo.png'
        plot.savefig(file)
        plot.clf()
    
        [plot] = epochs_cond.plot_image(combine='mean') 
        #mean over all channels, can select jsut a specific one as well
        file = cond_dir + '\\epo_mean.png'
        plot.savefig(file)
        plot.clf()
        
        [plot] = epochs_cond.plot_image(picks = [electrode], combine='mean') 
        #mean for POz
        file = cond_dir + '\\epo_'  + electrode + '.png'
        plot.savefig(file)
        plot.clf()
    
        #evoked data
        evo_cond = avg_evo_conditions[cond]
        
        plot = evo_cond.plot_topomap(times = PLOT_TIMES,
                              sphere = sphere,
                              ch_type = 'eeg')
        file = cond_dir + '\\evo_topo.png'
        plot.savefig(file)
        plot.clf()
        
        #evo_cond.plot(gfp = True)
        plot = evo_cond.plot(picks = [electrode], gfp=False)
        file = cond_dir + '\\evo_' + electrode + '.png'
        plot.savefig(file)
        plot.clf()
        
    #compare averagee evo 
    [plot] = mne.viz.plot_compare_evokeds(evos[part],
                                          sphere = sphere,
                                          legend='upper left',
                                          show_sensors='upper right')
    
    file = exp_dir + '\\evo_conds.png'
    plot.savefig(file)
    plot.clf()
    
    #compare averagee evo for POz
    [plot] = mne.viz.plot_compare_evokeds(evos[part], picks = [electrode],
                                          sphere = sphere,
                                          legend='upper left',
                                          show_sensors='upper right')
    
    file = exp_dir + '\\evo_conds_' + electrode + '.png'
    plot.savefig(file)
    plot.clf()

#VIZUALIZE average
def mne_avg(sphere, raws, epos, evos, exp_dir):
    #sphere model for topographic representation
    electrode = 'POz'
    
    evos_conds = map(list,zip(*evos))
    evos_conditions = dict(zip(c.CONDITIONS, evos_conds))
    avg_evos = []
    
    for cond in c.CONDITIONS:
        
        evos_cond = evos_conditions[cond]
        avg_evo_cond = mne.grand_average(evos_cond)
        
        cond_dir = exp_dir + '\\' + cond
        fm.do_dir(cond_dir)
        
        #this condition from all participants
        plot = avg_evo_cond.plot_topomap(times = PLOT_TIMES,
                              sphere = sphere,
                              ch_type = 'eeg')
        file = cond_dir + '\\evo_topo.png'
        plot.savefig(file)
        plot.clf()
        
        #evo_cond.plot(gfp = True)
        plot = avg_evo_cond.plot(picks = [electrode], gfp=False)
        file = cond_dir + '\\evo_' + electrode + '.png'
        plot.savefig(file)
        plot.clf()
    
        avg_evos.append(avg_evo_cond)
        
    avg_evos_conditions = dict(zip(c.CONDITIONS,avg_evos))
    #compare average evo for POz
    [plot] = mne.viz.plot_compare_evokeds(avg_evos_conditions, picks = [electrode],
                                          sphere = sphere,
                                          legend='upper left',
                                          show_sensors='upper right')
    
    file = exp_dir + '\\evo_conds_' + electrode + '.png'
    plot.savefig(file)
    plot.clf()

#explore results
def explore_mne(exp_dir):
    #raws
    raws = processing.load_raws()
    
    #epos
    epos = processing.load_epos()
    
    #evos
    evos = processing.load_evos()
    
    part_nr = 0 #only for one part
    
    # part level
    # part_dir = exp_dir + '\\part' + str(part_nr+1)
    # fm.do_dir(part_dir)
    # mne_part_level(part_nr, raws, epos, evos, part_dir) 
    
    #average
    avg_dir =  exp_dir + '\\avg' 
    fm.do_dir(avg_dir)
    sphere = make_topo_sphere(epos[part_nr])
    mne_avg(sphere, raws, epos, evos, avg_dir)
    
    
#explore parameters and results for sepcific dataset
def explore():
    #directory
    exp_dir = "exploration"
    fm.do_dir(exp_dir)
    
    #explore_sim_variables(exp_dir)
    
    exp_dir = exp_dir + "\\data"
    fm.do_dir(exp_dir)
    
    #setup dataset
    amp = (60,20)
    noise = (0.1,-0.1,0.02)
    bpf = False
    fm.set_up(amp, noise, bpf)
    c.set_up(amp, noise, bpf)

    explore_mne(exp_dir)
    
explore()
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    