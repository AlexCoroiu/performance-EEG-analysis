# -*- coding: utf-8 -*-

import mne
import numpy as np

#run variables

#simulation
DATA_DIR = "data_amp42"
AMP = (40,20)

#constants

RAWS_DIR = DATA_DIR + '\\' + "raws"
EPOS_DIR = DATA_DIR + '\\' + "epos"
EVOS_DIR = DATA_DIR + '\\' + "evos"
EPO_DFS_DIR = DATA_DIR + '\\' + "epo_dfs"
EVO_DFS_DIR = DATA_DIR + '\\' + "evo_dfs"
DATA_POINTS = DATA_DIR + '\\' + "dps"

NR_PARTICIPANTS = 20
NR_TRIALS = 20

# MONTAGE
SFREQ = 250 #samples per s
MONTAGE = 'standard_1020'  

#not including mastoids

CHANNELS_86 = ['Fp1', 'Fpz', 'Fp2', 
                'AF9', 'AF7', 'AF5', 'AF3', 'AF1', 'AFz', 'AF2', 'AF4', 'AF6', 'AF8', 'AF10', 
                'F9', 'F7', 'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', 'F10', 
                'FT9', 'FT7', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 'FT10', 
                'T9', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'T8', 'T10', 
                'TP9', 'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'TP8', 'TP10', 
                'P9', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'P10', 
                'PO9', 'PO7', 'PO5', 'PO3', 'PO1', 'POz', 'PO2', 'PO4', 'PO6', 'PO8', 'PO10', 
                'O1', 'Oz', 'O2', 
                'O9', 'Iz', 'O10']

CHANNELS_64 = ['Fp1', 'Fpz', 'Fp2', 
                'AF7', 'AF3', 'AFz', 'AF4', 'AF8', 
                'F7', 'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', 
                'FT7', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 
                'T9', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'T8', 'T10', 
                'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 'TP8',
                'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8',
                'PO7', 'PO3', 'POz', 'PO4', 'PO8',
                'O1', 'Oz', 'O2', 
                'Iz']

CHANNELS_31 = ['Fp1', 'Fpz', 'Fp2', 
                'F7', 'F3', 'Fz', 'F4', 'F8', 
                'FT7', 'FC3', 'FCz', 'FC4', 'FT8',
                'T7', 'C3', 'Cz', 'C4', 'T8', 
                'TP7', 'CP3', 'CPz', 'CP4', 'TP8',
                'P7', 'P3', 'Pz', 'P4', 'P8', 
                'O1', 'Oz', 'O2']

CHANNELS_VISUAL = ['P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8',
            'PO7', 'PO3', 'POz', 'PO4', 'PO8',
            'O1', 'Oz', 'O2', 
            'Iz']

CHANNELS_OCCIPITAL = ['PO7', 'PO3', 'POz', 'PO4', 'PO8',
            'O1', 'Oz', 'O2']

MEASURE_ELECTRODES = ['Oz', 'Fpz', 'T7', 'T8']

#info
INFO = mne.create_info(ch_names = CHANNELS_86,
                       sfreq = SFREQ,
                       ch_types = 'eeg')
INFO.set_montage(MONTAGE)

TSTEP = 1/SFREQ #250 samples in 1s

# ACTIVATION
TIMES = np.arange(100, dtype = np.float64) * TSTEP #[1,2...150]/250 ??
#WHYY 150??

EVENT_DURATION = 1*SFREQ #250 samples per event ==> 1 s

EVENT_IDS = {'baseline': 1, 
             'visual_right': 2, 
             'visual_left': 3}
EVENT_NRS = {1: 'baseline', 
             2: 'visual_right', 
             3: 'visual_left'}

EVENT_NAMES = EVENT_IDS.keys()

EVENTS = [] #base, activation, base, activation, base... activation

time = 0 #start

for i in range(0,NR_TRIALS):
    EVENTS.append([time,0,1]) #baseline
    time = time + EVENT_DURATION
    EVENTS.append([time,0,2]) #visual/right
    time = time + EVENT_DURATION
    EVENTS.append([time,0,1]) #baseline
    time = time + EVENT_DURATION
    EVENTS.append([time,0,3]) #visual/left
    time = time + EVENT_DURATION

EVENTS.append([time,0,1]) #baseline - IS IT NEEDED?

