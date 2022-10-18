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
NOISE

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

'''
WAVEFORM CREATION

time_latency = times - latency
    sinusoid = np.sin(2 * np.pi * f_band * time_latency)
    #time latency has to be used here for the actual time delay
    #plt.plot(times, sinusoid)
    #plt.show()
    var = 0.2 * duration #width of the gaussian function 
    sd = var ** 2
    shift = var/4
    
    #if duration changes than the shape of the signal changes as well --> invariable duration

    #position of the gaussian max
    gf = np.exp(-(time_latency + shift) ** 2 / #+/- gf is left/right of sin 0 (where polarity changes)  
                (sd*2)) #68% interval
    
    #duration bigger than altency than you ge ta shift too much to the right
    
    #!position of the gf comapred to the sinusoid
    #plt.plot(times,gf)
    #plt.show()
    wave = 1e-10 * sinusoid * gf
    #plt.plot(times, wave)
    #plt.show
    return wave
'''

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

#!!! always call concat only once, after the loop adds all dfs to a list

#!!! always index = False when saving pandas to csv

#!!! to csv overwrites by default

#!!! for and if does not introduce new scope in python, only functons do

'''
#windows used
window_ms = int(window*1000)
t_max = int(c.T_MAX*1000)
nr_windows = int(t_max/window_ms) + 1

#electrodes used
electrodes = c.DENSITY[density] 
if local:
    electrodes = list(set(electrodes) & set(c.CHANNELS_VISUAL))
'''


'''
reject ('null hypothesis'):
    False = not significant
    True = significant
'''

#extract t statistics for all data points in sig clusters
#t_sig_clusters = [t_stats[c] for c in sig_clusters]

#significant_points = cluster_pv.reshape(t_obs.shape).T < .05
#print(t_sig_clusters)


#MULTIINDEX
# multids = pd.MultiIndex.from_product([windows, electrodes],
#                                         names = ['time', 'channel'])
    
# results = pd.DataFrame(index = multids)


"""
    
    # t_count = len(analysed)
    # ch_count = len(analysed['channel'].unique())
    # t_count = len(analysed['time'].unique())
"""


#diff way to calcualte total and crit p val
#total tests performed
# window_ms = int(window_size*1000)
# time = math.floor((c.TEST_INTERVAL_MAX - c.TEST_INTERVAL_MIN)/window_ms) #rounded down
# electrodes =  density
# if local:
#     electrodes = c.DENSITY[density]
#     electrodes = len(list(set(electrodes) & set(c.CHANNELS_VISUAL)))

# total = time * electrodes


"""

CLUSTER PERMUTATION OLD FORMAT (time x channel and all clusters)
    
    #select significant clusters
    sig_clusters_ids = np.where(p_val_clusters < c.SIGNIFICANCE)[0]
    sig_clusters = [clusters[i] for i in sig_clusters_ids]
    
    print(sig_clusters)
    
    results = pd.DataFrame(columns = ['time', 'channel'])
    print(results) #empty df

    i = 1

    for cluster in sig_clusters:
        print(cluster.shape)
        shape = (nr_windows*nr_electrodes, 1)
        
        cluster_df = pd.DataFrame(data = cluster,
                                  index = windows,
                                  columns = electrodes)
        
        cluster_df.index.names = ['time']

        #print(cluster_df) #matrix
        
        cluster_name = 'cluster' + str(i)
        cluster_df = cluster_df.melt(ignore_index = False,
                                     var_name = 'channel',
                                     value_name = cluster_name)
        i = i+1
    
        cluster_df = cluster_df[cluster_df[cluster_name] == True]
        
        print(cluster_df)
        
        #add as column to results
        results = pd.merge(results, cluster_df, how = 'outer', #union
                       left_on = ['time', 'channel'],
                       right_on = ['time', 'channel'])
        
    print(results)
        
    return results
        
    
    #return sig. cluster data points (times and electrodes)
    #dataframe format?
    
"""

