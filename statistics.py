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

#HELPING FUNCTIONS
def load_final_results():
    dataframe_file = 'final_results.csv'
    data = pd.read_csv(dataframe_file)

    return data

def group_stats(data, i_var, d_var):
    grouped = data.groupby(i_var)
    return [grouped[d_var].mean(), grouped[d_var].std()]

def group_metrics(data):
    #(TN, FP, FN, TP, precision, recall, F1) 
    global_results = get_metrics(data['expected'],
                                 data['global_significant'])
    return global_results

def split_data(data, var):
    vars_data = []
    vals = data[var].unique()

    for val in vals:
        val_data = data[data[var] == val]
        vars_data.append(val_data)

    return vars_data

# SETUP
#load final results
data = load_final_results()

#variables
sim_vars = ['amplitude', 'noise', 'band_pass']

meas_vars = ['window_size', 'density', 'location']

i_vars = sim_vars + meas_vars

methods = ['mc_w', 'mc_b', 'cp'] #or get from unique
conditions = ['baseline', 'vs_right', 'vs_left', 'difference']

d_vars = ['F1','type_I_ER','type_II_ER'] #TODO ad expected at local level

# expected global results
data['expected'] = np.where(data['condition'] == 'baseline', False, True) #TODO addd expected at global level

#splitting data
methods_data = split_data(data, 'method')
m_names = data['method'].unique()

#directories
stats_dir = "statistics"
do_dir(stats_dir)

# SUMAMRY STATISTICS

# I. Between Method

# global
def compare_methods():
    methods_metrics = []
    
    for m in methods_data:
        m_name = m['method'].iloc[0]
        m_metrics = [m_name]

        metrics = group_metrics(m)
        m_metrics.extend(metrics)
        
        methods_metrics.append(m_metrics)
        
    methods_metrics_df = pd.DataFrame(methods_metrics, 
                              columns =['method'] + d_vars)

    dataframe_file = stats_dir + '\\compare_methods.csv'
    methods_metrics_df.to_csv(dataframe_file, index = False)
    
#global per condition
def compare_methods_conds():
    methods_metrics = []
    
    for m in methods_data:
        m_name = m['method'].iloc[0]
        m_cond_data = split_data(m, 'condition')

        for mc in m_cond_data:
            c_name = mc['condition'].iloc[0]
            mc_metrics = [m_name,c_name]
            
            metrics = group_metrics(mc)
            mc_metrics.extend(metrics)
            
            methods_metrics.append(mc_metrics)
    
    methods_metrics_df = pd.DataFrame(methods_metrics, 
                                      columns =['method', 'condition'] + d_vars)

    dataframe_file = stats_dir + '\\compare_methods_conds.csv'
    methods_metrics_df.to_csv(dataframe_file, index = False)


def compare_method_vars(m, var, stats_dir):
    m_name = m['method'].iloc[0]
    m_var_data = split_data(m, var)
    
    method_vars_metrics = []
    
    for mv in m_var_data:
        v_name = mv[var].iloc[0]
        mv_metrics = [m_name,v_name]
        
        metrics = group_metrics(mv)
        mv_metrics.extend(metrics)
        
        method_vars_metrics.append(mv_metrics)

    method_metrics_df = pd.DataFrame(method_vars_metrics, 
                                     columns =['method', var] + d_vars)

    dataframe_file = stats_dir + '\\' + var + '.csv'
    method_metrics_df.to_csv(dataframe_file, index = False)
    
def compare_vars():
    for m in methods_data:
        m_name = m['method'].iloc[0]
        stats_m_dir = stats_dir + '\\' + m_name
        do_dir(stats_m_dir)
        
        for v in i_vars:
            compare_method_vars(m, v, stats_m_dir)
            
