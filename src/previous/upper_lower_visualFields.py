#-*- coding: utf-8 -*-
"""
Created on Wed Dec 06 16:36:27 2019

@author: MiaoLi
"""
#%% =============================================================================
# IMPORTANT! This code converts pix to degree of visual angle directly
# e.g. in the algorithm, we removed a foveal region of r = 100 (pix),
# therefore, in visual angle degree, r = 3.839 deg
# =============================================================================
import os
import pandas as pd
import ast
import numpy as np
from math import pi
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
import copy
import operator
# convert pix to visual deg
k = 3.839/100
#%% =============================================================================
# upper/lower/quadrants visual fields
# =============================================================================
# get updated stimuli info
updated_stim_info_df = pd.read_excel('../update_stim_info.xlsx')

# positions of each display
posi_lists_temp = updated_stim_info_df['positions_list'].tolist()
posi_list=[]
for i in posi_lists_temp:
    i = ast.literal_eval(i)# megic! remore ' ' of the str
    posi_list.append(i)

up_posi_list    = []
low_posi_list   = []
up_r_posi_list  = []
up_l_posi_list  = []
low_r_posi_list = []
low_l_posi_list = []

# distinguish upper and lower visual fields; if y = 0, even index to upper visual field, odd index to lower visual field
for i, display in enumerate(posi_list):
    up_posi = []
    low_posi = []
    for posi in display:
        if posi[1] > 0:
            up_posi.append(posi)
        elif posi[1] < 0:
            low_posi.append(posi)
        else:

            if i%2 == 0:
                up_posi.append(posi)
            else:
                low_posi.append(posi)
    up_posi_list.append(up_posi)
    low_posi_list.append(low_posi)

# distinguish left and right visual fields; if x =0, even index to up-left visual field, odd index to up-right visual field
for i, half_display in enumerate(up_posi_list):
    left_posi = []
    right_posi = []
    for posi in half_display:
        if posi[0] < 0:
            left_posi.append(posi)
        elif posi[0] > 0:
            right_posi.append(posi)
        else:
            if i%2 == 0:
                left_posi.append(posi)
            else:
                right_posi.append(posi)
    up_r_posi_list.append(left_posi)
    up_l_posi_list.append(right_posi)

# for lower visual field; if x = 0; even index to lower-left visual field, odd index to lower-right visual field
for i, half_display in enumerate(low_posi_list):
    left_posi = []
    right_posi = []
    for posi in half_display:
        if posi[0] < 0:
            left_posi.append(posi)
        elif posi[0] > 0:
            right_posi.append(posi)
        else:
            if i%2 == 0:
                left_posi.append(posi)
            else:
                right_posi.append(posi)
    low_r_posi_list.append(left_posi)
    low_l_posi_list.append(right_posi)

#%% =============================================================================
# densities at different visual fields
# =============================================================================

def get_density(inputlist):
    '''calculate the density of 250 displays'''
    #get the aggregate surface
    aggregateSurface = []
    for display in inputlist:
        aggregateSurface_t = len(display)*pi*(0.25**2)
        aggregateSurface.append(aggregateSurface_t)
    #the density
    density = []
    for count, display in enumerate(inputlist):
        array = np.asarray(display)
        convexHullArea_t = ConvexHull(array).volume/(15.28**2)#caculate convexHull area- use .volume function
        density_t = round(aggregateSurface[count]/convexHullArea_t,5)
        density.append(density_t)
    return density

dnsty_up_posi_list    = []
dnsty_low_posi_list   = []
dnsty_up_r_posi_list  = []
dnsty_up_l_posi_list  = []
dnsty_low_r_posi_list = []
dnsty_low_l_posi_list = []

dnsty_up_posi_list    = get_density(up_posi_list)
dnsty_low_posi_list   = get_density(low_posi_list)
dnsty_up_r_posi_list  = get_density(up_r_posi_list)
dnsty_up_l_posi_list  = get_density(up_l_posi_list)
dnsty_low_r_posi_list = get_density(low_r_posi_list)
dnsty_low_l_posi_list = get_density(low_l_posi_list)

#%% =============================================================================
# update stimuli info
# =============================================================================
updated_stim_info_df['up_posi_list']          = up_posi_list
updated_stim_info_df['low_posi_list']         = low_posi_list
updated_stim_info_df['up_r_posi_list']        = up_r_posi_list
updated_stim_info_df['up_l_posi_list']        = up_l_posi_list
updated_stim_info_df['low_r_posi_list']       = low_r_posi_list
updated_stim_info_df['low_l_posi_list']       = low_l_posi_list

updated_stim_info_df['dnsty_up_posi_list']    = dnsty_up_posi_list
updated_stim_info_df['dnsty_low_posi_list']   = dnsty_low_posi_list
updated_stim_info_df['dnsty_up_r_posi_list']  = dnsty_up_r_posi_list
updated_stim_info_df['dnsty_up_l_posi_list']  = dnsty_up_l_posi_list
updated_stim_info_df['dnsty_low_r_posi_list'] = dnsty_low_r_posi_list
updated_stim_info_df['dnsty_low_l_posi_list'] = dnsty_low_l_posi_list

# =============================================================================
# get averaged quadrants density for each numerosity
# =============================================================================

df_c     = updated_stim_info_df[(updated_stim_info_df['crowdingcons'] == 1)]
df_nc    = updated_stim_info_df[(updated_stim_info_df['crowdingcons'] == 0)]

