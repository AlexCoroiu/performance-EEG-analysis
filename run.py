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
import results

# SIMULATE-ANALYSE DATA
def run_dataset():
    simulation.simulate()
    # processing.process()
    # preparation.prepare()
    # multiple_comparisons.test()
    # results.results()

run_dataset()
