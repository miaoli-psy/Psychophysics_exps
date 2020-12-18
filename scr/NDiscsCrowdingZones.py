# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:09:20 2020

@author: MiaoLi
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
#%% =============================================================================
# import clean data
# =============================================================================
totalData     = pd.read_excel('cleanedTotalData_fullinfo.xlsx')
totalData_c   = totalData[totalData.crowdingcons == 1]
totalData_nc  = totalData[totalData.crowdingcons == 0]
# for separate numerosity ranges
# crowding condition
data_N54_58_c  = totalData_c[totalData_c.winsize   == 0.7]
data_N49_53_c  = totalData_c[totalData_c.winsize   == 0.6]
data_N41_45_c  = totalData_c[totalData_c.winsize   == 0.5]
data_N31_35_c  = totalData_c[totalData_c.winsize   == 0.4]
data_N21_25_c  = totalData_c[totalData_c.winsize   == 0.3]

# no-crowding condition
data_N54_58_nc = totalData_nc[totalData_nc.winsize == 0.7]
data_N49_53_nc = totalData_nc[totalData_nc.winsize == 0.6]
data_N41_45_nc = totalData_nc[totalData_nc.winsize == 0.5]
data_N31_35_nc = totalData_nc[totalData_nc.winsize == 0.4]
data_N21_25_nc = totalData_nc[totalData_nc.winsize == 0.3]

#re-name N_disk to Numerosity
def renameC(df):
    df = df.rename(columns ={'N_disk':'Numerosity'}, inplace = True)
    return df
renameC(data_N54_58_c)
renameC(data_N49_53_c)
renameC(data_N41_45_c)
renameC(data_N31_35_c)
renameC(data_N21_25_c)
renameC(data_N21_25_nc)
renameC(data_N31_35_nc)
renameC(data_N41_45_nc)
renameC(data_N49_53_nc)
renameC(data_N54_58_nc)

# data_N54_58_c.to_excel('try.xlsx')
# deviiation score against number of discs into others crowding zones

#%% =============================================================================
# average per display (not per participant)
# =============================================================================
#for differnent windowsize
#crowding condition-to plot
winsize06 = data_N49_53_c['deviation_score'].groupby([data_N49_53_c['list_index'], data_N49_53_c['Numerosity'],data_N49_53_c['count_number']]).mean()
winsize06 = winsize06.reset_index(level=['count_number','Numerosity']) # convert index to coloum

winsize07 = data_N54_58_c['deviation_score'].groupby([data_N54_58_c['list_index'], data_N54_58_c['Numerosity'],data_N54_58_c['count_number']]).mean()
winsize07 = winsize07.reset_index(level=['count_number','Numerosity'])

winsize05 = data_N41_45_c['deviation_score'].groupby([data_N41_45_c['list_index'], data_N41_45_c['Numerosity'],data_N41_45_c['count_number']]).mean()
winsize05 = winsize05.reset_index(level=['count_number','Numerosity'])

winsize04 = data_N31_35_c['deviation_score'].groupby([data_N31_35_c['list_index'], data_N31_35_c['Numerosity'],data_N31_35_c['count_number']]).mean()
winsize04 = winsize04.reset_index(level=['count_number','Numerosity'])

winsize03 = data_N21_25_c['deviation_score'].groupby([data_N21_25_c['list_index'], data_N21_25_c['Numerosity'],data_N21_25_c['count_number']]).mean()
winsize03 = winsize03.reset_index(level=['count_number','Numerosity'])

