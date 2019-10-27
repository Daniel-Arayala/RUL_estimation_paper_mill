import os
import fnmatch
import pandas as pd
import pytz
import matplotlib.pyplot as plt
import numpy as np
import itertools


def count_repeated(x):
    global count
    if x == 0:
        count = count + 1
    else:
        count = 0
    return count 


# #data engineering
# Create a feature that marks how many minutes the information has been freezed
def count_change(df, col, new_col_name):
    actual_minus_previus = df[col].shift(1) - df[col]  #subtraction with shift to mark changes
    df = pd.concat([df, actual_minus_previus.rename('Sub')], axis=1)  # concat
    df[new_col_name] = df['Sub'].apply(lambda x: count_repeated(x))  #count minutes without change
    df = df.drop(columns=['Sub']) 
    df[new_col_name] = pd.to_numeric(df[new_col_name])  #converte tudo para numerico
    return df
    
def spike_mark(x, b_increment):
    global count
    if x != 0 :
        count = count + 1
    else:
        if not(b_increment):
            count = 0
    return count 


# data engineering
# Create a feature that count the number of times the freeze efect happens
def count_pikes(df, col, new_col_name, b_increment=False):
    actual_minus_previus = df[col].shift(1) - df[col] #subtraction with shift to mark changes
    df = pd.concat([df, actual_minus_previus.rename('Sub')], axis=1)  # concat
    
    df[new_col_name] = df['Sub'].apply(lambda x: spike_mark(x,b_increment)) #count minutes without change
    
    df = df.drop(columns=['Sub']) 
    df[new_col_name]=pd.to_numeric(df[new_col_name]) #converte tudo para numerico
    return df