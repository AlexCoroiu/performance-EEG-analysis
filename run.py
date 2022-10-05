# -*- coding: utf-8 -*-
"""

@author: User
"""
import file_manager as fm
import constants as c

import simulation
import processing

import preparation
import multiple_comparisons
import cluster_permutations

import exploration
import results

# SIMULATE-ANALYSE DATA
def run_data():
    simulation.simulate()
    processing.process()
    preparation.prepare()
     
def run_methods():
    multiple_comparisons.test_window()
    #multiple_comparisons.test_bonferroni()
    #cluster_permutations.test()
    
def run_dataset(amplitude, noise_filter, band_pass_filtering):
    
    #SETUP
    #file structure
    fm.set_up('data_amp' + str(amplitude[0]) + str(amplitude[1])
               + '_noise' + str(noise_filter[0])
               + '_filter' + str(band_pass_filtering))
    
    #constants  
    c.set_up(amplitude, noise_filter, band_pass_filtering)

    #RUN 
    run_data()
    run_methods()
    
amplitudes = [(40,20), (60,30), (60, 20), (80,40), (80,30), (80,20)] #mV (contra, ipsi)
noise_filters = [(0.1,-0.1,0.02),(0.2,-0.2,0.04)] #infinite impulse response filter
band_pass_filtering = [True,False]
    
def run():
    for amp in amplitudes:
        for nf in noise_filters:
            for bpf in band_pass_filtering:
                run_dataset(amp, nf, bpf)

#run_dataset((60,30), (0.1,-0.1,0.02), True)

#run()
#exploration.explore() #needs setup beforehand