#add color coloum
def add_color(row):
    if row['Numerosity'] == 21 or row['Numerosity'] == 31 or row['Numerosity'] == 41 or row['Numerosity'] == 49 or row['Numerosity'] == 54:
        return 'pink'
    if row['Numerosity'] == 22 or row['Numerosity'] == 32 or row['Numerosity'] == 42 or row['Numerosity'] == 50 or row['Numerosity'] == 55:
        return 'hotpink'
    if row['Numerosity'] == 23 or row['Numerosity'] == 33 or row['Numerosity'] == 43 or row['Numerosity'] == 51 or row['Numerosity'] == 56:
        return 'magenta'
    if row['Numerosity'] == 24 or row['Numerosity'] == 34 or row['Numerosity'] == 44 or row['Numerosity'] == 52 or row['Numerosity'] == 57:
        return 'mediumorchid'
    if row['Numerosity'] == 25 or row['Numerosity'] == 35 or row['Numerosity'] == 45 or row['Numerosity'] == 53 or row['Numerosity'] == 58:
        return 'blueviolet'

winsize07['color'] = winsize07.apply(lambda row: add_color(row), axis = 1)
winsize06['color'] = winsize06.apply(lambda row: add_color(row), axis = 1)
winsize05['color'] = winsize05.apply(lambda row: add_color(row), axis = 1)
winsize04['color'] = winsize04.apply(lambda row: add_color(row), axis = 1)
winsize03['color'] = winsize03.apply(lambda row: add_color(row), axis = 1)

#no-crowding condition-to calculate the average
winsize06nc = data_N49_53_nc['deviation_score'].groupby([data_N49_53_nc['list_index'], data_N49_53_nc['Numerosity'],data_N49_53_nc['count_number']]).mean()
winsize07nc = data_N54_58_nc['deviation_score'].groupby([data_N54_58_nc['list_index'], data_N54_58_nc['Numerosity'],data_N54_58_nc['count_number']]).mean()
winsize05nc = data_N41_45_nc['deviation_score'].groupby([data_N41_45_nc['list_index'], data_N41_45_nc['Numerosity'],data_N41_45_nc['count_number']]).mean()
winsize04nc = data_N31_35_nc['deviation_score'].groupby([data_N31_35_nc['list_index'], data_N31_35_nc['Numerosity'],data_N31_35_nc['count_number']]).mean()
winsize03nc = data_N21_25_nc['deviation_score'].groupby([data_N21_25_nc['list_index'], data_N21_25_nc['Numerosity'],data_N21_25_nc['count_number']]).mean()

nc07_mean = winsize07nc.mean()
nc06_mean = winsize06nc.mean()
nc05_mean = winsize05nc.mean()
nc04_mean = winsize04nc.mean()
nc03_mean = winsize03nc.mean()

#write to excel if necessary
writer = pd.ExcelWriter('nDiscsCrowdingzone_regdata.xlsx', engine = 'xlsxwriter')
winsize03.to_excel(writer, sheet_name = 'winsize03')
winsize04.to_excel(writer, sheet_name = 'winsize04')
winsize05.to_excel(writer, sheet_name = 'winsize05')
winsize05.to_excel(writer, sheet_name = 'winsize05')
winsize06.to_excel(writer, sheet_name = 'winsize06')
winsize07.to_excel(writer, sheet_name = 'winsize07')

#all datapoints together (statistically not meaningful)
# reg_data_all = pd.concat([winsize03,winsize04,winsize05, winsize06,winsize07])