ACTIVATIONS = {
    'visual_right':
        [('G_occipital_sup-lh', AMP[0]), #mV
         ('G_occipital_sup-rh', AMP[1])
         ],
    'visual_left':
        [('G_occipital_sup-lh', AMP[1]),
         ('G_occipital_sup-rh', AMP[0])
         ]
}
    
#(6,3)
#(4,2)

ANNOTATION = 'aparc.a2009s'

BASE_REGION = 'occipital_sup'

BASE_LATENCY = 0
BASE_DURATION = 1
BASE_AMPLITUDE = 0

#for evoked
T_MIN = -0.5
T_MAX = 0.5

F_BAND = 10

DURATION = 0.2 #200ms +/- 50ms
IPSILATERAL_DELAY = 0.015 #contralateral delay + 15ms

#alpha rythm??

# Participant/Trial variable DISTs

#signal variables

#amplitude +/- 5mV
AMPLITUDE_VAR_PART_DIST = (0,2.5) #mean latency
AMPLITUDE_VAR_DIST = (0,2.5) 

#175ms +/- 50*ms (contralateral) wiht the shift from the function - 0.1
LATENCY = 0.175

LATENCY_VAR_PART_DIST = (0, 0.025) #mean latency
LATENCY_VAR_DIST = (0,0.025) 
#main peak N1 towards P2 transition

# participant differences, normally distributed or just random?

# PROPAGATION

#sample subject
SAMPLE_DATA_PATH = mne.datasets.sample.data_path()
SUBJECTS_DIR = SAMPLE_DATA_PATH + '\subjects'
SUBJECT = 'sample'

#source space
SS_SRC_FILE = 'ss-src.fif'
NEW_SRC = False #takes some time to generate, should be created only once
if NEW_SRC: #create new
    SRC = mne.setup_source_space(subject = SUBJECT,
                                 subjects_dir = SUBJECTS_DIR)
    mne.write_source_spaces(SS_SRC_FILE, SRC, overwrite = True)
else: #load existing from file
    SRC = mne.read_source_spaces(SS_SRC_FILE)
    
#forward model
FS_FWD_FILE = 'fs-avg-fwd.fif'
NEW_FWD = False #takes some time to generate, should be created only once
if NEW_FWD: #create new
    BEM_SURF = mne.make_bem_model(subject = SUBJECT,
                                  subjects_dir = SUBJECTS_DIR)
                                  #default conductivity (0.3, 0.006, 0.3) 
                                  
    BEM = mne.make_bem_solution(BEM_SURF)
    
    TRANS = 'fsaverage' 
    # 'fsaverage' built-in free surfer transformation
    # None identity matrix
                
    FWD = mne.make_forward_solution(info = INFO,
                                    src = SRC,
                                    trans = TRANS,
                                    meg = False,
                                    bem = BEM)
                                    
    
    mne.write_forward_solution(FS_FWD_FILE, FWD, overwrite = True)
else: #load existing from file
    FWD = mne.read_forward_solution(FS_FWD_FILE)

# NOISE
#noise covariance matrix
NOISE_COV = mne.make_ad_hoc_cov(info = INFO)

#infinite impulse response filter
#high pass filter for 0.1 Hz frequencies
NOISE_FILTER = (0.1,-0.1,0.02)
#the bigger the iir filter values, the less noise (signal-noise ratio)
#(0.1,-0.1,0.02)
#(0.2,-0.2,0.04)

# #noise levels variables
# #+/-0.1 ??? the lower the value, the more amp
# #smth related to the noise freq (check psd plot)
# #0.04 ???? the lower the value, the higehr noise freq

#fit_iir_model_raw????


# PROCESSING VARIABLES
#filtering or baselien correction?

#band pass
FILTER = (0.1, 30)

#baselien correction: a  type of high pass fitlering?
BASELINE = (T_MIN, 0) #or None

  
#ANALYSIS
SIGNIFICANCE = 0.05

CONDITION_TIME = T_MAX - 0
BASELINE_TIME = 0 - T_MIN
TOTAL_TIME = T_MAX - T_MIN


# SLIDING WINDOW

# has to be multiple of 4
TIME_WINDOW_SHORT = 0.008 #8 ms 4*2
TIME_WINDOW_MED = 0.02 #20 ms 4*5
TIME_WINDOW_LONG = 0.032 #32 ms 4*8
TIME_WINDOW_V_LONG = 0.044 # ms 4*11
    