# https://www.cnblogs.com/huiyang865/p/5577772.html
# http://www.voidcn.com/article/p-slimdkya-bte.html

#for 5 crowding displays
df_c['density_low']  = df_c['dnsty_low_posi_list'].groupby   ([df_c['N_disk']]).transform('mean')
df_c['density_up']   = df_c['dnsty_up_posi_list'].groupby    ([df_c['N_disk']]).transform('mean')
df_c['density_Q1']   = df_c['dnsty_up_r_posi_list'].groupby  ([df_c['N_disk']]).transform('mean')
df_c['density_Q2']   = df_c['dnsty_up_l_posi_list'].groupby  ([df_c['N_disk']]).transform('mean')
df_c['density_Q3']   = df_c['dnsty_low_r_posi_list'].groupby ([df_c['N_disk']]).transform('mean')
df_c['density_Q4']   = df_c['dnsty_low_l_posi_list'].groupby ([df_c['N_disk']]).transform('mean')

#for 5 no-crowding displays
df_nc['density_low'] = df_nc['dnsty_low_posi_list'].groupby  ([df_nc['N_disk']]).transform('mean')
df_nc['density_up']  = df_nc['dnsty_up_posi_list'].groupby   ([df_nc['N_disk']]).transform('mean')
df_nc['density_Q1']  = df_nc['dnsty_up_r_posi_list'].groupby ([df_nc['N_disk']]).transform('mean')
df_nc['density_Q2']  = df_nc['dnsty_up_l_posi_list'].groupby ([df_nc['N_disk']]).transform('mean')
df_nc['density_Q3']  = df_nc['dnsty_low_r_posi_list'].groupby([df_nc['N_disk']]).transform('mean')
df_nc['density_Q4']  = df_nc['dnsty_low_l_posi_list'].groupby([df_nc['N_disk']]).transform('mean')

updated_stim_info_df = pd.concat([df_c, df_nc])
# updated_stim_info_df.to_excel('try1.xlsx')

#reshape stimuli info file by N_disk, crowdingcons and different densities
dfcopy  = updated_stim_info_df.copy()
# a=dfcopy.groupby(['N_disk','crowdingcons','density_low','density_up','density_Q1','density_Q2','density_Q3','density_Q4']).mean()
stimuliinfo_avrg_N = dfcopy.groupby(['crowdingcons', 'N_disk']).mean()
# stimuliinfo_avrg_N.to_excel('try2.xlsx')

#%% =============================================================================
# get data file and merge
# =============================================================================

#merge update_stim_info_df with totalData
totalData_new = pd.read_excel('../cleanedTotalData_fullinfo.xlsx')
to_drop = [ 'pk',
            'strictResponse',
            'expName',
            'handness',
            'stimuliPresentTime', 
            'positions', 
            'convexHull', 
            'averageE', 
            'avg_spacing', 
            'occupancyArea', 
            'aggregateSurface', 
            'density',
            'count_number1',
            'count_number2',
            'count_number3',
            'count_number4',
            'count_number5',
            'count_number6',
            'count_number7',
            'count_number8',
            'count_number9',
            'count_number10',
            'count_number11',
            'count_number12',
            'count_number13',
            'count_number14',
            'count_number15',
            'count_number16',
            'count_number17',
            'count_number18',
            'count_number19',
            'count_number20',
            'count_number21',
            'count_number22',
            'count_number23',
            'count_number24',
            'count_number25',
            'count_number26',
            'count_number27',
            'count_number28',
            'count_number29',
            'count_number30',
            'count_number']

totalData_new.drop(columns=to_drop, inplace = True)
# make sure the colums type are same for both files
totalData_new['crowdingcons']     = totalData_new['crowdingcons'].astype(int)
totalData_new['winsize']          = totalData_new['winsize'].astype(float)
totalData_new['index_stimuliInfo']= totalData_new['index_stimuliInfo'].astype(str)
totalData_new['N_disk']           = totalData_new['N_disk'].astype(int)

# updated_stim_info_df['crowdingcons']     = updated_stim_info_df['crowdingcons'].astype(int)
# updated_stim_info_df['winsize']          = updated_stim_info_df['winsize'].astype(float)
# updated_stim_info_df['index_stimuliInfo']= updated_stim_info_df['index_stimuliInfo'].astype(str)
# updated_stim_info_df['N_disk']           = updated_stim_info_df['N_disk'].astype(int)
# totalData_new.to_excel('try2.xlsx', sheet_name = 'Shee1')
#TODO: Check 2 df coloums that are to be merged
# for col in totalData_new.columns:
#     print(col)
# for col in updated_stim_info_df.columns:
#     print(col)
totalData_new_vfd = pd.merge(totalData_new,updated_stim_info_df, how = 'left', on = ['index_stimuliInfo', 'N_disk', 'crowdingcons','winsize'])
# totalData_new.to_excel('try3.xlsx')
# pp_data.drop_duplicates()

#%% =============================================================================
# deviation against local density (local density as a interpreter)
# =============================================================================
pivotT1 = pd.pivot_table(totalData_new_vfd,index = ['crowdingcons','participant_N',], columns = ['winsize','N_disk', 'density_low'],values = ['deviation_score'])
# pivotT1.to_excel('try4_1.xlsx')

# pivotT2 = pd.pivot_table(totalData_new,index = ['crowdingcons','participant_N',], columns = ['winsize','N_disk', 'local_density_at_minDiff', 'e_at_min_locDenDiff'],values = ['deviation_score'])
# # pivotT2.to_excel('try4_2.xlsx')






