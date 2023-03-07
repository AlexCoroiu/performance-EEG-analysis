# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

import numpy as np
import mne
import constants as c
import file_manager as fm

#SIMULATION FUNCTIONS

#simulate ERP wave
def simulate_wave(times, latency, duration, f_band):
    time_latency = times - latency
    sinusoid = np.sin(2 * np.pi * f_band * time_latency)
    #time latency has to be used here for the actual time delay
    var = 0.2 * duration #width of the gaussian function 
    sd = var ** 2
    shift = var/4
    
    #duration changes than the shape of the signal changes as well --> invariable duration

    #position of the gaussian max
    gf = np.exp(-(time_latency + shift) ** 2 / #+/- gf is left/right of sin 0 (where polarity changes)  
                (sd*2)) #68% interval
    
    #if duration bigger than latency than you get a shift too much to the right
    
    #!position of the gf compared to the sinusoid

    wave = 1e-10 * sinusoid * gf
    return wave

#add 0 wave to baseline data
def simulate_base(event, src_sim):
    waveform = simulate_wave(c.TIMES, c.BASE_LATENCY, 
                             c.BASE_DURATION, c.F_BAND)

    src_sim.add_data(c.BASE_LABEL,
                     c.BASE_AMPLITUDE*waveform,
                     event)

#add ERP wave to visual stimulus data
def simulate_activation(cond, event, src_sim, latency_var, amplitude_var):
    for hemi in range(2):
        region = c.ACTIVATIONS[cond][hemi][0]
        label = c.VISUAL_LABELS[region]
        
        #latency
        stimuli_side = cond.split('_')[1][0]
        hemi_side = label.hemi[0]
        
        hemi_latency = c.LATENCY + latency_var
        
        if stimuli_side == hemi_side: #ipsilateral            
            hemi_latency = hemi_latency + c.IPSILATERAL_DELAY

        #simualte wave
        waveform = simulate_wave(c.TIMES, hemi_latency, c.DURATION, c.F_BAND)
            
        #amplitude
        hemi_amplitude = c.ACTIVATIONS[cond][hemi][1] + amplitude_var
        
        #add wave
        src_sim.add_data(label,
                         hemi_amplitude * waveform,
                         event)
        
        #print(stimuli_side, hemi_side, hemi_latency, hemi_amplitude)    

#simulate data for one participant
def simulate_data(part_nr):
    
    #SIGNAL
    
    #events data - new one for each participant
    src_sim = mne.simulation.SourceSimulator(src = c.SRC, 
                                             tstep = c.TSTEP)
    
    for event in c.EVENTS:
        time = event[0]
        event_id = event[2]
        condition = c.EVENT_NAMES[event_id]
        if condition == 'baseline':
            simulate_base([event], src_sim)
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
        
            
            simulate_activation(condition, [event], src_sim, 
                                latency_var, amplitude_var)
    
    #add data
    raw_sim = mne.simulation.simulate_raw(c.INFO, 
                                          src_sim, 
                                          forward=c.FWD)

    
    #add noise
    mne.simulation.add_noise(raw_sim, c.NOISE_COV,
                              iir_filter = c.NOISE_FILTER) 
    #random_state: default, different every time
    

    return raw_sim

#simulate data for all participants
def simulate_raws():
    dataset = fm.RAWS_DIR
    fm.do_dir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part_nr = p + 1
        part = "part" + str(part_nr)
        raw = simulate_data(part_nr)
        raw_file = dataset + '\\' + part + '_eeg.fif'
        raw.save(raw_file, overwrite = True)

#DATA SIMULATE    
def simulate():
    dataset = fm.SIMULATION_DIR
    fm.do_dir(dataset)
    
    #simulation
    simulate_raws()
    

    