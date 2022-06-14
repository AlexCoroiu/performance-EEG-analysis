import numpy as np
import mne
import random
import os
import constants as c
import matplotlib.pyplot as plt
import pandas as pd

#GENERATIOAN VARIABLES
generated_latencies = []
generated_amplitudes = []

#SIMULATION FUNCTIONS
def simulate_wave(times, latency, duration, f_band):
    time_latency = times - latency
    sinusoid = np.sin(2 * np.pi * f_band * time_latency)
    #time latency has to be used here for the actual time delay
    #plt.plot(times, sinusoid)
    #plt.show()
    var = 0.2 * duration #width of the gaussian function 
    sd = var ** 2
    shift = var/4
    
    #if duration changes than the shape of the signal changes as well --> invariable duration

    #position of the gaussian max
    gf = np.exp(-(time_latency + shift) ** 2 / #+/- gf is left/right of sin 0 (where polarity changes)  
                (sd*2)) #68% interval
    
    #duration bigger than altency than you ge ta shift too much to the right
    
    #!position of the gf comapred to the sinusoid
    #plt.plot(times,gf)
    #plt.show()
    wave = 1e-10 * sinusoid * gf
    #plt.plot(times, wave)
    #plt.show
    return wave

#test = simulate_wave(c.TIMES, 0.175, 0.2, 10)

def simulate_base(event, src_sim, f_band):
    label = mne.read_labels_from_annot(c.SUBJECT, 
                                       c.ANNOTATION,
                                       subjects_dir = c.SUBJECTS_DIR,
                                       regexp = c.BASE_REGION,
                                       verbose = False)[0]
    waveform = simulate_wave(c.TIMES, c.BASE_LATENCY, c.BASE_DURATION, 
                             f_band)

    src_sim.add_data(label,
                     c.BASE_AMPLITUDE*waveform,
                     event)
    
def simulate_activation(event_id, event, src_sim, 
                        latency_var, ipsilateral_delay, duration, amplitude_var,
                        f_band):
    for hemi in range(2):
        region = c.ACTIVATIONS[event_id][hemi][0]
        label = mne.read_labels_from_annot(c.SUBJECT, 
                                           c.ANNOTATION,
                                           subjects_dir = c.SUBJECTS_DIR,
                                           regexp = region,
                                           verbose = False)[0]
        
        #latency
        stimuli_side = event_id.split('_')[1][0]
        hemi_side = label.hemi[0]
        
        hemi_latency = c.LATENCY + latency_var
        
        if stimuli_side == hemi_side: #ipsilateral            
            hemi_latency = hemi_latency + ipsilateral_delay

        #simualte wave
        waveform = simulate_wave(c.TIMES, hemi_latency, duration, f_band)
            
        #amplitude
        hemi_amplitude = c.ACTIVATIONS[event_id][hemi][1] + amplitude_var
        
        #add wave
        src_sim.add_data(label,
                         hemi_amplitude * waveform,
                         event)
        
        #print(stimuli_side, hemi_side, hemi_latency, hemi_amplitude)    

def simulate_data(part_nr, part_latency_var, part_amplitude_var):
    
    #SIGNAL
    ipsilateral_delay = c.IPSILATERAL_DELAY
    duration = c.DURATION
    
    #events data - new one for each participant
    src_sim = mne.simulation.SourceSimulator(src = c.SRC, 
                                             tstep = c.TSTEP)
    
    for event in c.EVENTS:
        event_id = event[2]
        condition = c.EVENT_NRS[event_id]
        if condition == 'baseline':
            simulate_base([event], src_sim, c.F_BAND)
        else:
            #signal vairables
            #latency
            event_latency_var = random.gauss(c.LATENCY_VAR_DIST[0],
                                             c.LATENCY_VAR_DIST[1])
            latency_var = part_latency_var + event_latency_var
            
            generated_latencies.append([part_nr, condition, latency_var])
        
            #amplitude
            event_amplitude_var = random.gauss(c.AMPLITUDE_VAR_DIST[0],
                                               c.AMPLITUDE_VAR_DIST[1])
            amplitude_var = part_amplitude_var + event_amplitude_var
            
            generated_amplitudes.append([part_nr, condition, amplitude_var])
            
            simulate_activation(condition, [event], src_sim, 
                                latency_var, ipsilateral_delay,
                                duration,
                                amplitude_var,
                                c.F_BAND)
    
    #add data
    raw_sim = mne.simulation.simulate_raw(c.INFO, 
                                          src_sim, 
                                          forward=c.FWD)
    
    #raw_sim.plot(group_by = 'position', duration = 2)
    
    #add noise
    mne.simulation.add_noise(raw_sim, c.NOISE_COV,
                              iir_filter = c.NOISE_FILTER) 
    #random_state: default, different every time
    
    #raw_sim.plot(group_by = 'position', duration = 2)

    return raw_sim

def save_generated_variables():
    dataset = c.DATA_DIR
    
    #latency
    latency_df = pd.DataFrame(data = generated_latencies, 
                              columns = ['part', 'condition', 'latency'])
    dataframe_file = dataset + '\\latencies' + '.csv'
    latency_df.to_csv(dataframe_file, index = False)

    amplitude_df = pd.DataFrame(data = generated_amplitudes,
                                columns = ['part', 'condition', 'amplitude'])
    dataframe_file = dataset + '\\amplitudes' + '.csv'
    amplitude_df.to_csv(dataframe_file, index = False)

#DATA SIMULATE
def simulate():
    dataset = c.DATA_DIR
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    dataset = c.RAWS_DIR
    if not os.path.exists(dataset):
        os.mkdir(dataset)
    
    for p in range(c.NR_PARTICIPANTS):
        part_nr = p + 1
        part = "part" + str(part_nr)
        #raw data
        part_latency_var = random.gauss(c.LATENCY_VAR_PART_DIST[0],
                                    c.LATENCY_VAR_PART_DIST[1])
    
        part_amplitude_var = random.gauss(c.AMPLITUDE_VAR_PART_DIST[0],
                                          c.AMPLITUDE_VAR_PART_DIST[1])
        
        raw = simulate_data(part_nr, part_latency_var, part_amplitude_var)
        raw_file = dataset + '\\' + part + '_eeg.fif'
        raw.save(raw_file, overwrite = True)
    
    save_generated_variables()
    
simulate()

    