# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 15:42:00 2022

@author: Alexandra
"""
import pandas as pd
from file_manager import do_dir
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
#variables
processing_vars = ['window_size', 'time_interval', 'density', 'location']
dependent_vars = ['type_I_ER','type_II_ER'] 
stats_vars = ['M', 'SD']

def p_val_conds_local(data, p_dir):
    do_dir(p_dir)    
    #plot scatter
    for d in dependent_vars:
        plot = sb.lmplot(data=data, 
                    x='crit_p_val', y=d, 
                    col = 'condition', #col, hue or row
                    col_wrap = 2,
                    scatter = True,
                    fit_reg=True,
                    facet_kws=dict(sharex=True, sharey=True))
        file = p_dir + '\\local_scatter_' + d + '_conds.png'
        plot.savefig(file)
        plot.fig.clf()
        
    # #plot violin
    # for d in dependent_vars:
    #     for cond in conditions:
    #         data_c = data[data['condition'] == cond]
    #         plot = sb.violinplot(data=data_c, 
    #                     x='crit_p_val', y=d)
    #         file = p_dir + '\\violin_' + d + '_' + cond + '.png'
    #         plot.get_figure().savefig(file)
    #         plot.get_figure().clf()
            
    # #plot histogram
    # for d in dependent_vars:
    #     for cond in conditions:
    #         data_c = data[data['condition'] == cond]
    #         plot = sb.histplot(data=data_c, 
    #                     x='crit_p_val', y=d)
    #         file = p_dir + '\\hist_' + d + '_' + cond + '.png'
    #         plot.get_figure().savefig(file)
    #         plot.get_figure().clf()
            
    # #plot boxplot
    # for d in dependent_vars:
    #     for cond in conditions:
    #         data_c = data[data['condition'] == cond]
    #         plot = sb.boxplot(data=data_c, 
    #                     x='crit_p_val', y=d)
    #         file = p_dir + '\\box_' + d + '_' + cond + '.png'
    #         plot.get_figure().savefig(file)
    #         plot.get_figure().clf()
        
def p_val_conds_vars_local(data, p_dir):
    #plot scatter
    for i in processing_vars:
        for d in dependent_vars:
            plot = sb.lmplot(data=data, 
                        x='crit_p_val', y=d, 
                        hue = i, #hue or row
                        col = 'condition',
                        col_wrap = 2,
                        scatter = True,
                        fit_reg=True,
                        facet_kws=dict(sharex=True, sharey=True))
            file = p_dir + '\\local_scatter_' + d + '_' + i + '_conds.png'
            plot.savefig(file)
            

def p_val_conds_global(data, p_dir):
    plot = sb.lmplot(data=data, 
                x='crit_p_val', y = 'positives_rate', 
                col = 'condition', #col, hue or row
                col_wrap = 2,
                scatter = True,
                fit_reg=True,
                facet_kws=dict(sharex=True, sharey=True))
    plot.refline(y = 0.05)
    file = p_dir + '\\global_scatter_positives_conds.png'
    plot.savefig(file)
    plot.fig.clf()
    
    
def p_val_conds_vars_global(data, p_dir):
    for i in processing_vars:
        plot = sb.lmplot(data=data, 
                    x='crit_p_val', y = 'positives_rate', 
                    hue = i, #hue or row
                    col = 'condition',
                    col_wrap = 2,
                    scatter = True,
                    fit_reg=True,
                    facet_kws=dict(sharex=True, sharey=True))
        plot.refline(y = 0.05)
        file = p_dir + '\\global_scatter_positives_' + i + '_conds.png'
        plot.savefig(file)


def p_val_tests(data, p_dir):
    plot = sb.relplot(data=data, 
                x='total', y = 'crit_p_val')
    file = p_dir + '\\p_val.png'
    
    min_tests = data['total'].min()
    max_tests = data['total'].max()
    
    #print(min_tests,max_tests)

    x = np.linspace(min_tests,max_tests,max_tests)
    y = 2*np.sqrt(0.05/x)
    plt.plot(x,y)
    
    
    plot.savefig(file)
    plot.fig.clf()
    
def total_tests(data,p_dir):
    plot = sb.lmplot(data=data, 
                x='total', y = 'positives_rate', 
                col = 'condition',
                col_wrap = 2,
                scatter = True,
                fit_reg=True,
                facet_kws=dict(sharex=True, sharey=True))
    plot.refline(y = 0.05)
    file = p_dir + '\\total_tests.png'
    plot.savefig(file)
    

def determine_p_val():
    # SETUP
    #load final results
    data_ERP = pd.read_csv('results.csv')
    data_lat = pd.read_csv('lat_results.csv')

    data_tests = {'diff': data_ERP, 'lat': data_lat}
    
    for d_name, data in data_tests.items():
        p_dir = 'p_val_' + d_name
        do_dir(p_dir)
        
        data = data[data['method'] == 'mc_w']
        
        #asses p val calcualtion
        p_val_tests(data,p_dir)
    
        # expected global results
        #data['expected'] = np.where(data['condition'] == 'baseline', False, True) 
        data['positives_rate'] = data['positives']/data['total']
    
        total_tests(data,p_dir)
    
        p_val_conds_global(data, p_dir)
        p_val_conds_vars_global(data, p_dir)
        
        p_val_conds_local(data, p_dir)
        p_val_conds_vars_local(data, p_dir)

    
determine_p_val()
#hue for highlighting other aspects    
#row like col for matrix
