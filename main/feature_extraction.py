import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_wnd_pkt_num(df, wnd_size):
    t0 = df["EpochArrivalTime"][0]
    dt = df["EpochArrivalTime"][1]-t0
    t = 0
    i = 0
    while t + dt < wnd_size: 
        t += dt
        i += 1 
        dt = df["EpochArrivalTime"][i+1]-df["EpochArrivalTime"][i]
    return (i, df["EpochArrivalTime"][i])

def get_wnd_pkt_num_arr(df, t_seconds):
    pkt_num_arr = [get_wnd_pkt_num(df,t_seconds)]
    
    for i in range(pkt_num_arr[0][0]+1, len(df)):
        dt=df["EpochArrivalTime"][i]-df["EpochArrivalTime"][i-1]
        t=0; j=i; ctr=0
        while t+dt<t_seconds:
            t+=dt; j-=1; ctr+=1
            dt=df["EpochArrivalTime"][j]-df["EpochArrivalTime"][j-1]
        pkt_num_arr.append((ctr, df.loc[i, "EpochArrivalTime"]))
    return pkt_num_arr

def get_num_of_same(df, attr, idx, pkt_num):
    num_of_same = 0
    value = df[attr][idx]
    for i in range(idx-1, idx-pkt_num, -1):
        if df[attr][i] == value:
            num_of_same += 1
    
    return num_of_same

def get_num_of_same_arr(df, attr, pkt_num):
    num_of_same_arr = []
    for i in range(len(pkt_num)):
        num_of_same_arr.append(get_num_of_same(df, attr, pkt_num[0]+i, pkt_num[i]))
    return num_of_same_arr

def shift_attack_indexes(attack_indexes, pkt_num):
    return list(np.array(attack_indexes)-pkt_num[0][0])

def reshift_attack_indexes(shifted_attack_indexes, pkt_num):
    return list(np.array(shifted_attack_indexes)+pkt_num[0][0])

def get_avg(df, attr, idx, pkt_num):
    sum = df[attr][idx]
    for i in range(idx-1, idx-pkt_num, -1):
        sum += df[attr][i]
    return sum/pkt_num


def get_avg_arr(df, attr, pkt_num):
    avg_arr = []
    for i in range(len(pkt_num)):
        avg_arr.append(get_avg(df, attr, pkt_num[0]+i, pkt_num[i]))
    return avg_arr

def get_num_of_all(df, attr, idx, pkt_num):
    counter = 0
    memory = []
    for i in range(idx-1, idx-pkt_num, -1):
        current_value = df[attr][i]
        if current_value not in memory:
            counter += 1
            memory.append(current_value)
    return counter

def get_num_of_all_arr(df, attr, pkt_num):
    num_of_all = []
    for i in range(len(pkt_num)):
        num_of_all.append(get_num_of_all(df, attr, pkt_num[0]+i, pkt_num[i]))
    return num_of_all

def get_num_of_previous(df, attr, idx, pkt_num):
    num_of_prev = 0
    value = df[attr][idx-1]
    for i in range(idx-1, idx-pkt_num, -1):
        if df[attr][i] == value:
            num_of_prev += 1
    return num_of_prev

def get_num_of_previous_arr(df, attr, pkt_num):
    num_of_prev_arr = []
    for i in range(len(pkt_num)):
        num_of_prev_arr.append(get_num_of_previous(df, attr, pkt_num[0]+i, pkt_num[i]))
    return num_of_prev_arr

def get_num_of_not_previous_nor_same(df, attr, idx, pkt_num):
    num = 0
    value_same = df[attr][idx]
    value_prev = df[attr][idx-1]
    for i in range(idx-1, idx-pkt_num, -1):
        if df[attr][i] != value_same and df[attr][i] != value_prev:
            num += 1
    return num

def get_num_of_not_previous_nor_same_arr(df, attr, pkt_num):
    num_arr = []
    for i in range(len(pkt_num)):
        num_arr.append(get_num_of_not_previous_nor_same(df, attr, pkt_num[0]+i, pkt_num[i]))
    return num_arr

def get_num_of_greater_than_current(df, attr, idx, pkt_num):
    num = 0
    value_current = df[attr][idx]
    for i in range(idx-1, idx-pkt_num, -1):
        if df[attr][i] > value_current:
            num += 1        
    return num

def get_num_of_greater_than_current_arr(df, attr, pkt_num):
    num_arr = []
    for i in range(len(pkt_num)):
        num_arr.append(get_num_of_greater_than_current(df, attr, pkt_num[0]+i, pkt_num[i]))
    return num_arr

# features:
# "wnd_avg_goose_pkt_interval","wnd_avg_goose_data_length", "wnd_goose_pkt_num",
# "wnd_goose_pkt_num_of_same_event","wnd_goose_pkt_num_of_previous_event",
# "wnd_goose_pkt_num_of_not_previous_nor_same_event","wnd_goose_num_of_all_events",
# "wnd_goose_pkt_num_of_same_sqNum","wnd_goose_pkt_num_of_greater_than_current_sqNum",
# "wnd_goose_pkt_num_of_same_datSet","wnd_goose_pkt_num_of_all_datSet"

def get_dos_features(df, wnd_size = 2):
    
    pkt_num = get_wnd_pkt_num_arr(df, wnd_size)
    
    df_new = pd.DataFrame()
    df_new["wnd_avg_goose_pkt_interval"] = get_avg_arr(df, "timeInterval", [x[0] for x in pkt_num])
    df_new["wnd_avg_goose_data_length"] = get_avg_arr(df, "Length", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num"] = [x[0] for x in pkt_num]
    df_new["wnd_goose_pkt_num_of_same_event"] = get_num_of_same_arr(df, "stNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_previous_event"] = get_num_of_previous_arr(df, "stNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_not_previous_nor_same_event"] = get_num_of_not_previous_nor_same_arr(df, "stNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_num_of_all_events"] = get_num_of_all_arr(df, "stNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_same_sqNum"] = get_num_of_same_arr(df, "sqNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_greater_than_current_sqNum"] = get_num_of_greater_than_current_arr(df, "sqNum", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_same_datSet"] = get_num_of_same_arr(df, "datSet", [x[0] for x in pkt_num])
    df_new["wnd_goose_pkt_num_of_all_datSet"] = get_num_of_all_arr(df, "datSet", [x[0] for x in pkt_num])

    attack_indexes = [i for i, val in enumerate(df["label"]) if val]
    shifted_attack_indexes = shift_attack_indexes(attack_indexes, pkt_num)
    labels = [True if i in shifted_attack_indexes else False for i in range(len(df_new.index))]
    df_new = df_new.assign(label=labels)
    return df_new

def plot_feature(df, feature):
    plt.scatter(df.index, df[feature], color='blue', label='Normal')
    plt.scatter(df.index[df['label']], df[feature][df['label']], color='red', label='Malicious')
    plt.xlabel('Index')
    plt.ylabel(feature)
    plt.legend()
    plt.show()