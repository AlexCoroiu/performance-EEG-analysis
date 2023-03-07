# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

import numpy as np
import mne
import constants as c
import file_manager as fm
import matplotlib.pyplot as plt
import simulation as sim


#SIMULATION FUNCTIONS

#visualize ERP wave 
def simulate_wave(times, latency, duration, f_band, viz_dir):
    time_latency = times - latency
    sinusoid = np.sin(2 * np.pi * f_band * time_latency)
    #time latency has to be used here for the actual time delay
    plt.plot(times, sinusoid)
    file = viz_dir + '\\sinusoid.png'
    plt.savefig(file)
    plt.clf()
    
    var = 0.2 * duration #width of the gaussian function 
    sd = var ** 2
    shift = var/4
    
    #duration changes than the shape of the signal changes as well --> invariable duration

    #position of the gaussian max
    gf = np.exp(-(time_latency + shift) ** 2 / #+/- gf is left/right of sin 0 (where polarity changes)  
                (sd*2)) #68% interval
    
    #if duration bigger than latency than you get a shift too much to the right
    
    #!position of the gf compared to the sinusoid
    plt.plot(times,gf)
    file = viz_dir + '\\gaussian.png'
    plt.savefig(file)
    plt.clf()
    
    wave = 1e-10 * sinusoid * gf
    plt.plot(times, wave*60)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    file = viz_dir + '\\wave.png'
    plt.savefig(file)
    plt.clf()

#visualize simulated data per participant
def simulate_data(part_nr, viz_dir):
    
    #SIGNAL
    
    #events data - new one for each participant
    src_sim = mne.simulation.SourceSimulator(src = c.SRC, 
                                             tstep = c.TSTEP)
    
    for event in c.EVENTS:
        time = event[0]
        event_id = event[2]
        condition = c.EVENT_NAMES[event_id]
        if condition == 'baseline':
            sim.simulate_base([event], src_sim)
        else:
            #signal vairables
            
            #latency
            latency_var = c.LAT_VARS.loc[(c.LAT_VARS['part'] == part_nr) & 
                                         (c.LAT_VARS['time'] == time), 
                                         'var'].iloc[0]
            
        
            #amplitude
            amplitude_var = c.AMP_VARS.loc[(c.AMP_VARS['part'] == part_nr) & 
                                           (c.AMP_VARS['time'] == time),
                                           'var'].iloc[0]
        
            
            sim.simulate_activation(condition, [event], src_sim, 
                                latency_var, amplitude_var)
    
    #add data
    raw_sim = mne.simulation.simulate_raw(c.INFO, 
                                          src_sim, 
                                          forward=c.FWD)
    
    raw_sim.pick(c.CHANNELS_OCCIPITAL)
    
    plot = raw_sim.plot(duration = 1.5, start = 0.5, 
                        show_scrollbars = False,
                        show_scalebars = False)
    file = viz_dir + '\\signal.png'
    plot.savefig(file)
    plot.clf()
    
    #add noise
    mne.simulation.add_noise(raw_sim, c.NOISE_COV,
                              iir_filter = c.NOISE_FILTER) 
    #random_state: default, different every time
    
    plot = raw_sim.plot(duration = 1.5, start = 0.5, 
                        show_scrollbars = False,
                        show_scalebars = False)
    file = viz_dir + '\\data.png'
    plot.savefig(file)
    plot.clf()

#vizualize for one specific dataset       
def vizualize():
    #directory
    viz_dir = "vizualization"
    fm.do_dir(viz_dir)
    
    #simulation
    simulate_wave(c.TIMES, 0.175, 0.2, 10, viz_dir)
    
    #setup dataset
    amp = (60,20)
    noise = (0.1,-0.1,0.02)
    bpf = False
    fm.set_up(amp, noise, bpf)
    c.set_up(amp, noise, bpf)
    
    #data
    simulate_data(1, viz_dir)
    

vizualize()