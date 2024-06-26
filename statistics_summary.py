# -*- coding: utf-8 -*-
"""
@author: Alexandra Coroiu
"""

import pandas as pd
import seaborn as sb
import numpy as np
from results import get_metrics
from file_manager import do_dir
from itertools import repeat
import scipy

#variables
simulation_vars = ['amplitude', 'noise', 'band_pass']
measurement_vars = ['window_size', 'time_interval', 'density', 'location']
independent_vars = simulation_vars + measurement_vars
dependent_vars = ['type_I_ER','type_II_ER'] 
stats_vars = ['M', 'SD']


#HELPING FUNCTIONS

#load results dataframe
def load_final_results():
    dataframe_file = 'results.csv'
    data = pd.read_csv(dataframe_file)

    return data

#mean metrics type I,II ER
def local_stats(data, var):
    #(mean, sd)
    return [data[var].mean(), data[var].std()]

#mean FDRs
def FDR_stats(data):
    data_positives = data[data['global_significant'] == True]
    data_positives['FDR'] = data_positives['FP']/data_positives['positives']
    return [data_positives['FDR'].mean(), data_positives['FDR'].std()]

#calculate global type I,II ER
def global_metrics(data):
    #(TN, FP, FN, TP, type_I_ER, type_II_ER)
    
    (TN, FP, FN, TP,
     type_I_ER, type_II_ER) = get_metrics(data['expected'],
                                          data['global_significant'])
    return (type_I_ER, type_II_ER)

#split by data parameter value
def split_data(data, var):
    vars_data = {}
    vals = data[var].unique()

    for val in vals:
        val_data = data[data[var] == val]
        vars_data[val] = val_data

    return vars_data

# SUMAMRY STATISTICS

# I. Between Method

#global methods per condition
def compare_methods_conds_global(stats_dir, methods):
        
    methods_metrics = []
    
    for m_name, m_data in methods.items():
        
        m_conds = split_data(m_data, 'condition')

        for c_name, mt_data in m_conds.items():
            
            metrics = global_metrics(mt_data)
            mt_metrics = zip(repeat(m_name), repeat(c_name), 
                            dependent_vars, metrics)
            
            methods_metrics.extend(mt_metrics)
    
    methods_metrics_df = pd.DataFrame(methods_metrics, 
                                      columns =['method', 'condition', 'metric', 'value'])
    
    methods_metrics_df = methods_metrics_df.pivot(index = ['condition', 'metric'],
                                                  columns = 'method',
                                                  values = 'value')
    
    methods_metrics_df = methods_metrics_df.round(decimals = 4)

    dataframe_file = stats_dir + '\\global_comparison_methods_conds.csv'
    methods_metrics_df.to_csv(dataframe_file)


#local per condition
def compare_methods_conds_local(stats_dir, methods):
    d_stats = []
    
    for m_name, m_data in methods.items():
        
        m_conds = split_data(m_data, 'condition')
        
        for c_name, mt_data in m_conds.items():
            
            for d in dependent_vars:
                
                stats = local_stats(mt_data, d)
                
                mt_stats = zip(repeat(m_name), repeat(c_name), repeat(d),
                                stats_vars, stats)
                d_stats.extend(mt_stats)
            
            
    d_stats_df = pd.DataFrame(d_stats, 
                              columns =['method', 'condition', 'metric',
                                         'stats', 'value'])
    
    d_stats_df = d_stats_df.pivot(index = ['condition', 'metric', 'stats'],
                                  columns = 'method',
                                  values = 'value')
    
    d_stats_df = d_stats_df.round(decimals = 4)
    
    dataframe_file = stats_dir + '\\local_comaprison_methods_conds.csv'
    d_stats_df.to_csv(dataframe_file)

#compare local FDR
def compare_FDR_conds_local(stats_dir, methods):
    d_stats = []
    
    for m_name, m_data in methods.items():
        
        m_conds = split_data(m_data, 'condition')
        
        for c_name, mt_data in m_conds.items():
            
            stats = FDR_stats(mt_data)
            
            mt_stats = zip(repeat(m_name), repeat(c_name),
                            stats_vars, stats)
            d_stats.extend(mt_stats)
            
            
    d_stats_df = pd.DataFrame(d_stats, 
                              columns =['method', 'condition',
                                         'stats', 'value'])
    
    d_stats_df = d_stats_df.pivot(index = ['condition', 'stats'],
                                  columns = 'method',
                                  values = 'value')
    
    d_stats_df = d_stats_df.round(decimals = 4)
    
    dataframe_file = stats_dir + '\\local_comaprison_FDR_conds.csv'
    d_stats_df.to_csv(dataframe_file)

# II. Within Methods