def compare_method_vars_cond(m, var, stats_dir):
    m_name = m['method'].iloc[0]
    m_var_data = split_data(m, var)
    
    method_vars_metrics = []
    
    for mv in m_var_data:
        v_name = mv[var].iloc[0]
        m_cond_data = split_data(mv, 'condition')
        
        for mc in m_cond_data:
            c_name = mc['condition'].iloc[0]
            mc_metrics = [m_name,v_name,c_name]
            
            metrics = group_metrics(mc)
            mc_metrics.extend(metrics)
            
            method_vars_metrics.append(mc_metrics)

    method_metrics_df = pd.DataFrame(method_vars_metrics, 
                                     columns = ['method', var, 'condition'] + d_vars)

    dataframe_file = stats_dir + '\\' + var +'_conds.csv'
    method_metrics_df.to_csv(dataframe_file, index = False)
            
def compare_vars_cond():
    for m in methods_data:
        m_name = m['method'].iloc[0]
        stats_m_dir = stats_dir + '\\' + m_name
        do_dir(stats_m_dir)
        
        for v in i_vars:
            compare_method_vars_cond(m, v, stats_m_dir)

#local level
def compare_methods_local():
    stats = {}
    for d in d_vars:
        d_stats = []
        for m in methods_data:
            m_name = m['method'].iloc[0]
            
            m_stats = [m_name]
            m_stats.extend([m[d].mean(),m[d].std()])
            
            d_stats.append(m_stats)
        
        d_stats_df = pd.DataFrame(d_stats,
                                  columns = ['method', 
                                             'M', 'SD'])
        d_stats_df = d_stats_df.set_index('method')
        stats[d] = d_stats_df
        
    stats_df = pd.concat(stats, axis = 1,
                         names = ['metric'] )
    
    dataframe_file = stats_dir + '\\local_comaprison_methods.csv'
    stats_df.to_csv(dataframe_file)

def compare_methods_conds_local():
    stats = {}
    for d in d_vars:
        d_stats = []
        for m in methods_data:
            m_name = m['method'].iloc[0]
            m_cond_data = split_data(m, 'condition')
            for mc in m_cond_data:
                c_name = mc['condition'].iloc[0]
                m_stats = [m_name, c_name]
                m_stats.extend([mc[d].mean(),mc[d].std()])
                
                d_stats.append(m_stats)
            
            d_stats_df = pd.DataFrame(d_stats,
                                      columns = ['method', 'condition',
                                                  'M', 'SD'])
            d_stats_df = d_stats_df.set_index(['method', 'condition'])
            stats[d] = d_stats_df
            
        stats_df = pd.concat(stats, axis = 1,
                              names = ['metric'] )
    
    dataframe_file = stats_dir + '\\local_comaprison_methods_conds.csv'
    stats_df.to_csv(dataframe_file)
    
def compare_vars_local():
    for m in methods_data:
        m_name = m['method'].iloc[0]
        stats_m_dir = stats_dir + '\\' + m_name
        for var in i_vars:
            mv_data = split_data(m, var)
            mv_stats = {}
            for d in d_vars:
                d_stats = []
                for mv in mv_data:
                    v_name = mv[var].iloc[0]
                    v_stats = [m_name, v_name]
                    v_stats.extend([mv[d].mean(),mv[d].std()])
                    
                    d_stats.append(v_stats)
                
                d_stats_df = pd.DataFrame(d_stats,
                                          columns = ['method', var,
                                                      'M', 'SD'])
                d_stats_df = d_stats_df.set_index(['method', var])
                mv_stats[d] = d_stats_df
             
            stats_df = pd.concat(mv_stats, axis = 1,
                                 names = ['metric'])
            
            dataframe_file = stats_m_dir + '\\' + var + '_local.csv'
            stats_df.to_csv(dataframe_file)

                