"""

CLUSTER PERMUTATION OLD FORMAT RESULTS

sig = load_analysed(window_size,density,local,cond,'cp')

#sig cluster count
clusters = list(set(sig.columns.tolist()) - set(['time', 'channel']))
sig_count = len(clusters)

#TP
tp_clusters = []
for clust in clusters:
    cluster_df = sig[['time','channel',clust]]
    
    #retain only cluster vars
    cluster_df = cluster_df[cluster_df[clust] == True]
    
    #add only columns which contain true positives for vals in signal criteria
    cluster_df = cluster_df[(cluster_df['time'] <= c.SIG_INTERVAL_MAX) &
                            (cluster_df['time'] >= c.SIG_INTERVAL_MIN)]
    cluster_df = cluster_df[cluster_df['channel'].isin(c.CHANNELS_VISUAL)]
    
    #if there is any sig data point in the cluster, consider it a true positive
    if cluster_df.shape[0] > 0:
        tp_clusters.append(clust)
    
tp_count = len(tp_clusters)

#FP
fp_count = sig_count - tp_count

#TN

#FN

#precision
if sig_count != 0:
    precision = tp_count/sig_count
else:
    precision = 0

#vars that don't exist for this method
total = None
crit_p_val = None


#save
return [window_size, density, local, 
        cond, 'cp', 
        crit_p_val, total, 
        sig_count, tp_count, fp_count, precision] 

"""

"""
CLUSTER PERMUTATION OLD FORMAT FINAL RESULTS
#TP
tp_clusters = []
for clust in clusters:
    cluster_df = sig[['time','channel',clust]]
    
    #retain only cluster vars
    cluster_df = cluster_df[cluster_df[clust] == True]
    
    #add only columns which contain true positives for vals in signal criteria
    cluster_df = cluster_df[(cluster_df['time'] <= c.SIG_INTERVAL_MAX) &
                            (cluster_df['time'] >= c.SIG_INTERVAL_MIN)]
    cluster_df = cluster_df[cluster_df['channel'].isin(c.CHANNELS_VISUAL)]
    
    #if there is any sig data point in the cluster, consider it a true positive
    if cluster_df.shape[0] > 0:
        tp_clusters.append(clust)
        
"""

"""

CONFUSION MATRXI WITHOUR SKLEARN
def extract_actual_mc(predicted):
    predicted_count = len(predicted)
    
    #actual positives found in predicted values
    #expected time interval
    positives = predicted[(predicted['time'] <= c.SIG_INTERVAL_MAX) &
                          (predicted['time'] >= c.SIG_INTERVAL_MIN)] #must use bit wise boolean logic operators
    
    #expected electrode location
    positives = positives[positives['channel'].isin(c.CHANNELS_VISUAL)]
    
    positives_count = len(positives)
    
    #actual negatives found in predicted values
    negatives_count = predicted_count - positives_count 
    
    return (predicted_count, positives_count, negatives_count)

def extract_actual_cp(predicted):
    predicted_count = len(predicted)
    
    #actual positives
    positives = predicted[any(((datapoint[0] <= c.SIG_INTERVAL_MAX & 
                               datapoint[0] >= c.SIG_INTERVAL_MIN) & 
                              datapoint[1].isin(c.CHANNELS_VISUAL))
                              for datapoint in predicted['data_points'])] 
    
    positives_count = len(positives)
    
    #actual negatives found in predicted values
    negatives_count = predicted_count - positives_count                      
    
    return (predicted_count, positives_count, negatives_count)
"""


"""
#CONFUSION MATRIX
#sig cluster count
predicted_positive = analysed[analysed['significant'] == True]
P_count, TP_count, FP_count = extract_actual_cp(predicted_positive)

#non significant test results
predicted_negative = analysed[analysed['significant'] == False]   
N_count, FN_count, TN_count = extract_actual_cp(predicted_negative)

#METRICS
precision = calcualte_metrics(P_count, TP_count, FP_count, 
                              N_count, TN_count, FN_count)
"""