#save it
# writer.save()
#%%=============================================================================
# calculate correlations
# =============================================================================
r07, p07 = stats.pearsonr(winsize07['deviation_score'], winsize07['count_number'])
r06, p06 = stats.pearsonr(winsize06['deviation_score'], winsize06['count_number'])
r05, p05 = stats.pearsonr(winsize05['deviation_score'], winsize05['count_number'])
r04, p04 = stats.pearsonr(winsize04['deviation_score'], winsize04['count_number'])
r03, p03 = stats.pearsonr(winsize03['deviation_score'], winsize03['count_number'])
#%%=============================================================================
# increase the size of crowding zones
# =============================================================================
def get_regData(countN):
    '''
    increase both major and minor axes:
    esize 110%: count_number1
    esize 120%: count_number2
    esize 130%: count_number3
    esize 140%: count_number4
    esize 150%: count_number5
    esize 160%: count_number6
    esize 170%: count_number7
    esize 180%: count_number8
    esize 190%: count_number9
    esize 200#: count_number10

    keep minor axis same:
    esize 110%: ncount_number1
    esize 120%: ncount_number2
    esize 130%: ncount_number3
    esize 140%: ncount_number4
    esize 150%: ncount_number5
    esize 160%: ncount_number6
    esize 170%: ncount_number7
    esize 180%: ncount_number8
    esize 190%: ncount_number9
    esize 200#: ncount_number10
    '''
    ws07 = data_N54_58_c['deviation_score'].groupby([data_N54_58_c['list_index'], data_N54_58_c['Numerosity'],data_N54_58_c[countN]]).mean()
    ws06 = data_N49_53_c['deviation_score'].groupby([data_N49_53_c['list_index'], data_N49_53_c['Numerosity'],data_N49_53_c[countN]]).mean()
    ws05 = data_N41_45_c['deviation_score'].groupby([data_N41_45_c['list_index'], data_N41_45_c['Numerosity'],data_N41_45_c[countN]]).mean()
    ws04 = data_N31_35_c['deviation_score'].groupby([data_N31_35_c['list_index'], data_N31_35_c['Numerosity'],data_N31_35_c[countN]]).mean()
    ws03 = data_N21_25_c['deviation_score'].groupby([data_N21_25_c['list_index'], data_N21_25_c['Numerosity'],data_N21_25_c[countN]]).mean()
    
    ws07 = ws07.reset_index(level = [countN])
    ws06 = ws06.reset_index(level = [countN])
    ws05 = ws05.reset_index(level = [countN])
    ws04 = ws04.reset_index(level = [countN])
    ws03 = ws03.reset_index(level = [countN])

    return ws03, ws04, ws05, ws06, ws07
#%%=============================================================================
# regplot plot - single winsize
# =============================================================================
ax_r = sns.regplot(x="count_number", y="deviation_score", data=winsize03, x_jitter=0.3)
ax_r.spines['top'].set_visible(False)
ax_r.spines['right'].set_visible(False)
# ax_r.set_xlabel('No. of discs in others crowding zones_ellipseSize%s' %(ellipseSize))
ax_r.set(ylim = (-2, 8))
# ax_r.set(xlim = (31, 55))
sns.set(rc={'figure.figsize':(6,3)})
#%% =============================================================================
# plot-all winsize in one figure-actual ellipse size
# =============================================================================
sns.set(style = 'white', color_codes = True)
sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
# sns.set_palette("pastel")
fig, axes = plt.subplots(2,3, figsize =(13,6),sharex = True, sharey = True)
# sns.despine() #remove top and left line

#regration - multi color
#sns.regplot(x="count_number", y="deviation_score", data=winsize03, x_jitter=0.5, ax=axes[0,0], scatter_kws={'facecolors':winsize03['color']}, color = 'black')
#sns.regplot(x="count_number", y="deviation_score", data=winsize04, x_jitter=0.5, ax=axes[0,1], scatter_kws={'facecolors':winsize04['color']}, color = 'black')
#sns.regplot(x="count_number", y="deviation_score", data=winsize05, x_jitter=0.5, ax=axes[0,2], scatter_kws={'facecolors':winsize05['color']}, color = 'black')
#sns.regplot(x="count_number", y="deviation_score", data=winsize06, x_jitter=0.5, ax=axes[1,0], scatter_kws={'facecolors':winsize06['color']}, color = 'black')
#sns.regplot(x="count_number", y="deviation_score", data=winsize07, x_jitter=0.5, ax=axes[1,1], scatter_kws={'facecolors':winsize07['color']}, color = 'black')

