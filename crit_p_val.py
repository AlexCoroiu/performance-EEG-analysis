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

# variables
processing_vars = ['window_size', 'time_interval', 'density', 'location']
dependent_vars = ['type_I_ER', 'type_II_ER', 'FDR']
stats_vars = ['M', 'SD']

def p_val_metrics(data, p_dir):
    do_dir(p_dir)
    # plot scatter
    for d in dependent_vars:
        plot = sb.lmplot(data=data,
                         x='crit_p_val', y=d,
                         col='condition',  # col, hue or row
                         col_wrap=2,
                         scatter=True,
                         fit_reg=True,
                         sharex=True,
                         sharey=True)
        file = p_dir + '\\scatter_' + d + '_conds.png'

        for ax in plot.axes.flat:
            ax.axhline(0.05, ls='--')

        plot.savefig(file)
        plot.fig.clf()

def vars_metrics(data, p_dir):
    do_dir(p_dir)
    # plot scatter
    for i in processing_vars:
        for d in dependent_vars:
            plot = sb.lmplot(data=data,
                             x='total', y=d,
                             hue=i,  # hue or row
                             col='condition',
                             col_wrap=2,
                             scatter=True,
                             fit_reg=True,
                             sharex=True,
                             sharey=True)
            file = p_dir + '\\scatter_' + d + '_' + i + '_conds.png'

            for ax in plot.axes.flat:
                ax.axhline(0.05, ls='--')

            plot.savefig(file)
            plot.fig.clf()


def p_val_total(data, p_dir):
    do_dir(p_dir)
    
    data_plot = data.rename(columns = {'total':'dataset_size'})
    
    plot = sb.relplot(data=data_plot,
                      x='dataset_size', y='crit_p_val')
    file = p_dir + '\\p_val.png'

    min_tests = data['total'].min()
    max_tests = data['total'].max()

    # print(min_tests,max_tests)

    x = np.linspace(min_tests, max_tests, max_tests)
    #y = 2*np.sqrt(0.05/x)
    y = (1/2)*np.sqrt(0.05/x)
    plt.plot(x, y)

    plot.savefig(file)
    plot.fig.clf()


def total_metrics(data, p_dir):
    do_dir(p_dir)
    # plot scatter
    
    data_plot = data.rename(columns = {'total':'dataset_size'})
    for d in dependent_vars:
        plot = sb.lmplot(data=data_plot,
                         x='dataset_size', y=d,
                         col='condition',
                         col_wrap=2,
                         scatter=True,
                         fit_reg=True,
                         sharex=True,
                         sharey=True)
        #plot.refline(y = 0.05)
        file = p_dir + '\\total_tests_' + d + '.png'

        for ax in plot.axes.flat:
            ax.axhline(0.05, ls='--')

        plot.savefig(file)
        plot.fig.clf()


def global_sig(data, p_dir):
    do_dir(p_dir)
    
    #create eprcentage data
    conditions = data['condition'].unique()

    percentage_conds = []

    for cond in conditions:
        data_c = data[data['condition'] == cond]
        data_c = data_c.groupby('total')['global_significant'].value_counts(normalize = True)
        data_c = data_c.mul(100).rename('percent_significant').reset_index()
        data_c['condition'] = cond
        percentage_conds.append(data_c)
        
    percentage_data = pd.concat(percentage_conds)
    
    percentage_data = percentage_data[['condition', 'total', 
                                       'global_significant', 'percent_significant']]
    
    print(percentage_data)
    
    percentage_data = percentage_data[percentage_data['global_significant'] == True]
    
    dataframe_file = p_dir + '\\percentage.csv'
    percentage_data.to_csv(dataframe_file)
    
    #plot
    percentage_data = percentage_data.rename(columns = {'total':'dataset_size'})
    
    plot = sb.lmplot(data=percentage_data,
                    x='dataset_size', y='percent_significant',
                    col='condition',
                    col_wrap=2,
                    scatter = True,
                    fit_reg=False,
                    sharex=True,
                    sharey=True)
    #plt.ylim(0,100)
                    
    file = p_dir + '\\global.png'

    for ax in plot.axes.flat:
        ax.axhline(5, ls='--')
        
    plot.savefig(file)
    plot.fig.clf()
    

def positive_rate(data):
    data_base = data[(data['condition'] == 'baseline') |
                     (data['condition'] == 'lat_baseline')]

    data_base_sig = data_base[data_base['global_significant'] == True]

    print(data_base_sig['positives'].describe())
    print(data_base_sig['type_I_ER'].describe())


def determine_p_val():
    # SETUP
    # load final results
    data_ERP = pd.read_csv('results.csv')
    data_lat = pd.read_csv('lat_results.csv')

    data_tests = {'diff': data_ERP, 'lat': data_lat}

    for d_name, data in data_tests.items():
        p_dir = 'p_val_' + d_name
        do_dir(p_dir)

        data = data[data['method'] == 'mc_w']

        positive_rate(data)

        # FDR
        data['FDR'] = data['FP']/data['positives']

        # asses p val calcualtion
        #p_val_metrics(data,p_dir)

        #total_metrics(data,p_dir)

        #vars_metrics(data, p_dir)

        #global_sig(data, p_dir)

        p_val_total(data, p_dir)


determine_p_val()
