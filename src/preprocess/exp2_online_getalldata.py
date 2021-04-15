# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:20:00 2020
This script collects each participant raw data, and write to one file.
All NaN response and redundant columns are removed.
Valide responseN was converted to int 
output: 'clean_totalData.xlsx' (need to be pre-processed)

@author: Miao
"""
import os, copy
import pandas as pd

from src.commons.process_dataframe import insert_new_col
from src.commons.process_str import imageFile_to_number3, raw_resp_to_int

if __name__ == '__main__':
    to_excel = False

    # list raw data files
    files = os.listdir(os.chdir("../../data/exp2_data_online/raw_data"))

    # collect all raw fiels
    data_csv = [file for file in files if file.startswith('P') & file.endswith('csv')]

    # read data files
    totalData = pd.DataFrame()
    for i in data_csv:
        data_exp2_online = pd.read_csv(i)
        totalData = totalData.append(data_exp2_online)

    # first clean - remove useless columns

    # get column names
    col_names = []
    for col in totalData.columns:
        col_names.append(col)

    # make a copy for all column names
    all_col_names = copy.deepcopy(col_names)

    keptcolumns = ['responseN', 'participantID', 'age', 'blockOrder', 'sex', 'imageFile', 'blocks.thisIndex']

    # get dropped names
    dropped = []
    for col in all_col_names:
        if col not in keptcolumns:
            dropped.append(col)

    # get data with kept columns
    totalData = totalData.drop(dropped, axis = 1)

    # remove rows with NaN
    totalData = totalData.dropna()

    # check responseN columns
    totalData['responseN'].apply(type).value_counts()
    #totalData['responseN_Type'] = totalData['responseN'].apply(lambda x: type(x).__name__)

    # convert response to int
    totalData['responseN'] = totalData['responseN'].apply(raw_resp_to_int)

    # remove rows with NaN after convert all response to srting
    totalData = totalData.dropna()

    # map all needed columns from imageFile
    insert_new_col(totalData, "imageFile", "Ndisplay", imageFile_to_number3)
    totalData['Ndisplay'] = totalData['Ndisplay'].astype(int) #change to int

    # reset index
    totalData = totalData.reset_index(drop = True)

    # read stimuli file
    stimuli = pd.read_excel('../../../displays/exp2_stim_info.xlsx')

    # map totalData with stimulus properties
    totalData = pd.merge(totalData, stimuli, how = 'left', on = ['Ndisplay'])

    # get deviation
    totalData['deviation'] = totalData['responseN'] - totalData['Numerosity']

    # write to excel
    if to_excel:
        totalData.to_excel('../../../src/preprocess/try.xlsx')