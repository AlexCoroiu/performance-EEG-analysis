# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:38:39 2022

@author: User
"""

# def create_concat_epo(epos):
#     dataset = c.DATA_DIR

#     concat_epo = mne.concatenate_epochs(epos)
#     concat_epo_file =  dataset + '\\concat' + '_epo.fif'
#     concat_epo.save(concat_epo_file, overwrite = True)
    
# def load_concat_epo():
#     dataset = c.DATA_DIR
    
#     concat_epo_file =  dataset + '\\concat' + '_epo.fif'
#     concat_epo = mne.read_epochs(concat_epo_file)
    
#     return concat_epo
    
# def create_epo_dfs(epos):
#     # (part, condition, epoch, time, electrode, value)
#     dataset = c.EPO_DFS_DIR
    
#     if not os.path.exists(dataset):
#         os.mkdir(dataset)
    
    
#     for p in range(c.NR_PARTICIPANTS):
#         nr = str(p + 1)
#         part = "part" + nr
#         epo_part = epos[p]
        
#         #save epoched as pandas dataframe
#         dataframe = epo_part.to_data_frame(long_format = True)
        
#         #print(dataframe.columns)
    
#         dataframe['part'] = nr
#         columns = ['part', 'condition', 'epoch', 'time', 'channel', 'value']
#         dataframe = dataframe[columns]
        
#         #save
#         dataframe_file = dataset + '\\' + part + '.csv'
#         dataframe.to_csv(dataframe_file)
    
# def load_epo_dfs():
#     dataset = c.EPO_DFS_DIR
    
#     epo_dfs = []
    
#     for p in range(c.NR_PARTICIPANTS):
#         part = "part" + str(p + 1)
        
#         epo_df_file = dataset +  '\\' + part + '.csv'
#         epo_df_part = pd.read_csv(epo_df_file)
        
#         epo_dfs.append(epo_df_part)
    
#     return epo_dfs

# def create_epo_concat_df(epo_dfs):
#     dataset = c.DATA_DIR
    
#     epo_dataframe = pd.concat(epo_dfs, axis=0) #very computationally heavy
#     dataframe_file = dataset + '\\epo_dataframe' + '.csv'
#     epo_dataframe.to_csv(dataframe_file)
    
    
# def load_epo_concat_df():
#     dataset = c.DATA_DIR
    
#     dataframe_file = dataset + '\\epo_dataframe' + '.csv'
#     epo_dataframe = pd.read_csv(dataframe_file)
    
#     return epo_dataframe

# def create_avg_evo(concat_epo):
#     #create concatanated evokeds - population average
#     dataset = c.DATA_DIR
#     avg_evo = []
    
#     for event in c.EVENT_NAMES:
            
#         condition = concat_epo[event]
        
#         #evoked data
#         evoked = condition.average() #average or gfp
        
#         avg_evo.append(evoked)
    
#     avg_evo_file = dataset + '\\avg' + '_ave.fif'
#     mne.write_evokeds(avg_evo_file, avg_evo)

# def load_avg_evo():
#     dataset = c.DATA_DIR
    
#     avg_evo_file =  dataset + '\\avg' + '_ave.fif'
#     avg_evo = mne.read_evokeds(avg_evo_file)
    
#     return avg_evo

# def create_avg_df(avg_evo):
#     # (condition, time, electrode, value)
    
#     dataset = c.DATA_DIR
#     dfs = []
    
#     for evoked in avg_evo:
#         df = evoked.to_data_frame(long_format = True)
#         condition = evoked.comment
#         df['condition'] = condition
#         columns = ['condition', 'time', 'channel', 'value']
#         df = df[columns]
#         dfs.append(df)
        
#     dataframe = pd.concat(dfs, axis=0)
#     dataframe_file = dataset + '\\avg_df' + '.csv'
#     dataframe.to_csv(dataframe_file)
    
# def load_avg_df():
#     dataset = c.DATA_DIR
    
#     dataframe_file = dataset + '\\avg_df' + '.csv'
#     avg_dataframe = pd.read_csv(dataframe_file)
    
#     return avg_dataframe

'''
#infinite impulse response filter
#high pass filter for 0.1 Hz frequencies
NOISE_FILTER = (0.1,-0.1,0.02)
#the bigger the iir filter values, the less noise (signal-noise ratio)
#(0.1,-0.1,0.02)
#(0.2,-0.2,0.04)

# #noise levels variables
# #+/-0.1 ??? the lower the value, the more amp
# #smth related to the noise freq (check psd plot)
# #0.04 ???? the lower the value, the higehr noise freq

#fit_iir_model_raw????

'''

#baseline correction - a type of high pass filtering