# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 19:43:56 2019

@author: MiaoLi
"""

#%%
import sys, os
import pandas as pd
# import seaborn as sns
# from shapely.geometry import Polygon, Point
sys.path.append('C:\\Users\\MiaoLi\\Desktop\\SCALab\\Programming\\crowdingnumerositygit\\GenerationAlgorithm\\VirtualEllipseFunc')
# import m_defineEllipses
import seaborn as sns
import matplotlib.pyplot as plt
# import scipy.stats
# import numpy as np
from sklearn import linear_model
from scipy import stats
#%%
# =============================================================================
# read differet sheets of the same excel file
# =============================================================================
# winsize0.6 crowding
totalC_N49_53            = pd.ExcelFile('../totalC_N49_53_scaterdata.xlsx')
totalC_N49_53_actualSize = pd.read_excel(totalC_N49_53, 'actualSize0.25_0.1')
totalC_N49_53_110        = pd.read_excel(totalC_N49_53, '110%0.275_0.11')
totalC_N49_53_120        = pd.read_excel(totalC_N49_53, '120%0.3_0.12')
totalC_N49_53_130        = pd.read_excel(totalC_N49_53, '130%0.325_0.13')
totalC_N49_53_140        = pd.read_excel(totalC_N49_53, '140%')
totalC_N49_53_150        = pd.read_excel(totalC_N49_53, '150%')
totalC_N49_53_160        = pd.read_excel(totalC_N49_53, '160%')
totalC_N49_53_170        = pd.read_excel(totalC_N49_53, '170%')
totalC_N49_53_180        = pd.read_excel(totalC_N49_53, '180%')
totalC_N49_53_190        = pd.read_excel(totalC_N49_53, '190%')
totalC_N49_53_200        = pd.read_excel(totalC_N49_53, '200%')
totalC_N49_53_210        = pd.read_excel(totalC_N49_53, '210%')
totalC_N49_53_220        = pd.read_excel(totalC_N49_53, '220%')
totalC_N49_53_230        = pd.read_excel(totalC_N49_53, '230%')
totalC_N49_53_240        = pd.read_excel(totalC_N49_53, '240%')
totalC_N49_53_250        = pd.read_excel(totalC_N49_53, '250%')
totalC_N49_53_260        = pd.read_excel(totalC_N49_53, '260%')
totalC_N49_53_270        = pd.read_excel(totalC_N49_53, '270%')
totalC_N49_53_280        = pd.read_excel(totalC_N49_53, '280%')
totalC_N49_53_290        = pd.read_excel(totalC_N49_53, '290%')
totalC_N49_53_300        = pd.read_excel(totalC_N49_53, '300%')
totalC_N49_53_310        = pd.read_excel(totalC_N49_53, '310%')
totalC_N49_53_320        = pd.read_excel(totalC_N49_53, '320%')
totalC_N49_53_330        = pd.read_excel(totalC_N49_53, '330%')
totalC_N49_53_340        = pd.read_excel(totalC_N49_53, '340%')
totalC_N49_53_350        = pd.read_excel(totalC_N49_53, '350%')
totalC_N49_53_360        = pd.read_excel(totalC_N49_53, '360%')
totalC_N49_53_370        = pd.read_excel(totalC_N49_53, '370%')
totalC_N49_53_380        = pd.read_excel(totalC_N49_53, '380%')
totalC_N49_53_390        = pd.read_excel(totalC_N49_53, '390%')
totalC_N49_53_400        = pd.read_excel(totalC_N49_53, '400%')


# winsize0.6 no-crowding
totalNC_N49_53            = pd.ExcelFile('../totalNC_N49_53_scaterdata.xlsx')
totalNC_N49_53_actualSize = pd.read_excel(totalNC_N49_53, 'actualSize')
totalNC_N49_53_110        = pd.read_excel(totalNC_N49_53, '110%')
totalNC_N49_53_120        = pd.read_excel(totalNC_N49_53, '120%')
totalNC_N49_53_130        = pd.read_excel(totalNC_N49_53, '130%')
totalNC_N49_53_140        = pd.read_excel(totalNC_N49_53, '140%')
totalNC_N49_53_150        = pd.read_excel(totalNC_N49_53, '150%')
totalNC_N49_53_160        = pd.read_excel(totalNC_N49_53, '160%')
totalNC_N49_53_170        = pd.read_excel(totalNC_N49_53, '170%')
totalNC_N49_53_180        = pd.read_excel(totalNC_N49_53, '180%')
totalNC_N49_53_190        = pd.read_excel(totalNC_N49_53, '190%')
totalNC_N49_53_200        = pd.read_excel(totalNC_N49_53, '200%')
totalNC_N49_53_210        = pd.read_excel(totalNC_N49_53, '210%')
totalNC_N49_53_220        = pd.read_excel(totalNC_N49_53, '220%')
totalNC_N49_53_230        = pd.read_excel(totalNC_N49_53, '230%')
totalNC_N49_53_240        = pd.read_excel(totalNC_N49_53, '240%')
totalNC_N49_53_250        = pd.read_excel(totalNC_N49_53, '250%')
totalNC_N49_53_260        = pd.read_excel(totalNC_N49_53, '260%')
totalNC_N49_53_270        = pd.read_excel(totalNC_N49_53, '270%')
totalNC_N49_53_280        = pd.read_excel(totalNC_N49_53, '280%')
totalNC_N49_53_290        = pd.read_excel(totalNC_N49_53, '290%')
totalNC_N49_53_300        = pd.read_excel(totalNC_N49_53, '300%')
totalNC_N49_53_310        = pd.read_excel(totalNC_N49_53, '310%')
totalNC_N49_53_320        = pd.read_excel(totalNC_N49_53, '320%')
totalNC_N49_53_330        = pd.read_excel(totalNC_N49_53, '330%')
totalNC_N49_53_340        = pd.read_excel(totalNC_N49_53, '340%')
totalNC_N49_53_350        = pd.read_excel(totalNC_N49_53, '350%')
totalNC_N49_53_360        = pd.read_excel(totalNC_N49_53, '360%')
totalNC_N49_53_370        = pd.read_excel(totalNC_N49_53, '370%')
totalNC_N49_53_380        = pd.read_excel(totalNC_N49_53, '380%')
totalNC_N49_53_390        = pd.read_excel(totalNC_N49_53, '390%')
totalNC_N49_53_400        = pd.read_excel(totalNC_N49_53, '400%')

# winsize0.7
totalC_N54_58            = pd.ExcelFile ('../totalC_N54_58_scaterdata.xlsx')
totalC_N54_58_actualSize = pd.read_excel(totalC_N54_58, 'actualSize')
totalC_N54_58_110        = pd.read_excel(totalC_N54_58, '110%')
totalC_N54_58_120        = pd.read_excel(totalC_N54_58, '120%')
totalC_N54_58_130        = pd.read_excel(totalC_N54_58, '130%')
totalC_N54_58_140        = pd.read_excel(totalC_N54_58, '140%')
totalC_N54_58_150        = pd.read_excel(totalC_N54_58, '150%')
totalC_N54_58_160        = pd.read_excel(totalC_N54_58, '160%')
totalC_N54_58_170        = pd.read_excel(totalC_N54_58, '170%')
totalC_N54_58_180        = pd.read_excel(totalC_N54_58, '180%')
totalC_N54_58_190        = pd.read_excel(totalC_N54_58, '190%')
totalC_N54_58_200        = pd.read_excel(totalC_N54_58, '200%')

# winsize0.7 no-crowding
totalNC_N54_58            = pd.ExcelFile('../totalNC_N54_58_scaterdata.xlsx')
totalNC_N54_58_actualSize = pd.read_excel(totalNC_N54_58, 'actualSize')
totalNC_N54_58_110        = pd.read_excel(totalNC_N54_58, '110%')
totalNC_N54_58_120        = pd.read_excel(totalNC_N54_58, '120%')
totalNC_N54_58_130        = pd.read_excel(totalNC_N54_58, '130%')
totalNC_N54_58_140        = pd.read_excel(totalNC_N54_58, '140%')
totalNC_N54_58_150        = pd.read_excel(totalNC_N54_58, '150%')
totalNC_N54_58_160        = pd.read_excel(totalNC_N54_58, '160%')
totalNC_N54_58_170        = pd.read_excel(totalNC_N54_58, '170%')
totalNC_N54_58_180        = pd.read_excel(totalNC_N54_58, '180%')
totalNC_N54_58_190        = pd.read_excel(totalNC_N54_58, '190%')
totalNC_N54_58_200        = pd.read_excel(totalNC_N54_58, '200%')
# =============================================================================
# Scatter plots
# =============================================================================
ellipseSize = '200'
ax = sns.stripplot(x='count_number10',y = 'deviation_score', data = totalC_N49_53_200, size = 8, jitter = 0.3, 
                    alpha = 0.3, color = 'k', edgecolor = 'gray')
# ax.set(xscale = 'log', yscale = 'log')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# add corrosponing no-crowding average line
# ax.axhline(3.26, ls='--', color = 'lime',linewidth=5)
ax.set_xlabel('No. of discs in others crowding zones_ellipseSize%s' %(ellipseSize))
# ax.set_ylabel('')

# ax.set(xlim = (0, 16))
ax.set(ylim = (-20, 25))
sns.set(rc={'figure.figsize':(6,3)})
plt.savefig('../scaterplot06_c_%s.png' %(ellipseSize), dpi=200,bbox_inches = 'tight',pad_inches = 0)

#
# # myx = scaterP_07_data['Count_number'].to_numpy()

# # slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x=scaterP_07_data['Count_number'][mask],y = scaterP_07_data['Deviation'][mask])
# reg  = linear_model.LinearRegression()
# x = scaterP_07_data['Count_number'].values.reshape(-1,1)
# y = scaterP_07_data['Deviation'].values.reshape(-1,1)
# reg.fit(x,y)
# r = reg.coef_
# intercept = reg.intercept_

#%% =============================================================================
# regplot
# =============================================================================

ax_r = sns.regplot(x="count_number10", y="deviation_score", data=totalC_N49_53_200, x_jitter=0.5)
ax_r.spines['top'].set_visible(False)
ax_r.spines['right'].set_visible(False)
ax_r.set_xlabel('No. of discs in others crowding zones_ellipseSize%s' %(ellipseSize))
ax_r.set(ylim = (-20, 25))
# ax_r.set(xlim = (31, 55))
sns.set(rc={'figure.figsize':(6,3)})
# plt.savefig('../scaterplot06_c_%s.png' %(ellipseSize), dpi=200,bbox_inches = 'tight',pad_inches = 0)



#%%
# scaterP_06_data = pd.read_excel('scaterplot_raw06.xlsx')

# bx = sns.stripplot(x='Count_number',y = 'Deviation', data = scaterP_06_data, color = 'k', size = 8, jitter = 0.3, 
#                     alpha = 0.3,edgecolor = 'gray')
# # bx = sns.regplot(x="Count_number", y="Deviation", data=scaterP_06_data, x_jitter = 0.3, color = 'k', y_jitter = 0.05)
# bx.spines['top'].set_visible(False)
# bx.spines['right'].set_visible(False)
# bx.axhline(3.902947846, ls ='--', color = 'lime', linewidth=5)
# bx.set_xlabel('')
# bx.set_ylabel('')
# # bx.set(xlim = (0, 16), xticks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14])
# bx.set(ylim = (-25, 25))

# plt.savefig('scaterplot06_1.png', dpi=200,bbox_inches = 'tight',pad_inches = 0)

#%%
# scaterP_both_data = pd.read_excel('scaterboth_raw.xlsx')

# ax = sns.stripplot(x='Count_number',y = 'Deviation', data = scaterP_both_data, size = 8, jitter = 0.3, 
#                     alpha = 0.2, color = 'k', edgecolor = 'gray')
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# ax.set_xlabel('')
# ax.set_ylabel('')
# # ax.set(xlim = (0, 16), xticks = [1, 3, 6, 7, 8, 9, 11, 15])
# ax.set(ylim = (-25,25))

# plt.savefig('scaterplotboth.png', dpi=200,bbox_inches = 'tight',pad_inches = 0)