#regration - uni color
sns.regplot(x="count_number", y="deviation_score", data=winsize03, x_jitter=0.5, ax=axes[0,0])
sns.regplot(x="count_number", y="deviation_score", data=winsize04, x_jitter=0.5, ax=axes[0,1])
sns.regplot(x="count_number", y="deviation_score", data=winsize05, x_jitter=0.5, ax=axes[0,2])
sns.regplot(x="count_number", y="deviation_score", data=winsize06, x_jitter=0.5, ax=axes[1,0])
sns.regplot(x="count_number", y="deviation_score", data=winsize07, x_jitter=0.5, ax=axes[1,1])
#average for no-crowding condition
color = 'k'
axes[0,0].axhline(nc03_mean, ls='--',color = color)
axes[0,1].axhline(nc04_mean, ls='--',color = color)
axes[0,2].axhline(nc05_mean, ls='--',color = color)
axes[1,0].axhline(nc06_mean, ls='--',color = color)
axes[1,1].axhline(nc07_mean, ls='--',color = color)

#set x, y limits
axes[0,0].set_ylim(-2,7)
axes[0,1].set_ylim(-2,7)
axes[0,2].set_ylim(-2,7)
axes[1,0].set_ylim(-2,7)
axes[1,1].set_ylim(-2,7)

#set x ticks
axes[0,0].get_xaxis().set_ticks([0, 2, 4, 6, 8, 10, 12, 14, 16])

axes[0,0].set_xlim(-1,16)
axes[0,1].set_xlim(-1,16)
axes[0,2].set_xlim(-1,16)
axes[1,0].set_xlim(-1,16)
axes[1,1].set_xlim(-1,16)

#set x,y label
axes[0,0].set(xlabel='', ylabel='')
axes[0,1].set(xlabel='', ylabel='')
axes[0,2].set(xlabel='', ylabel='')
axes[1,0].set(xlabel='', ylabel='')
axes[1,1].set(xlabel='Number of discs falls into others\' crowding zones', ylabel = '')

# axes[0,1].yaxis.set_visible(False)
# axes[1,2].yaxis.set_visible(False)
# axes[1,1].yaxis.set_visible(False)
# axes[0,0].yaxis.set_visible(False)
# axes[1,0].yaxis.set_visible(False)

axes[1,1].xaxis.label.set_size(20)

# add necessary text 
fig.text(0.08, 0.5, 'Deviation Scores', va = 'center', rotation ='vertical', fontsize = 20)

# peasorn r
fig.text(0.28, 0.85, 'r = %s'%(round(r03,2)), va = 'center', fontsize = 15) #winsize03
fig.text(0.56, 0.85, 'r = %s'%(round(r04,2)), va = 'center', fontsize = 15) #winsize04
fig.text(0.83, 0.85, 'r = %s'%(round(r05,2)), va = 'center', fontsize = 15) #winsize05
fig.text(0.28, 0.43, 'r = %s'%(round(r06,2)), va = 'center', fontsize = 15) #winsize06
fig.text(0.56, 0.43, 'r = %s'%(round(r07,2)), va = 'center', fontsize = 15) #winsize07

fig.text(0.15, 0.89, '(a) numerosity range: 21-25', fontsize = 14)
fig.text(0.43, 0.89, '(b) numerosity range: 31-35', fontsize = 14)
fig.text(0.7, 0.89,  '(c) numerosity range: 41-45', fontsize = 14)
fig.text(0.15, 0.48, '(d) numerosity range: 49-53', fontsize = 14)
fig.text(0.43, 0.48, '(e) numerosity range: 54-58', fontsize = 14)

##add legend
#axes[1,2].plot([2.5],[5], 'o', color = 'pink',markeredgecolor = 'k')
#axes[1,2].plot([2.5],[4], 'o', color = 'hotpink',markeredgecolor = 'k')
#axes[1,2].plot([2.5],[3], 'o', color = 'magenta',markeredgecolor = 'k')
#axes[1,2].plot([2.5],[2], 'o', color = 'mediumorchid',markeredgecolor = 'k')
#axes[1,2].plot([2.5],[1], 'o', color = 'blueviolet',markeredgecolor = 'k')

#fig.text(0.73, 0.392, '21, 31, 41, 49, 54', va = 'center', fontsize = 12)
#fig.text(0.73, 0.354, '22, 32, 42, 50, 55', va = 'center', fontsize = 12)
#fig.text(0.73, 0.317, '23, 33, 43, 51, 56', va = 'center', fontsize = 12)
#fig.text(0.73, 0.278, '24, 34, 44, 52, 57', va = 'center', fontsize = 12)
#fig.text(0.73, 0.239, '25, 35, 45, 53, 58', va = 'center', fontsize = 12)