#global
def compare_vars_conds_global(stats_i_dir, mi_split, m_name, i):
     i_metrics = []
     
     for i_name, mi_data in mi_split.items():
         
         mi_conds = split_data(mi_data, 'condition')

         for c_name, mic_data in mi_conds.items():
         
             metrics = global_metrics(mic_data)
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
            
     
#local
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

#FDR
def compare_vars_FDR_conds_local(stats_i_dir, mi_split, m_name, i):
    d_stats = []
    
    for i_name, mi_data in mi_split.items():
        
        mi_conds = split_data(mi_data, 'condition')
        
        for c_name, mic_data in mi_conds.items():
            
                stats = FDR_stats(mic_data)
                m_stats = zip(repeat(m_name), repeat (i_name), repeat(c_name),
                              stats_vars, stats)
    
                d_stats.extend(m_stats)
                
                d_stats_df = pd.DataFrame(d_stats,
                                          columns = ['method', i, 'condition', 
                                                     'stats', 'value'])
                
                d_stats_df = d_stats_df.pivot(index = ['method', 'condition', 'stats'],
                                              columns = i,
                                              values = 'value')
                
                d_stats_df = d_stats_df.round(decimals = 4)
                
                dataframe_file = stats_i_dir + '\\local_comparison_FDR_' + i + '_conds.csv'
                d_stats_df.to_csv(dataframe_file)
 
    
#plots for local tests
def plots_vars_conds_local(stats_i_dir, m_split, m_name, i):
    
    stats_plots_dir = stats_i_dir + '\\plots'
    do_dir(stats_plots_dir)
  
    m_conds = split_data(m_split, 'condition')

    for c_name, mt_data in m_conds.items(): #for each cond
        
    #split per d
        for d in dependent_vars: #for each metric
            
            plot = sb.violinplot(data=mt_data, 
                                 x=i, y=d)
            file = stats_plots_dir + '\\' + d + '_' + c_name + '_violin.png'
            plot.get_figure().savefig(file)
            plot.get_figure().clear()
            
def cohen_d(data, popmean):
    return abs((data.mean() - popmean)/data.std())

#test difference between data aprameter values
def test_diff_conds_local(stats_i_dir, m_split, m_name, i):
    
    stats_tests_dir = stats_i_dir + '\\tests'
    do_dir(stats_tests_dir)
  
    m_conds = split_data(m_split, 'condition')

    for c_name, mt_data in m_conds.items(): #for each cond
        
    #split per d
        for d in dependent_vars: #for each metric
            
            ids = list(set(['method', 'condition'] + independent_vars) - set([i]))    
            d_data = mt_data.pivot(index = ids,
                                   columns = i,
                                   values = d)
            
            #matrix
            d_matrix = []
            
            
            #calcualte differences
            vals = mt_data[i].unique()
            for v1 in vals:
                for v2 in vals:
                    v_diff = d_data[v1] - d_data[v2]
                    
                    #print('mean', v_diff.mean(), 'sd', v_diff.std())
                    #sb.displot(v_diff)

                    #test normality beforehand
                    t_stat, p_val = scipy.stats.shapiro(v_diff)
                    
                    normality = p_val < 0.05
                    
                    if normality:
                        #t_test
                        t_stat, p_val = scipy.stats.ttest_1samp(v_diff, 
                                                                popmean = 0,
                                                                alternative = 'two-sided')
                        
                        #print('p_val', p_val)
                        effect_size = cohen_d(v_diff, 0)
                        #print('cohen d', effect_size)
                        reject = (p_val < 0.05) and (effect_size > 0.8)
                        #print('reject', reject)
                        
                    #sample not representative of population => small p val
                    
                    else:
                        reject = None
                    
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
    
    
    #local stats
    compare_methods_conds_local(stats_dir, methods)
    
    #global metrics
    compare_methods_conds_global(stats_dir, methods)
    
    #FDR
    compare_FDR_conds_local(stats_dir, methods)

    #within methods & conditions (vars)
    for m_name, m_data in methods.items():
        
        #create directory
        stats_m_dir = stats_dir + '\\' + m_name
        do_dir(stats_m_dir)
        
        for i in independent_vars:

            #create directory
            stats_i_dir = stats_m_dir + '\\' + i
            do_dir(stats_i_dir)
        
            mi_data = split_data(m_data, i)
                        
            #local stats
            compare_vars_conds_local(stats_i_dir, mi_data, m_name, i)
            
            #global metrics
            compare_vars_conds_global(stats_i_dir, mi_data, m_name, i)
            
            #FDR
            compare_vars_FDR_conds_local(stats_i_dir, mi_data, m_name, i)
            
            #plots
            plots_vars_conds_local(stats_i_dir, m_data, m_name, i)
            
            #tests
            #test_diff_conds_local(stats_i_dir, m_data, m_name, i)


#make sure it's commented out before running lat statistics
#get_stats()


    

    



