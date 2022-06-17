# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:01:37 2022

@author: User
"""

#setup
import mne
import spicy.stats
import preparation as prep
#load prepped data

window = 4
density = 86
local = False
data = prep.load_test_dfs(window, density, local)

#test mean == 0, 2 sided
#for each time x electrode
t_test, p_val = stats.ttest_1samp(data)