def compare_vars_conds_local():
    for m in methods_data:
        m_name = m['method'].iloc[0]
        stats_m_dir = stats_dir + '\\' + m_name
        for var in i_vars:
            mv_data = split_data(m, var)
            mv_stats = {}
            for d in d_vars:
                d_stats = []
                for mv in mv_data:
                    v_name = mv[var].iloc[0]
                    mv_cond_data = split_data(mv, 'condition')
                    for mvc in mv_cond_data:
                        c_name = mvc['condition'].iloc[0]
                        v_stats = [m_name, v_name, c_name]
                        v_stats.extend([mvc[d].mean(),mvc[d].std()])
                        
                        d_stats.append(v_stats)
                
                d_stats_df = pd.DataFrame(d_stats,
                                          columns = ['method', var, 'condition',
                                                      'M', 'SD'])
                d_stats_df = d_stats_df.set_index(['method', var])
                mv_stats[d] = d_stats_df
             
            stats_df = pd.concat(mv_stats, axis = 1,
                                 names = ['metric'])
            
            dataframe_file = stats_m_dir + '\\' + var + '_conds_local.csv'
            stats_df.to_csv(dataframe_file)
        
#p_val

# def p_val_local(method):
#     data_m = data[data['method'] == method]
#     stats_plots_dir = stats_dir + '\\' + method + '\\plots'
#     do_dir(stats_plots_dir)
    
#     #plot scatter
#     for d in d_vars:
#         s_plot = sb.lmplot(data=data_m, 
#                     x='crit_p_val', y=d, 
#                     scatter = True,
#                     fit_reg=True,
#                     facet_kws=dict(sharex=False, sharey=False))
#         file = stats_plots_dir + '\\' + d + '_scatter.png'
#         s_plot.savefig(file)
    
#     #plot violin
#     for d in d_vars:
#         v_plot = sb.violinplot(data=data_m, 
#                     x='crit_p_val', y=d, 
#                     facet_kws=dict(sharex=False, sharey=False))
#         file = stats_plots_dir + '\\' + d + '_violin.png'
#         v_plot.get_figure().savefig(file)
    
def p_val_conds_local(method):
    data_m = data[data['method'] == method]
    stats_plots_dir = stats_dir + '\\' + method + '\\plots'
    do_dir(stats_plots_dir)
    
    #plot scatter #TODO is it  really linear, can we talk about lienarity?
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

def get_stats(): 
    #global
    compare_methods()
    compare_methods_conds()
    compare_vars()
    compare_vars_cond()
    
    #local
    compare_methods_local()
    compare_methods_conds_local()
    compare_vars_local()
    compare_vars_conds_local()
    
    # p_val_local('mc_w')
    # p_val_conds_local('mc_w')
    # p_val_conds_vars_local('mc_w')  
    
get_stats()

#TODO fix abomination code above (simplify /reuse method code)

#%% EXPLORATION VARIABLES

data_w = data[data['method'] == 'w']

#data_w.plot.scatter(x='crit_p_val', y = 'F1')

sb.lmplot(x='crit_p_val', y='F1', data=data_w, fit_reg=True)
sb.lmplot(x='total', y='F1', data=data_w, fit_reg=True)
sb.lmplot(x='total', y='crit_p_val', data=data_w, fit_reg=True)

sb.lmplot(data=data_w, 
        x='type_I_ER', y='type_II_ER', 
        scatter = True,
        fit_reg=True)

# as the number of tests increases the crit_p_value decreases
# lower crit p val => lower F1

sb.lmplot(x='crit_p_val', y='FP', data=data_w, fit_reg=True)
sb.lmplot(x='crit_p_val', y='FN', data=data_w, fit_reg=True)

# higher crit_p_val => lower FP (type I) and especially lower FN (type II)

sb.lmplot(data=data_w, 
        x='type_I_ER', y='type_II_ER', 
        col = 'condition',
        hue = 'band_pass',
        scatter = True,
        fit_reg=True,
        facet_kws=dict(sharex=False, sharey=False))

# STATISTICAL TESTS
sb.lmplot(x='crit_p_val', y='FN', data=data_w, fit_reg=True)

# higher crit_p_val => lower FP (type I) and especially lower FN (type II)

# STATISTICAL TESTS
