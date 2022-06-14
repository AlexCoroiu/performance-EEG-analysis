# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:36:41 2022

@author: User
"""

#%%selection
import constants as c
import os.path
import pandas as pd

#%%
#set up

# def create_data_points(dataframe):
    
#     data_points = dataframe[['time','channel']].drop_duplicates()
    
#     dataset = c.DATA_POINTS
#     if not os.path.exists(dataset):
#         os.mkdir(dataset)

#     #part x condition x time x electrode
#     print(dataframe.head(5))
#     print(dataframe.tail(5))
    
#     #re-shape dataframe
#     #part | time | condition | baseline | visual-left | visual-right
#     wide_dataframe = dataframe.pivot(index=['part','time', 'channel'], 
#                     columns='condition', 
#                     values='value')
    
#     print(wide_dataframe.head(5))
#     print(wide_dataframe.tail(5))
    
#     #descriptives
#     wide_dataframe[c.EVENT_NAMES].describe()
    
#     #split by time x electrode
#     grouped_dataframe = wide_dataframe.groupby(by = ['time','channel'])
#     print(grouped_dataframe.head(5))
#     print(grouped_dataframe.tail(5))

    
#     split_df = {}
    
#     for i,row in data_points.iterrows():
#         dp = (row['time'],row['channel'])
#         group = grouped_dataframe.get_group(dp)
#         split_df[dp] = group
    
#     print(split_df)
    
#     for dp in split_df:
#         dataframe_file = dataset + '\\' + str(dp[0]) + "_" + dp[1] + '.csv'
#         split_df[dp].to_csv(dataframe_file)
        
# def load_data_points(dataframe):

#     data_points = dataframe[['time','channel']].drop_duplicates()
    
#     dataset = c.DATA_POINTS
    
#     dps = {}
    
#     for i,row in data_points.iterrows():
#         dp = (row['time'],row['channel'])
#         dp_file =  dataset + '\\' + str(dp[0]) + "_" + dp[1] + '.csv'
#         dp_values = pd.read_csv(dp_file)
#         dps[dp] = dp_values
    
#     return dps


#%%
# average baseline? for testing

#%%

# ELECT RELEVANT DATA
# select testing window

# select electrodes




