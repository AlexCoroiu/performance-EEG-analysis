# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

import mne
import numpy as np
import file_manager as fm

# DATA SIZE
NR_PARTICIPANTS = 20
NR_TRIALS = 20

# MONTAGE
SFREQ = 250 #samples per second
MONTAGE = 'standard_1020'

# (excluding mastoids)

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

CHANNELS_VISUAL = ['P9', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'P10', 
                    'PO9', 'PO7', 'PO5', 'PO3', 'PO1', 'POz', 'PO2', 'PO4', 'PO6', 'PO8', 'PO10', 
                    'O1', 'Oz', 'O2', 
                    'O9', 'Iz', 'O10']

# (total channels ∩ visual) to get visual channels for different densities

CHANNELS_OCCIPITAL = ['PO9', 'PO7', 'PO5', 'PO3', 'PO1', 'POz', 'PO2', 'PO4', 'PO6', 'PO8', 'PO10', 
                      'O1', 'Oz', 'O2']

# (total channels ∩ occipital) to get occipital channels for different densities

MEASURE_ELECTRODES = ['Oz', 'Fpz', 'T7', 'T8']

# info
INFO = mne.create_info(ch_names = CHANNELS_86,
                       sfreq = SFREQ,
                       ch_types = 'eeg')
INFO.set_montage(MONTAGE)

# SIGNAL

# time 
TSTEP = 1/SFREQ #1/250 of 1 second
TIMES = np.arange(100, dtype = np.float64) * TSTEP # [1...100]/250
EVENT_DURATION = 1*SFREQ #250 samples = 1 second

# events
CONDITIONS = ['baseline', 
              'vs_right', 
              'vs_left',]

INDEXES = [1,2,3]

EVENT_IDS = dict(zip(CONDITIONS, INDEXES))
EVENT_NAMES = dict(zip(INDEXES, CONDITIONS))

EVENTS = [] 

time = 0 #start

for i in range(0,NR_TRIALS):    
    EVENTS.append([time,0,1]) #baseline
    time = time + EVENT_DURATION
    EVENTS.append([time,0,2]) #vs_right
    time = time + EVENT_DURATION
    EVENTS.append([time,0,1]) #baseline
    time = time + EVENT_DURATION
    EVENTS.append([time,0,3]) #vs_left
    time = time + EVENT_DURATION

EVENTS.append([time,0,1]) #end with baseline

# location

ANNOTATION = 'aparc.a2009s'

BASE_REGION = 'occipital_sup'

BASE_LABEL = fm.do_label(ANNOTATION, BASE_REGION)

left_hemi = 'G_occipital_sup-lh'
right_hemi = 'G_occipital_sup-rh'

VISUAL_LABELS = {left_hemi : fm.do_label(ANNOTATION, left_hemi),
                 right_hemi : fm.do_label(ANNOTATION, right_hemi)} 

# WAVEFORM

F_BAND = 10 #alpha rythm

BASE_LATENCY = 0
BASE_DURATION = 1
BASE_AMPLITUDE = 0

LATENCY = 0.175 #175ms +/- 50*ms, main peak N1 (slightly shifted towards P2)
IPSILATERAL_DELAY = 0.015 #contralateral latency + 15ms
DURATION = 0.2 #200ms +/- 50ms

# participant & trial variables, normally distributed:

LATENCY_VAR_PART_DIST = (0, 0.025) 
LATENCY_VAR_DIST = (0,0.025) 
#latency +/- 50 ms(2*SD)

AMPLITUDE_VAR_PART_DIST = (0,2.5)
AMPLITUDE_VAR_DIST = (0,2.5) 
#amplitude +/- 5mV (2*SD)

#latency variables
LAT_VARS_FILE = 'vars_latency.csv'
NEW_VARS = False #should be created only once (x2 test-retest)
LAT_VARS = fm.do_vars(LAT_VARS_FILE, NEW_VARS, 
                        NR_PARTICIPANTS, EVENTS, EVENT_NAMES, 
                        LATENCY_VAR_PART_DIST, LATENCY_VAR_DIST)

#amplitude variables
AMP_VARS_FILE = 'vars_amplitude.csv'
NEW_VARS = False #should be created only once 
AMP_VARS = fm.do_vars(AMP_VARS_FILE, NEW_VARS, 
                        NR_PARTICIPANTS, EVENTS, EVENT_NAMES, 
                        AMPLITUDE_VAR_PART_DIST, AMPLITUDE_VAR_DIST)

# PROPAGATION

#source space
SS_SRC_FILE = 'ss-src.fif'
NEW_SRC = False #takes some time to generate, should be created only once
SRC = fm.do_src(SS_SRC_FILE, NEW_SRC)
    
#forward model
FS_FWD_FILE = 'fs-avg-fwd.fif'
NEW_FWD = False #takes some time to generate, should be created only once
TRANS = 'fsaverage' 
# 'fsaverage' = built-in free surfer transformation/ None = identity matrix

FWD = fm.do_fwd(FS_FWD_FILE, NEW_FWD, TRANS, SRC, INFO)

# NOISE

#noise covariance matrix
NOISE_COV = mne.make_ad_hoc_cov(info = INFO)

# PROCESSING
# band pass
FILTER = (0.1, 30)

# time
T_MIN = -0.5
T_MAX = 0.5

BASELINE = (T_MIN, 0) #or None (for baseline correction)

# PREPARATION
DIFFERENCE = 'difference'
TEST_CONDITIONS = CONDITIONS + [DIFFERENCE] #4 total

#electrode density
DENSITY = {86: CHANNELS_86,
           64: CHANNELS_64,
           31: CHANNELS_31}

#a priori electrode location
LOCAL = [True, False] #only visual, or all

# window size (multiples of 4)
WINDOW_SIZE = [0.004, 0.012, 0.02] # 4 ms (original), 12 ms, or 20 ms

#tested inerval
TEST_INTERVAL_MIN = 50
TEST_INTERVAL_MAX = 300 

#a priori time interval
TIME_INTERVAL = [True, False] #only aroudn expected ERP, or all psot sitmulus

# ANALYSIS
SIGNIFICANCE = 0.05

#true signal interval
SIG_INTERVAL_MIN = 100
SIG_INTERVAL_MAX = 250

# SIMULATION VARIABLES
# Change these variables to generate data with different amplitude values

AMPLITUDE = None
NOISE_FILTER = None
BAND_PASS_FILTERING = None

ACTIVATIONS = None

def set_up(amplitude, noise_filter, band_pass_filtering):
    
    consts = globals()
    
    consts["AMPLITUDE"] = amplitude
    
    consts["ACTIVATIONS"] = {
        'vs_right':
            [(left_hemi, AMPLITUDE[0]), #contra
             (right_hemi, AMPLITUDE[1]) #ipsi
             ],
        'vs_left':
            [(left_hemi, AMPLITUDE[1]), #ipsi
             (right_hemi, AMPLITUDE[0]) #contra
             ]
    }

    consts["NOISE_FILTER"] = noise_filter
    consts["BAND_PASS_FILTERING"] = band_pass_filtering



