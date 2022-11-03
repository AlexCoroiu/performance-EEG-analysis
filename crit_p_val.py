# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:42:00 2022

@author: Alexandra
"""
import statsitics as stats
import lateralization as lat
import padnas as pd
import numpy as np
from file_manager import do_dir
import seaborn as sb

#variables
simulation_vars = ['amplitude', 'noise', 'band_pass']
measurement_vars = ['window_size', 'density', 'location']
independent_vars = simulation_vars + measurement_vars
dependent_vars = ['F1','type_I_ER','type_II_ER'] 
stats_vars = ['M', 'SD']

# SETUP
#load final results
data_ERP = stats.load_final_results()
data_lat = lat.load_final_results()

data = pd.concat([data_ERP, data_lat])

# expected global results
data['expected'] = np.where(data['condition'] == 'baseline', False, True) 

methods = data['method'].unique()
conditions = data['conditions'].unique()

data = data[data['method'] == 'mc_w']

p_dir = 'p_val' 
do_dir(p_dir)

def p_val_conds_local():
    do_dir(p_dir)    
    #plot scatter
    for d in dependent_vars:
        plot = sb.lmplot(data=data, 
                    x='crit_p_val', y=d, 
                    col = 'condition',
                    scatter = True,
                    fit_reg=True,
                    facet_kws=dict(sharex=False, sharey=False))
        file = p_dir + '\\conds_' + d + '_scatter.png'
        plot.savefig(file)
        plot.fig.clf()
        
    #plot violin
    for d in dependent_vars:
        for cond in conditions:
            data_c = data[data['condition'] == cond]
            plot = sb.violinplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = p_dir + '\\' + d + '_' + cond + '_violin.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
            
    #plot histogram
    for d in dependent_vars:
        for cond in conditions:
            data_c = data[data['condition'] == cond]
            plot = sb.histplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = p_dir + '\\' + d + '_' + cond + '_hist.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
            
    #plot boxplot
    for d in dependent_vars:
        for cond in conditions:
            data_c = data[data['condition'] == cond]
            plot = sb.boxplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = p_dir + '\\' + d + '_' + cond + '_box.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
        
def p_val_conds_vars_local():
    #plot
    for v in independent_vars:
        for d in dependent_vars:
            plot = sb.lmplot(data=data, 
                        x='crit_p_val', y=d, 
                        col = 'condition',
                        scatter = True,
                        fit_reg=True,
                        facet_kws=dict(sharex=False, sharey=False))
            file = p_dir + '\\conds_' + v + '_' + d + '.png'
            plot.savefig(file)
            

    
#hue for highlighting other aspects    
#row like col for matrix

#TODO global
