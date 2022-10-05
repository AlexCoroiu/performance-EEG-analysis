# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:36:00 2022

@author: User
"""

import simulation
import processing
import exploration

import preparation
import multiple_comparisons
import cluster_permutations
import results

# SIMULATE-ANALYSE DATA
def run_data():
    #simulation.simulate()
    processing.process()
    preparation.prepare()
     
def run_methods():
    multiple_comparisons.test_window()
    #multiple_comparisons.test_bonferroni()
    #cluster_permutations.test()
    
def run_results():
    results.results()

#RUN 
#run_data()
run_methods()