#remoing the borders and ticks of the last subplot
axes[1,2].spines['top'].set_visible(False)
axes[1,2].spines['left'].set_visible(False)
axes[1,2].spines['right'].set_visible(False)
axes[1,2].spines['bottom'].set_visible(False)
#removing the tick marks
axes[1,2].tick_params(bottom = False, left = False)

#removing the x label
axes[1,2].xaxis.set_visible(False)

# remove the empty subplot
# axes[1,2].set_visible(False)

plt.show()
plt.tight_layout()

#save the plot
fig.savefig("try1.svg", dpi = fig.dpi)

#%% =============================================================================
# plot-increase ellipse size
# =============================================================================
figb, axesb = plt.subplots(2,3, figsize =(13,6),sharex = True, sharey = True)
countnumber = ['count_number1',\
               'count_number2',\
               'count_number3',\
               'count_number4',\
               'count_number5',\
               'count_number6',\
               'count_number7',\
               'count_number8',\
               'count_number9',\
               'count_number10',\
               'ncount_number1',\
               'ncount_number2',\
               'ncount_number3',\
               'ncount_number4',\
               'ncount_number5',\
               'ncount_number6',\
               'ncount_number7',\
               'ncount_number8',\
               'ncount_number9',\
               'ncount_number10']
title = ['The size of crowding zones: major axis = 0.275e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.3e, minor axis = 0.12e',\
         'The size of crowding zones: major axis = 0.325e, minor axis = 0.13e',\
         'The size of crowding zones: major axis = 0.35e, minor axis = 0.14e',\
         'The size of crowding zones: major axis = 0.375e, minor axis = 0.15e',\
         'The size of crowding zones: major axis = 0.4e, minor axis = 0.16e',\
         'The size of crowding zones: major axis = 0.425e, minor axis = 0.17e',\
         'The size of crowding zones: major axis = 0.45e, minor axis = 0.18e',\
         'The size of crowding zones: major axis = 0.475e, minor axis = 0.19e',\
         'The size of crowding zones: major axis = 0.5e, minor axis = 0.2e',\
         'The size of crowding zones: major axis = 0.275e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.3e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.325e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.35e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.375e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.4e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.425e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.45e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.475e, minor axis = 0.11e',\
         'The size of crowding zones: major axis = 0.5e, minor axis = 0.11e']

#TODO
esize = 2

#choose from countnumber list: which ellipse size

regdata = get_regData(countnumber[esize])

#get x values
if esize < 10:
    if esize <5:
        x = list(regdata[esize].columns)[0]
    else:
        x = list(regdata[esize%5].columns)[0]
else:
    if esize < 15:
        x = list(regdata[esize-10].columns)[0]
    else:
        x = list(regdata[(esize-10)%5].columns)[0]


#person r
r03_a,p03_a = stats.pearsonr(regdata[0]['deviation_score'], regdata[0][x])
r04_a,p04_a = stats.pearsonr(regdata[1]['deviation_score'], regdata[1][x])
r05_a,p05_a = stats.pearsonr(regdata[2]['deviation_score'], regdata[2][x])
r06_a,p06_a = stats.pearsonr(regdata[3]['deviation_score'], regdata[3][x])
r07_a,p07_a = stats.pearsonr(regdata[4]['deviation_score'], regdata[4][x])

#store all rs and ps 
rs, ps = [], []
rs = [r03_a, r04_a, r05_a, r06_a, r07_a]
ps = [p03_a, p04_a, p05_a, p06_a, p07_a]

