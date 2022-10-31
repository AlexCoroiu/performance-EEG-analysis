# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:05:18 2022

@author: User
"""

import pandas as pd
import os
import sklearn.metrics
import seaborn as sb
import numpy as np
from results import get_metrics
from file_manager import do_dir
import matplotlib.pyplot as plt
from itertools import repeat
import scipy

#variables
simulation_vars = ['amplitude', 'noise', 'band_pass']
measurement_vars = ['window_size', 'density', 'location']
independent_vars = simulation_vars + measurement_vars
dependent_vars = ['F1','type_I_ER','type_II_ER'] 
stats_vars = ['M', 'SD']


#HELPING FUNCTIONS
def load_final_results():
    dataframe_file = 'final_results.csv'
    data = pd.read_csv(dataframe_file)

    return data

def local_stats(data, var):
    #(mean, sd)
    return [data[var].mean(), data[var].std()]

def global_metrics(data):
    #(TN, FP, FN, TP, precision, recall, F1, type_I_ER, type_II_ER)
    (TN, FP, FN, TP, precision, recall, 
     F1, type_I_ER, type_II_ER) = get_metrics(data['expected'],
                                              data['global_significant'])
    return (F1, type_I_ER, type_II_ER)

def split_data(data, var):
    vars_data = {}
    vals = data[var].unique()

    for val in vals:
        val_data = data[data[var] == val]
        vars_data[val] = val_data

    return vars_data

# SUMAMRY STATISTICS

# I. Between Method

#global methods
def compare_methods_global(stats_dir, methods):
    methods_metrics = []
    
    for m_name, m_data in methods.items():
        metrics = global_metrics(m_data)
        m_metrics = zip(repeat(m_name), dependent_vars, metrics)
        
        methods_metrics.extend(m_metrics)
        
    methods_metrics_df = pd.DataFrame(methods_metrics, 
                                      columns = ['method', 'metric', 'value'])
    
    methods_metrics_df = methods_metrics_df.pivot(index = 'metric',
                                                  columns = 'method',
                                                  values = 'value')
    
    methods_metrics_df = methods_metrics_df.round(decimals = 4)
    
    dataframe_file = stats_dir + '\\global_comparison_methods.csv'
    methods_metrics_df.to_csv(dataframe_file)
    
#global methods per condition
def compare_methods_conds_global(stats_dir, methods):
    methods_metrics = []
    
    for m_name, m_data in methods.items():
        
        m_conds = split_data(m_data, 'condition')

        for c_name, mc_data in m_conds.items():
            metrics = global_metrics(mc_data)
            mc_metrics = zip(repeat(m_name), repeat(c_name), 
                            dependent_vars, metrics)
            
            methods_metrics.extend(mc_metrics)
    
    methods_metrics_df = pd.DataFrame(methods_metrics, 
                                      columns =['method', 'condition', 'metric', 'value'])
    
    methods_metrics_df = methods_metrics_df.pivot(index = ['condition', 'metric'],
                                                  columns = 'method',
                                                  values = 'value')
    
    methods_metrics_df = methods_metrics_df.round(decimals = 4)

    dataframe_file = stats_dir + '\\global_comparison_methods_conds.csv'
    methods_metrics_df.to_csv(dataframe_file)

#local methods
def compare_methods_local(stats_dir, methods):
    d_stats = []
    
    for m_name, m_data in methods.items():
        for d in dependent_vars:
            stats = local_stats(m_data, d)
            m_stats = zip(repeat(m_name), repeat(d), stats_vars, stats)

            d_stats.extend(m_stats)
        
    d_stats_df = pd.DataFrame(d_stats,
                              columns = ['method', 'metric',  'stats', 'value'])
    
    d_stats_df = d_stats_df.pivot(index = ['metric', 'stats'],
                                  columns = 'method',
                                  values = 'value')
    
    d_stats_df = d_stats_df.round(decimals = 4)
    
    dataframe_file = stats_dir + '\\local_comaprison_methods.csv'
    d_stats_df.to_csv(dataframe_file)


#local per condition
def compare_methods_conds_local(stats_dir, methods):
    d_stats = []
    
    for m_name, m_data in methods.items():
        
        m_conds = split_data(m_data, 'condition')
        
        for c_name, mc_data in m_conds.items():
            
            for d in dependent_vars:
                
                stats = local_stats(mc_data, d)
                
                mc_stats = zip(repeat(m_name), repeat(c_name), repeat(d),
                                stats_vars, stats)
                d_stats.extend(mc_stats)
            
            
    d_stats_df = pd.DataFrame(d_stats, 
                              columns =['method', 'condition', 'metric',
                                         'stats', 'value'])
    
    d_stats_df = d_stats_df.pivot(index = ['condition', 'metric', 'stats'],
                                  columns = 'method',
                                  values = 'value')
    
    d_stats_df = d_stats_df.round(decimals = 4)
    
    dataframe_file = stats_dir + '\\local_comaprison_methods_conds.csv'
    d_stats_df.to_csv(dataframe_file)


# II. Within Methods

#global
def compare_vars_global(stats_i_dir, mi_split, m_name, i):
    i_stats = []
    
    for i_name, mi_data in mi_split.items():
        metrics = global_metrics(mi_data)
        mc_metrics = zip(repeat(m_name), repeat(i_name), 
                        dependent_vars, metrics)
        
        i_stats.extend(mc_metrics)

    i_stats_df = pd.DataFrame(i_stats, 
                              columns =['method', i, 'metric', 'value'])
    
    i_stats_df = i_stats_df.pivot(index = ['method', 'metric'],
                                  columns = i,
                                  values = 'value')
    
    i_stats_df = i_stats_df.round(decimals = 4)

    dataframe_file = stats_i_dir + '\\global_comparison_' + i + '.csv'
    i_stats_df.to_csv(dataframe_file)
            

def compare_vars_conds_global(stats_i_dir, mi_split, m_name, i):
     i_metrics = []
     
     for i_name, mi_data in mi_split.items():
         
         mi_conds = split_data(mi_data, 'condition')

         for c_name, mic_data in mi_conds.items():
         
             metrics = global_metrics(mi_data)
             mic_metrics = zip(repeat(m_name), repeat(i_name), repeat(c_name),
                             dependent_vars, metrics)
             
             i_metrics.extend(mic_metrics)

     i_metrics_df = pd.DataFrame(i_metrics, 
                               columns =['method', i, 'condition', 'metric', 'value'])
     
     i_metrics_df = i_metrics_df.pivot(index = ['method', 'condition', 'metric'],
                                   columns = i,
                                   values = 'value')
     
     i_metrics_df = i_metrics_df.round(decimals = 4)

     dataframe_file = stats_i_dir + '\\global_comparison_' + i + '_conds.csv'
     i_metrics_df.to_csv(dataframe_file)


def compare_vars_local(stats_i_dir, mi_split, m_name, i):
    d_stats = []
    
    for i_name, mi_data in mi_split.items():
        for d in dependent_vars:
            
            stats = local_stats(mi_data, d)
            m_stats = zip(repeat(m_name), repeat (i_name), repeat(d), 
                          stats_vars, stats)

            d_stats.extend(m_stats)
            
            d_stats_df = pd.DataFrame(d_stats,
                                      columns = ['method', i, 'metric', 'stats', 'value'])
            
            d_stats_df = d_stats_df.pivot(index = ['method', 'metric', 'stats'],
                                          columns = i,
                                          values = 'value')
            
            d_stats_df = d_stats_df.round(decimals = 4)
            
            dataframe_file = stats_i_dir + '\\local_comparison_' + i + '.csv'
            d_stats_df.to_csv(dataframe_file)
            
              
def compare_vars_conds_local(stats_i_dir, mi_split, m_name, i):
    d_stats = []
    
    for i_name, mi_data in mi_split.items():
        
        mi_conds = split_data(mi_data, 'condition')
        
        for c_name, mic_data in mi_conds.items():
            
            for d in dependent_vars:
                
                stats = local_stats(mic_data, d)
                m_stats = zip(repeat(m_name), repeat (i_name), repeat(c_name),
                              repeat(d), stats_vars, stats)
    
                d_stats.extend(m_stats)
                
                d_stats_df = pd.DataFrame(d_stats,
                                          columns = ['method', i, 'condition', 
                                                     'metric', 'stats', 'value'])
                
                d_stats_df = d_stats_df.pivot(index = ['method', 'condition', 'metric', 'stats'],
                                              columns = i,
                                              values = 'value')
                
                d_stats_df = d_stats_df.round(decimals = 4)
                
                dataframe_file = stats_i_dir + '\\local_comparison_' + i + '_conds.csv'
                d_stats_df.to_csv(dataframe_file)
 

#plots for local tests: box plots, violin plots?
def plots_vars_local(stats_i_dir, m_split, m_name, i):
    
    stats_plots_dir = stats_i_dir + '\\plots'
    do_dir(stats_plots_dir)
  
    m_conds = split_data(m_split, 'condition')

    for c_name, mc_data in m_conds.items(): #for each cond
        
    #split per d
        for d in dependent_vars: #for each metric
            
            plot = sb.violinplot(data=mc_data, 
                                 x=i, y=d)
            file = stats_plots_dir + '\\' + d + '_' + c_name + '_violin.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
            

def test_diff_local(stats_i_dir, m_split, m_name, i):
    
    stats_tests_dir = stats_i_dir + '\\tests'
    do_dir(stats_tests_dir)
  
    m_conds = split_data(m_split, 'condition')

    for c_name, mc_data in m_conds.items(): #for each cond
        
    #split per d
        for d in dependent_vars: #for each metric
            
            ids = list(set(['method', 'condition'] + independent_vars) - set([i]))    
            d_data = mc_data.pivot(index = ids,
                                   columns = i,
                                   values = d)
            
            #matrix
            d_matrix = []
            
            
            #calcualte differences
            vals = mc_data[i].unique()
            for v1 in vals:
                for v2 in vals:
                    v_diff = d_data[v1] - d_data[v2]
                    
                    #rint(v_diff)
                    
                    #TODO test normality beforehand
                    t_stat, p_val = scipy.stats.ttest_1samp(v_diff, 
                                                            popmean = 0,
                                                            alternative = 'two-sided')
                
                    
                    reject = p_val < 0.05
                    
                    d_matrix.append([v1,v2,reject])
                    
            #save matrix
            d_matrix_df = pd.DataFrame(data = d_matrix,
                                        columns = ['v1', 'v2', 'reject'])
            
            d_matrix_df = d_matrix_df.pivot(index = 'v1',
                                            columns = 'v2',
                                            values = 'reject')
            
            
            dataframe_file = stats_tests_dir + '\\' + d + '_' + c_name + '.csv'
            d_matrix_df.to_csv(dataframe_file)
                    
                                    

#get statistics
def get_stats(): 
    
    # SETUP
    #load final results
    data = load_final_results()

    # expected global results
    data['expected'] = np.where(data['condition'] == 'baseline', False, True) 
    
    methods = data['method'].unique()

    #splitting data
    methods = split_data(data, 'method')

    #directories
    stats_dir = "statistics"
    do_dir(stats_dir)
    
    # STATS 
    
    #between methods
    
    #global metrics
    compare_methods_global(stats_dir, methods)
    compare_methods_conds_global(stats_dir, methods)
    
    #local stats
    #TODO probably doesnt make sense since they function differently
    # compare_methods_local(stats_dir, methods)
    # compare_methods_conds_local(stats_dir, methods)

    #within methods & conditions (vars)
    
    #global

    #local
    
    for m_name, m_data in methods.items():
        
        #create directory
        stats_m_dir = stats_dir + '\\' + m_name
        do_dir(stats_m_dir)
        
        for i in independent_vars:

            #create directory
            stats_i_dir = stats_m_dir + '\\' + i
            do_dir(stats_i_dir)
        
            mi_data = split_data(m_data, i)
            #global metrics
            compare_vars_global(stats_i_dir, mi_data, m_name, i)
            compare_vars_conds_global(stats_i_dir, mi_data, m_name, i)
            #local stats
            compare_vars_local(stats_i_dir, mi_data, m_name, i)
            compare_vars_conds_local(stats_i_dir, mi_data, m_name, i)
            
            #plots
            plots_vars_local(stats_i_dir, m_data, m_name, i)
            
            #tests
            test_diff_local(stats_i_dir, m_data, m_name, i)
            

    # p_val_local('mc_w')
    # p_val_conds_local('mc_w')
    # p_val_conds_vars_local('mc_w')  

get_stats()



    
#%%
#TODO P_VAL

def p_val_conds_local(method):
    data_m = data[data['method'] == method]
    stats_plots_dir = stats_dir + '\\' + method + '\\plots'
    do_dir(stats_plots_dir)
    
    #plot scatter
    for d in d_vars:
        plot = sb.lmplot(data=data_m, 
                    x='crit_p_val', y=d, 
                    col = 'condition',
                    scatter = True,
                    fit_reg=True,
                    facet_kws=dict(sharex=False, sharey=False))
        file = stats_plots_dir + '\\cond_' + d + '_scatter.png'
        plot.savefig(file)
        plot.fig.clf()
        
    #plot violin
    for d in d_vars:
        for cond in conditions:
            data_c = data_m[data_m['condition'] == cond]
            plot = sb.violinplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = stats_plots_dir + '\\' + d + '_' + cond + '_violin.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
            
    #plot histogram
    for d in d_vars:
        for cond in conditions:
            data_c = data_m[data_m['condition'] == cond]
            plot = sb.histplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = stats_plots_dir + '\\' + d + '_' + cond + '_hist.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
            
    #plot boxplot
    for d in d_vars:
        for cond in conditions:
            data_c = data_m[data_m['condition'] == cond]
            plot = sb.boxplot(data=data_c, 
                        x='crit_p_val', y=d)
            file = stats_plots_dir + '\\' + d + '_' + cond + '_box.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clf()
    

    
def p_val_conds_vars_local(method, independent_vars):
    data_m = data[data['method'] == method]
    stats_plots_dir = stats_dir + '\\' + method + '\\plots'
    do_dir(stats_plots_dir)
    
    #plot
    for v in i_vars:
        for d in d_vars:
            plot = sb.lmplot(data=data_m, 
                        x='crit_p_val', y=d, 
                        col = 'condition',
                        scatter = True,
                        fit_reg=True,
                        facet_kws=dict(sharex=False, sharey=False))
            file = stats_plots_dir + '\\cond_' + v + '_' + d + '.png'
            plot.savefig(file)
            

    
#hue for highlighting other aspects    
#row like col for matrix

    



