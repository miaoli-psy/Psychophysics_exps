# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:15:04 2020

@author: Miao
"""
import os, math
import pandas as pd
# current path
cur_path = os.getcwd()

# change to data folder
dataptah = os.chdir("../../numerosity_exps/data/data")

# read the totalData file
totalData = pd.read_excel('clean_totalData.xlsx', index_col = 0)

# =============================================================================
# remove outliers
# =============================================================================

#remove obvious outliers - typos
totalData = totalData[(totalData['responseN'] < 100) & (totalData['responseN'] > 5)]

# per winsize - obvious outliers
lim04_x, lim04_y = round(math.sqrt(34)), 44*2
lim06_x, lim06_y = round(math.sqrt(58)), 68*2

# sperate data for each winsize
w04_data = totalData[totalData.winsize == 0.4]
w06_data = totalData[totalData.winsize == 0.6]

# keep response within lim
w04_data = w04_data[(w04_data['responseN'] < lim04_y) & (w04_data['responseN'] > lim04_x)]
w06_data = w06_data[(w06_data['responseN'] < lim06_y) & (w06_data['responseN'] > lim06_x)]

# keep data within 2 std
w04_resp_std  = w04_data['responseN'].std()
w06_resp_std  = w06_data['responseN'].std()

w04_resp_mean = w04_data['responseN'].mean()
w06_resp_mean = w06_data['responseN'].mean()

w04_resp_min, w04_resp_max  = w04_resp_mean - 2*w04_resp_std, w04_resp_mean + 2*w04_resp_std
w06_resp_min, w06_resp_max  = w06_resp_mean - 2*w06_resp_std, w06_resp_mean + 2*w06_resp_std

# data keeped within 2 std
w04_data2std = w04_data[(w04_data['responseN'] < w04_resp_max) & (w04_data['responseN'] > w04_resp_min)] #94.2%trails are kept
w06_data2std = w06_data[(w06_data['responseN'] < w06_resp_max) & (w06_data['responseN'] > w06_resp_min)] #94.0%trails are kept; altohether, 94.1% trails are kept

# =============================================================================
# conbined data
# =============================================================================
totalData = pd.concat([w04_data2std,w06_data2std], ignore_index = True) # response within 2std
#totalData = pd.concat([w04_data,w06_data], ignore_index = True) # response removed obvious outliers only

#to excel if needed
totalData.to_excel('../try.xlsx')
# =============================================================================
# pivot table
# =============================================================================
pT  = pd.pivot_table(totalData, index = ['crowding', 'participantID'], columns = ['winsize', 'Numerosity'], values = ['deviation'])
pT2 = pd.pivot_table(totalData, index = ['crowding', 'participantID'], columns = ['winsize', 'clustering'], values = ['deviation'])
pT3 = pd.pivot_table(totalData, index = ['crowding', 'participantID'], columns = ['winsize', 'Numerosity','clustering'], values = ['deviation'])

# write to excel
#pT3.to_excel('../try3.xlsx')