#regration
sns.regplot(x=x, y="deviation_score", data=regdata[0], x_jitter=0.5, ax=axesb[0,0], ci = 0)
sns.regplot(x=x, y="deviation_score", data=regdata[1], x_jitter=0.5, ax=axesb[0,1], ci = 0)
sns.regplot(x=x, y="deviation_score", data=regdata[2], x_jitter=0.5, ax=axesb[0,2], ci = 0)
sns.regplot(x=x, y="deviation_score", data=regdata[3], x_jitter=0.5, ax=axesb[1,0], ci = 0)
sns.regplot(x=x, y="deviation_score", data=regdata[4], x_jitter=0.5, ax=axesb[1,1], ci = 0)

#average for no-crowding condition
color = 'k'
axesb[0,0].axhline(nc03_mean, ls='--',color = color)
axesb[0,1].axhline(nc04_mean, ls='--',color = color)
axesb[0,2].axhline(nc05_mean, ls='--',color = color)
axesb[1,0].axhline(nc06_mean, ls='--',color = color)
axesb[1,1].axhline(nc07_mean, ls='--',color = color)

#set y limits
axesb[0,0].set_ylim(-2,7)
axesb[0,1].set_ylim(-2,7)
axesb[0,2].set_ylim(-2,7)
axesb[1,0].set_ylim(-2,7)
axesb[1,1].set_ylim(-2,7)

#set x,y label
axesb[0,0].set(xlabel='', ylabel='')
axesb[0,1].set(xlabel='', ylabel='')
axesb[0,2].set(xlabel='', ylabel='')
axesb[1,0].set(xlabel='', ylabel='')
axesb[1,1].set(xlabel='Number of discs falls into others\' crowding zones' , ylabel = '')
axesb[1,1].xaxis.label.set_size(20)

#set title
figb.text(0.19, 0.95, title[esize], fontsize = 20)

#add text
figb.text(0.15, 0.89, '(a) numerosity range: 21-25', fontsize = 14)
figb.text(0.43, 0.89, '(b) numerosity range: 31-35', fontsize = 14)
figb.text(0.7, 0.89,  '(c) numerosity range: 41-45', fontsize = 14)
figb.text(0.15, 0.48, '(d) numerosity range: 49-53', fontsize = 14)
figb.text(0.43, 0.48, '(e) numerosity range: 54-58', fontsize = 14)
figb.text(0.08, 0.5, 'Deviation', va = 'center', rotation ='vertical', fontsize = 20)

# peasorn r
figb.text(0.28, 0.85, 'r = %s'%(round(r03_a,2)), va = 'center', fontsize = 15) #winsize03
figb.text(0.56, 0.85, 'r = %s'%(round(r04_a,2)), va = 'center', fontsize = 15) #winsize04
figb.text(0.83, 0.85, 'r = %s'%(round(r05_a,2)), va = 'center', fontsize = 15) #winsize05
figb.text(0.28, 0.43, 'r = %s'%(round(r06_a,2)), va = 'center', fontsize = 15) #winsize06
figb.text(0.56, 0.43, 'r = %s'%(round(r07_a,2)), va = 'center', fontsize = 15) #winsize07
# remove the empty subplot
axesb[1,2].set_visible(False)
plt.show()

# figb.savefig("Fig_%s.png" %(esize), edgecolor = 'k', dpi = fig.dpi)
#%% =============================================================================
# rs for all size of ellipses
# =============================================================================
esizes = [i for i in range(10)]


r_03s, r_04s, r_05s, r_06s, r_07s = [], [], [] ,[] ,[]
p_03s, p_04s, p_05s, p_06s, p_07s = [], [], [] ,[] ,[]

for e in esizes:
    #choose from countnumber list: which ellipse size
    regdata = get_regData(countnumber[e])
    
    #get x values
    if e < 10:
        if e <5:
            x = list(regdata[e].columns)[0]
        else:
            x = list(regdata[e%5].columns)[0]
    else:
        if e < 15:
            x = list(regdata[e-10].columns)[0]
        else:
            x = list(regdata[(e-10)%5].columns)[0]
    #person r
    r03_a,p03_a = stats.pearsonr(regdata[0]['deviation_score'], regdata[0][x])
    r04_a,p04_a = stats.pearsonr(regdata[1]['deviation_score'], regdata[1][x])
    r05_a,p05_a = stats.pearsonr(regdata[2]['deviation_score'], regdata[2][x])
    r06_a,p06_a = stats.pearsonr(regdata[3]['deviation_score'], regdata[3][x])
    r07_a,p07_a = stats.pearsonr(regdata[4]['deviation_score'], regdata[4][x])
    
    r_03s.append(r03_a)
    r_04s.append(r04_a)
    r_05s.append(r05_a)
    r_06s.append(r06_a)
    r_07s.append(r07_a)
    
    p_03s.append(p03_a)
    p_04s.append(p04_a)
    p_05s.append(p05_a)
    p_06s.append(p06_a)
    p_07s.append(p07_a)
    
y = [1.1, 1.2, 1.3, 1.4,1.5,1.6,1.7,1.8,1.9,2.0]
#rs_df = pd.DataFrame(r_03s, r_04s,r_05s,r_06s,r_07s, p_03s, p_04s,p_05s,p_06s,p_07s, y)
rs_df = pd.DataFrame(list(zip(r_03s, r_04s,r_05s,r_06s,r_07s, p_03s, p_04s,p_05s,p_06s,p_07s, y)),
                     columns = ['r_03s', 'r_04s','r_05s','r_06s','r_07s', 'p_03s', 'p_04s','p_05s','p_06s','p_07s', 'size'])

figc, axesc = plt.subplots(2,3, figsize =(13,6),sharex = True, sharey = True)
sns.regplot(x= "size", y = "r_03s", data = rs_df, ax=axesc[0,0], ci = 0)
sns.regplot(x= "size", y = "r_04s", data = rs_df, ax=axesc[0,1], ci = 0)
sns.regplot(x= "size", y = "r_05s", data = rs_df, ax=axesc[0,2], ci = 0)
sns.regplot(x= "size", y = "r_06s", data = rs_df, ax=axesc[1,0], ci = 0)
sns.regplot(x= "size", y = "r_07s", data = rs_df, ax=axesc[1,1], ci = 0)


#set y limits
axesc[0,0].set_ylim(-0.6,0.2)
axesc[0,1].set_ylim(-0.6,0.2)
axesc[0,2].set_ylim(--0.6,0.2)
axesc[1,0].set_ylim(-0.6,0.2)
axesc[1,1].set_ylim(-0.6,0.2)

#set x,y label
axesc[0,0].set(xlabel='', ylabel='')
axesc[0,1].set(xlabel='', ylabel='')
axesc[0,2].set(xlabel='', ylabel='')
axesc[1,0].set(xlabel='', ylabel='')
axesc[1,1].set(xlabel='Ellipse Size' , ylabel = '')
axesc[1,1].xaxis.label.set_size(20)

#set title
#figc.text(0.19, 0.95,"Correlations against ellipse size", fontsize = 20)

#set x ticks
axesc[0,0].get_xaxis().set_ticks([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])

axesc[0,0].set_xlim(1,2.02)
axesc[0,1].set_xlim(1,2.02)
axesc[0,2].set_xlim(1,2.02)
axesc[1,0].set_xlim(1,2.02)
axesc[1,1].set_xlim(1,2.02)

#add normal size R
color = 'k'
axesc[0,0].axhline(r03, ls='--',color = color)
axesc[0,1].axhline(r04, ls='--',color = color)
axesc[0,2].axhline(r05, ls='--',color = color)
axesc[1,0].axhline(r06, ls='--',color = color)
axesc[1,1].axhline(r07, ls='--',color = color)
# add necessary text 
figc.text(0.06, 0.5, 'Correlation Coefficient', va = 'center', rotation ='vertical', fontsize = 20)


figc.text(0.15, 0.89, '(a) numerosity range: 21-25', fontsize = 14)
figc.text(0.43, 0.89, '(b) numerosity range: 31-35', fontsize = 14)
figc.text(0.7, 0.89,  '(c) numerosity range: 41-45', fontsize = 14)
figc.text(0.15, 0.48, '(d) numerosity range: 49-53', fontsize = 14)
figc.text(0.43, 0.48, '(e) numerosity range: 54-58', fontsize = 14)


#removing the tick marks
axesc[1,2].tick_params(bottom = False, left = False)

#removing the x label
axesc[1,2].xaxis.set_visible(False)

# remove the empty subplot
axesc[1,2].set_visible(False)

plt.show()
plt.tight_layout()

#save the plot
figc.savefig("try1.svg", dpi = fig.dpi)

#%% =============================================================================
# scatter plot
# =============================================================================
winsize07_scat = data_N54_58_c['deviation_score'].groupby([data_N54_58_c['list_index'], data_N54_58_c['Numerosity'],data_N54_58_c['count_number'],data_N54_58_c['participant_N']]).mean()
winsize06_scat = data_N49_53_c['deviation_score'].groupby([data_N49_53_c['list_index'], data_N49_53_c['Numerosity'],data_N49_53_c['count_number'],data_N49_53_c['participant_N']]).mean()
winsize05_scat = data_N41_45_c['deviation_score'].groupby([data_N41_45_c['list_index'], data_N41_45_c['Numerosity'],data_N41_45_c['count_number'],data_N41_45_c['participant_N']]).mean()
winsize04_scat = data_N31_35_c['deviation_score'].groupby([data_N31_35_c['list_index'], data_N31_35_c['Numerosity'],data_N31_35_c['count_number'],data_N31_35_c['participant_N']]).mean()
winsize03_scat = data_N21_25_c['deviation_score'].groupby([data_N21_25_c['list_index'], data_N21_25_c['Numerosity'],data_N21_25_c['count_number'],data_N21_25_c['participant_N']]).mean()

winsize07_scat = winsize07_scat.reset_index(level=['count_number','Numerosity'])
winsize06_scat = winsize06_scat.reset_index(level=['count_number','Numerosity'])
winsize05_scat = winsize05_scat.reset_index(level=['count_number','Numerosity'])
winsize04_scat = winsize04_scat.reset_index(level=['count_number','Numerosity'])
winsize03_scat = winsize03_scat.reset_index(level=['count_number','Numerosity'])
#set style
sns.set(style = 'white', color_codes = True)
sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})

winsize = 0.3
# winsize = 0.4
# winsize = 0.5
# winsize = 0.6
# winsize = 0.7

if winsize == 0.3:
    data = winsize03_scat
    title = 'Numerosity range: 21-25'
    name = '21_25'
if winsize ==0.4:
    data = winsize04_scat
    title = 'Numerosity range 31-35'
    name = '31_35'
if winsize ==0.5:
    data = winsize05_scat
    title = 'Numerosity range 41-45'
    name = '41_45'
if winsize ==0.6:
    data = winsize06_scat
    title = 'Numerosity range 49-53'
    name = '49_53'
if winsize ==0.7:
    data = winsize07_scat
    title = 'Numerosity range 54-58'
    name = '54_58'
g = sns.scatterplot(x = 'count_number', y = 'deviation_score',data = data, hue = 'Numerosity',alpha=0.5, legend = 'full')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
g.set_xlim(-1,16)
g.set_ylim(-20,25)
g.set_xlabel('Number of discs falls into others\' crowding zones', fontsize = 18)
g.set_ylabel('Deviation', fontsize = 18)
g.set_title(title, fontsize =18)
# g.set_title('Numerosity range: 31-35')
# g.set_title('Numerosity range: 41-45')
# g.set_title('Numerosity range: 49-53')
# g.set_title('Numerosity range: 54-58')
#figure size
sns.set(rc={'figure.figsize':(6,3)})
plt.savefig('scatter%s.png'%(name),bbox_inches='tight')
#%% =============================================================================
# SEM
# =============================================================================
import math
a_54 = winsize07_scat.iloc[winsize07_scat.index.get_level_values('list_index')==0]
a_54 = a_54[a_54.Numerosity == 54]
SEM =a_54.loc[:,"deviation_score"].std()/math.sqrt(20)