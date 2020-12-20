 # -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 23:20:33 2019

@author: MiaoLi
"""
#%%
import os, sys
import pandas as pd
import ast
# import seaborn as sns
from collections import OrderedDict
from shapely.geometry import Polygon, Point
sys.path.append('C:\\Users\\MiaoLi\\Desktop\\SCALab\\Programming\\crowdingnumerositygit\\GenerationAlgorithm\\VirtualEllipseFunc')
import m_defineEllipses
# import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math
# import xlsxwriter

#%%=============================================================================
# list my raw data files
# =============================================================================
#parent directory
path = os.path.abspath(os.path.dirname(os.getcwd()))
files = os.listdir(path)
data_csv = [file for file in files if file.startswith('alternative') & file.endswith('csv')]

#%%=============================================================================
# import stimuli display
# =============================================================================
stimuliFile = '../Idea1_DESCO.xlsx'
stimuliInfo = pd.read_excel(stimuliFile)
posi_lists_temp = stimuliInfo['positions'].tolist()

posi_list=[]
for i in posi_lists_temp:
    i = ast.literal_eval(i)# megic! remore ' ' of the str
    posi_list.append(i)

#%%============================================================================
# inspect disks fall into others crowding zones
# =============================================================================

dic_count_in_crowdingZone = {}
list_count_in_crowdingZone = []
for indexPosiList in range(0,len(posi_list)):
    display_posi = posi_list[indexPosiList]
    #final ellipses
    ellipses = []
    for posi in display_posi:
        e = m_defineEllipses.defineVirtualEllipses(posi, 0.25, 0.1)
        ellipses.append(e)
    # final_ellipses = list(set(ellipses)) #if order doest matter
    final_ellipses = list(OrderedDict.fromkeys(ellipses)) #ordermatters
    count_in_crowdingZone = 0
        #crowding zones after reomve overlapping areas
    for count, i in enumerate(final_ellipses, start = 1):
        ellipsePolygon = m_defineEllipses.ellipseToPolygon([i])[0] #radial ellipse
        # ellipsePolygonT = ellipseToPolygon([i])[1]#tangential ellipse
        epPolygon = Polygon(ellipsePolygon)
        # epPolygonT = Polygon(ellipsePolygonT)
        # radial_area_dic[(i[0],i[1])] = [] #set the keys of the dictionary--taken_posi
        for posi in display_posi:
            if epPolygon.contains(Point(posi)) == True:
                count_in_crowdingZone += 1
    count_number_end = count_in_crowdingZone-len(display_posi)
    dic_temp_item = {indexPosiList: count_number_end}
    dic_count_in_crowdingZone.update(dic_temp_item)
    list_count_in_crowdingZone.append(count_number_end)
    
stimuliInfo.insert(1, 'count_number',list_count_in_crowdingZone)
# stimuliInfo.to_excel('count_number.xlsx')

#%% =============================================================================
# count_number: increasing ellipse sizes
# =============================================================================
# for i in range(5):
#     name='to_plot_nc'+str(i)
#     locals()['to_plot_nc'+str(i)]=i

for i in range(1,31):
    locals()['list_count_in_crowdingZone'+str(i)] = []

# list_count_in_crowdingZone1, \
# list_count_in_crowdingZone2, \
# list_count_in_crowdingZone3, \
# list_count_in_crowdingZone4, \
# list_count_in_crowdingZone5, \
# list_count_in_crowdingZone6, \
# list_count_in_crowdingZone7, \
# list_count_in_crowdingZone8, \
# list_count_in_crowdingZone9, \
# list_count_in_crowdingZone10, \
# list_count_in_crowdingZone11, \
# list_count_in_crowdingZone12, \
# list_count_in_crowdingZone13, \
# list_count_in_crowdingZone14, \
# list_count_in_crowdingZone15, \
# list_count_in_crowdingZone16, \
# list_count_in_crowdingZone17, \
# list_count_in_crowdingZone18, \
# list_count_in_crowdingZone19, \
# list_count_in_crowdingZone20, \
# list_count_in_crowdingZone21, \
# list_count_in_crowdingZone22, \
# list_count_in_crowdingZone23, \
# list_count_in_crowdingZone24, \
# list_count_in_crowdingZone25, \
# list_count_in_crowdingZone26, \
# list_count_in_crowdingZone27, \
# list_count_in_crowdingZone28, \
# list_count_in_crowdingZone29, \
# list_count_in_crowdingZone30 = ([] for i in range(30))

for indexPosiList, display_posi in enumerate(posi_list):
    ellipse_110, ellipse_120, ellipse_130, ellipse_140, ellipse_150, \
    ellipse_160, ellipse_170, ellipse_180, ellipse_190, ellipse_200, \
    ellipse_210, ellipse_220, ellipse_230, ellipse_240, ellipse_250, \
    ellipse_260, ellipse_270, ellipse_280, ellipse_290, ellipse_300, \
    ellipse_310, ellipse_320, ellipse_330, ellipse_340, ellipse_350, \
    ellipse_360, ellipse_370, ellipse_380, ellipse_390, ellipse_400 = ([] for i in range(30))
    for posi in display_posi:
        e1 = m_defineEllipses.defineVirtualEllipses(posi, 0.275, 0.11)
        e2 = m_defineEllipses.defineVirtualEllipses(posi, 0.3, 0.12)
        e3 = m_defineEllipses.defineVirtualEllipses(posi, 0.325, 0.13)
        e4 = m_defineEllipses.defineVirtualEllipses(posi, 0.35, 0.14)
        e5 = m_defineEllipses.defineVirtualEllipses(posi, 0.375, 0.15)
        e6 = m_defineEllipses.defineVirtualEllipses(posi, 0.4, 0.16)
        e7 = m_defineEllipses.defineVirtualEllipses(posi, 0.425, 0.17)
        e8 = m_defineEllipses.defineVirtualEllipses(posi, 0.45, 0.18)
        e9 = m_defineEllipses.defineVirtualEllipses(posi, 0.475, 0.19)
        e10 = m_defineEllipses.defineVirtualEllipses(posi, 0.5, 0.20)
        e11 = m_defineEllipses.defineVirtualEllipses(posi, 0.525, 0.21)
        e12 = m_defineEllipses.defineVirtualEllipses(posi, 0.55, 0.22)
        e13 = m_defineEllipses.defineVirtualEllipses(posi, 0.575, 0.23)
        e14 = m_defineEllipses.defineVirtualEllipses(posi, 0.6, 0.24)
        e15 = m_defineEllipses.defineVirtualEllipses(posi, 0.625, 0.25)
        e16 = m_defineEllipses.defineVirtualEllipses(posi, 0.65, 0.26)
        e17 = m_defineEllipses.defineVirtualEllipses(posi, 0.675, 0.27)
        e18 = m_defineEllipses.defineVirtualEllipses(posi, 0.7, 0.28)
        e19 = m_defineEllipses.defineVirtualEllipses(posi, 0.725, 0.29)
        e20 = m_defineEllipses.defineVirtualEllipses(posi, 0.75, 0.30)
        e21 = m_defineEllipses.defineVirtualEllipses(posi, 0.775, 0.31)
        e22 = m_defineEllipses.defineVirtualEllipses(posi, 0.8, 0.32)
        e23 = m_defineEllipses.defineVirtualEllipses(posi, 0.825, 0.33)
        e24 = m_defineEllipses.defineVirtualEllipses(posi, 0.85, 0.34)
        e25 = m_defineEllipses.defineVirtualEllipses(posi, 0.875, 0.35)
        e26 = m_defineEllipses.defineVirtualEllipses(posi, 0.9, 0.36)
        e27 = m_defineEllipses.defineVirtualEllipses(posi, 0.925, 0.37)
        e28 = m_defineEllipses.defineVirtualEllipses(posi, 0.95, 0.38)
        e29 = m_defineEllipses.defineVirtualEllipses(posi, 0.975, 0.39)
        e30 = m_defineEllipses.defineVirtualEllipses(posi, 1, 0.40)
        
        ellipse_110.append(e1)
        ellipse_120.append(e2)
        ellipse_130.append(e3)
        ellipse_140.append(e4)
        ellipse_150.append(e5)
        ellipse_160.append(e6)
        ellipse_170.append(e7)
        ellipse_180.append(e8)
        ellipse_190.append(e9)
        ellipse_200.append(e10)
        ellipse_210.append(e11)
        ellipse_220.append(e12)
        ellipse_230.append(e13)
        ellipse_240.append(e14)
        ellipse_250.append(e15)
        ellipse_260.append(e16)
        ellipse_270.append(e17)
        ellipse_280.append(e18)
        ellipse_290.append(e19)
        ellipse_300.append(e20)
        ellipse_310.append(e21)
        ellipse_320.append(e22)
        ellipse_330.append(e23)
        ellipse_340.append(e24)
        ellipse_350.append(e25)
        ellipse_360.append(e26)
        ellipse_370.append(e27)
        ellipse_380.append(e28)
        ellipse_390.append(e29)
        ellipse_400.append(e30)
    final_ellipses_110 = list(OrderedDict.fromkeys(ellipse_110))
    final_ellipses_120 = list(OrderedDict.fromkeys(ellipse_120))
    final_ellipses_130 = list(OrderedDict.fromkeys(ellipse_130))
    final_ellipses_140 = list(OrderedDict.fromkeys(ellipse_140))
    final_ellipses_150 = list(OrderedDict.fromkeys(ellipse_150))
    final_ellipses_160 = list(OrderedDict.fromkeys(ellipse_160))
    final_ellipses_170 = list(OrderedDict.fromkeys(ellipse_170))
    final_ellipses_180 = list(OrderedDict.fromkeys(ellipse_180))
    final_ellipses_190 = list(OrderedDict.fromkeys(ellipse_190))
    final_ellipses_200 = list(OrderedDict.fromkeys(ellipse_200))
    final_ellipses_210 = list(OrderedDict.fromkeys(ellipse_210))
    final_ellipses_220 = list(OrderedDict.fromkeys(ellipse_220))
    final_ellipses_230 = list(OrderedDict.fromkeys(ellipse_230))
    final_ellipses_240 = list(OrderedDict.fromkeys(ellipse_240))
    final_ellipses_250 = list(OrderedDict.fromkeys(ellipse_250))
    final_ellipses_260 = list(OrderedDict.fromkeys(ellipse_260))
    final_ellipses_270 = list(OrderedDict.fromkeys(ellipse_270))
    final_ellipses_280 = list(OrderedDict.fromkeys(ellipse_280))
    final_ellipses_290 = list(OrderedDict.fromkeys(ellipse_290))
    final_ellipses_300 = list(OrderedDict.fromkeys(ellipse_300))
    final_ellipses_310 = list(OrderedDict.fromkeys(ellipse_310))
    final_ellipses_320 = list(OrderedDict.fromkeys(ellipse_320))
    final_ellipses_330 = list(OrderedDict.fromkeys(ellipse_330))
    final_ellipses_340 = list(OrderedDict.fromkeys(ellipse_340))
    final_ellipses_350 = list(OrderedDict.fromkeys(ellipse_350))
    final_ellipses_360 = list(OrderedDict.fromkeys(ellipse_360))
    final_ellipses_370 = list(OrderedDict.fromkeys(ellipse_370))
    final_ellipses_380 = list(OrderedDict.fromkeys(ellipse_380))
    final_ellipses_390 = list(OrderedDict.fromkeys(ellipse_390))
    final_ellipses_400 = list(OrderedDict.fromkeys(ellipse_400))
    
    count_in_crowdingZone1 = count_in_crowdingZone2 = count_in_crowdingZone3= count_in_crowdingZone4 = count_in_crowdingZone5 = 0
    count_in_crowdingZone6 = count_in_crowdingZone7 = count_in_crowdingZone8= count_in_crowdingZone9 = count_in_crowdingZone10= 0
    count_in_crowdingZone11 = count_in_crowdingZone12 = count_in_crowdingZone13= count_in_crowdingZone14 = count_in_crowdingZone15 = 0
    count_in_crowdingZone16 = count_in_crowdingZone17 = count_in_crowdingZone18= count_in_crowdingZone19 = count_in_crowdingZone20= 0
    count_in_crowdingZone21 = count_in_crowdingZone22 = count_in_crowdingZone23= count_in_crowdingZone24 = count_in_crowdingZone25 = 0
    count_in_crowdingZone26 = count_in_crowdingZone27 = count_in_crowdingZone28= count_in_crowdingZone29 = count_in_crowdingZone30= 0

    for i110, i120, i130, i140, i150, i160, i170, i180, i190, i200, i210, i220, i230, i240, i250, i260, i270, i280, i290, i300, i310, i320, i330, i340, i350, i360, i370, i380, i390, i400, \
        in zip(final_ellipses_110, final_ellipses_120, final_ellipses_130,final_ellipses_140,final_ellipses_150, \
               final_ellipses_160, final_ellipses_170, final_ellipses_180, final_ellipses_190, final_ellipses_200, \
               final_ellipses_210, final_ellipses_220, final_ellipses_230,final_ellipses_240,final_ellipses_250, \
               final_ellipses_260, final_ellipses_270, final_ellipses_280, final_ellipses_290, final_ellipses_300,\
               final_ellipses_310, final_ellipses_320, final_ellipses_330,final_ellipses_340,final_ellipses_350, \
               final_ellipses_360, final_ellipses_370, final_ellipses_380, final_ellipses_390, final_ellipses_400):

        ellipsePolygon110 = m_defineEllipses.ellipseToPolygon([i110])[0]
        ellipsePolygon120 = m_defineEllipses.ellipseToPolygon([i120])[0]
        ellipsePolygon130 = m_defineEllipses.ellipseToPolygon([i130])[0]
        ellipsePolygon140 = m_defineEllipses.ellipseToPolygon([i140])[0]
        ellipsePolygon150 = m_defineEllipses.ellipseToPolygon([i150])[0]
        ellipsePolygon160 = m_defineEllipses.ellipseToPolygon([i160])[0]
        ellipsePolygon170 = m_defineEllipses.ellipseToPolygon([i170])[0]
        ellipsePolygon180 = m_defineEllipses.ellipseToPolygon([i180])[0]
        ellipsePolygon190 = m_defineEllipses.ellipseToPolygon([i190])[0]
        ellipsePolygon200 = m_defineEllipses.ellipseToPolygon([i200])[0]
        ellipsePolygon210 = m_defineEllipses.ellipseToPolygon([i210])[0]
        ellipsePolygon220 = m_defineEllipses.ellipseToPolygon([i220])[0]
        ellipsePolygon230 = m_defineEllipses.ellipseToPolygon([i230])[0]
        ellipsePolygon240 = m_defineEllipses.ellipseToPolygon([i240])[0]
        ellipsePolygon250 = m_defineEllipses.ellipseToPolygon([i250])[0]
        ellipsePolygon260 = m_defineEllipses.ellipseToPolygon([i260])[0]
        ellipsePolygon270 = m_defineEllipses.ellipseToPolygon([i270])[0]
        ellipsePolygon280 = m_defineEllipses.ellipseToPolygon([i280])[0]
        ellipsePolygon290 = m_defineEllipses.ellipseToPolygon([i290])[0]
        ellipsePolygon300 = m_defineEllipses.ellipseToPolygon([i300])[0]
        ellipsePolygon310 = m_defineEllipses.ellipseToPolygon([i310])[0]
        ellipsePolygon320 = m_defineEllipses.ellipseToPolygon([i320])[0]
        ellipsePolygon330 = m_defineEllipses.ellipseToPolygon([i330])[0]
        ellipsePolygon340 = m_defineEllipses.ellipseToPolygon([i340])[0]
        ellipsePolygon350 = m_defineEllipses.ellipseToPolygon([i350])[0]
        ellipsePolygon360 = m_defineEllipses.ellipseToPolygon([i360])[0]
        ellipsePolygon370 = m_defineEllipses.ellipseToPolygon([i370])[0]
        ellipsePolygon380 = m_defineEllipses.ellipseToPolygon([i380])[0]
        ellipsePolygon390 = m_defineEllipses.ellipseToPolygon([i390])[0]
        ellipsePolygon400 = m_defineEllipses.ellipseToPolygon([i400])[0]

        epPolygon110 = Polygon(ellipsePolygon110)
        epPolygon120 = Polygon(ellipsePolygon120)
        epPolygon130 = Polygon(ellipsePolygon130)
        epPolygon140 = Polygon(ellipsePolygon140)
        epPolygon150 = Polygon(ellipsePolygon150)
        epPolygon160 = Polygon(ellipsePolygon160)
        epPolygon170 = Polygon(ellipsePolygon170)
        epPolygon180 = Polygon(ellipsePolygon180)
        epPolygon190 = Polygon(ellipsePolygon190)
        epPolygon200 = Polygon(ellipsePolygon200)
        epPolygon210 = Polygon(ellipsePolygon210)
        epPolygon220 = Polygon(ellipsePolygon220)
        epPolygon230 = Polygon(ellipsePolygon230)
        epPolygon240 = Polygon(ellipsePolygon240)
        epPolygon250 = Polygon(ellipsePolygon250)
        epPolygon260 = Polygon(ellipsePolygon260)
        epPolygon270 = Polygon(ellipsePolygon270)
        epPolygon280 = Polygon(ellipsePolygon280)
        epPolygon290 = Polygon(ellipsePolygon290)
        epPolygon300 = Polygon(ellipsePolygon300)
        epPolygon310 = Polygon(ellipsePolygon310)
        epPolygon320 = Polygon(ellipsePolygon320)
        epPolygon330 = Polygon(ellipsePolygon330)
        epPolygon340 = Polygon(ellipsePolygon340)
        epPolygon350 = Polygon(ellipsePolygon350)
        epPolygon360 = Polygon(ellipsePolygon360)
        epPolygon370 = Polygon(ellipsePolygon370)
        epPolygon380 = Polygon(ellipsePolygon380)
        epPolygon390 = Polygon(ellipsePolygon390)
        epPolygon400 = Polygon(ellipsePolygon400)

        for posi in display_posi:
            if epPolygon110.contains(Point(posi)) == True:
                count_in_crowdingZone1 += 1
            if epPolygon120.contains(Point(posi)) == True:
                count_in_crowdingZone2 += 1
            if epPolygon130.contains(Point(posi)) == True:
                count_in_crowdingZone3 += 1
            if epPolygon140.contains(Point(posi)) == True:
                count_in_crowdingZone4 += 1
            if epPolygon150.contains(Point(posi)) == True:
                count_in_crowdingZone5 += 1
            if epPolygon160.contains(Point(posi)) == True:
                count_in_crowdingZone6 += 1
            if epPolygon170.contains(Point(posi)) == True:
                count_in_crowdingZone7 += 1
            if epPolygon180.contains(Point(posi)) == True:
                count_in_crowdingZone8 += 1
            if epPolygon190.contains(Point(posi)) == True:
                count_in_crowdingZone9 += 1
            if epPolygon200.contains(Point(posi)) == True:
                count_in_crowdingZone10 += 1
            if epPolygon210.contains(Point(posi)) == True:
                count_in_crowdingZone11 += 1
            if epPolygon220.contains(Point(posi)) == True:
                count_in_crowdingZone12 += 1
            if epPolygon230.contains(Point(posi)) == True:
                count_in_crowdingZone13 += 1
            if epPolygon240.contains(Point(posi)) == True:
                count_in_crowdingZone14 += 1
            if epPolygon250.contains(Point(posi)) == True:
                count_in_crowdingZone15 += 1
            if epPolygon260.contains(Point(posi)) == True:
                count_in_crowdingZone16 += 1
            if epPolygon270.contains(Point(posi)) == True:
                count_in_crowdingZone17 += 1
            if epPolygon280.contains(Point(posi)) == True:
                count_in_crowdingZone18 += 1
            if epPolygon290.contains(Point(posi)) == True:
                count_in_crowdingZone19 += 1
            if epPolygon300.contains(Point(posi)) == True:
                count_in_crowdingZone20 += 1
            if epPolygon310.contains(Point(posi)) == True:
                count_in_crowdingZone21 += 1
            if epPolygon320.contains(Point(posi)) == True:
                count_in_crowdingZone22 += 1
            if epPolygon330.contains(Point(posi)) == True:
                count_in_crowdingZone23 += 1
            if epPolygon340.contains(Point(posi)) == True:
                count_in_crowdingZone24 += 1
            if epPolygon350.contains(Point(posi)) == True:
                count_in_crowdingZone25 += 1
            if epPolygon360.contains(Point(posi)) == True:
                count_in_crowdingZone26 += 1
            if epPolygon370.contains(Point(posi)) == True:
                count_in_crowdingZone27 += 1
            if epPolygon380.contains(Point(posi)) == True:
                count_in_crowdingZone28 += 1
            if epPolygon390.contains(Point(posi)) == True:
                count_in_crowdingZone29 += 1
            if epPolygon400.contains(Point(posi)) == True:
                count_in_crowdingZone30 += 1

    count_number_end1   = count_in_crowdingZone1 -len(display_posi)
    count_number_end2   = count_in_crowdingZone2 -len(display_posi)
    count_number_end3   = count_in_crowdingZone3 -len(display_posi)
    count_number_end4   = count_in_crowdingZone4 -len(display_posi)
    count_number_end5   = count_in_crowdingZone5 -len(display_posi)
    count_number_end6   = count_in_crowdingZone6 -len(display_posi)
    count_number_end7   = count_in_crowdingZone7 -len(display_posi)
    count_number_end8   = count_in_crowdingZone8 -len(display_posi)
    count_number_end9   = count_in_crowdingZone9 -len(display_posi)
    count_number_end10  = count_in_crowdingZone10-len(display_posi)
    count_number_end11  = count_in_crowdingZone11-len(display_posi)
    count_number_end12  = count_in_crowdingZone12-len(display_posi)
    count_number_end13  = count_in_crowdingZone13-len(display_posi)
    count_number_end14  = count_in_crowdingZone14-len(display_posi)
    count_number_end15  = count_in_crowdingZone15-len(display_posi)
    count_number_end16  = count_in_crowdingZone16-len(display_posi)
    count_number_end17  = count_in_crowdingZone17-len(display_posi)
    count_number_end18  = count_in_crowdingZone18-len(display_posi)
    count_number_end19  = count_in_crowdingZone19-len(display_posi)
    count_number_end20  = count_in_crowdingZone20-len(display_posi)
    count_number_end21  = count_in_crowdingZone21-len(display_posi)
    count_number_end22  = count_in_crowdingZone22-len(display_posi)
    count_number_end23  = count_in_crowdingZone23-len(display_posi)
    count_number_end24  = count_in_crowdingZone24-len(display_posi)
    count_number_end25  = count_in_crowdingZone25-len(display_posi)
    count_number_end26  = count_in_crowdingZone26-len(display_posi)
    count_number_end27  = count_in_crowdingZone27-len(display_posi)
    count_number_end28  = count_in_crowdingZone28-len(display_posi)
    count_number_end29  = count_in_crowdingZone29-len(display_posi)
    count_number_end30  = count_in_crowdingZone30-len(display_posi)
    
    list_count_in_crowdingZone1.append(count_number_end1)
    list_count_in_crowdingZone2.append(count_number_end2)
    list_count_in_crowdingZone3.append(count_number_end3)
    list_count_in_crowdingZone4.append(count_number_end4)
    list_count_in_crowdingZone5.append(count_number_end5)
    list_count_in_crowdingZone6.append(count_number_end6)
    list_count_in_crowdingZone7.append(count_number_end7)
    list_count_in_crowdingZone8.append(count_number_end8)
    list_count_in_crowdingZone9.append(count_number_end9)
    list_count_in_crowdingZone10.append(count_number_end10)
    list_count_in_crowdingZone11.append(count_number_end11)
    list_count_in_crowdingZone12.append(count_number_end12)
    list_count_in_crowdingZone13.append(count_number_end13)
    list_count_in_crowdingZone14.append(count_number_end14)
    list_count_in_crowdingZone15.append(count_number_end15)
    list_count_in_crowdingZone16.append(count_number_end16)
    list_count_in_crowdingZone17.append(count_number_end17)
    list_count_in_crowdingZone18.append(count_number_end18)
    list_count_in_crowdingZone19.append(count_number_end19)
    list_count_in_crowdingZone20.append(count_number_end20)
    list_count_in_crowdingZone21.append(count_number_end21)
    list_count_in_crowdingZone22.append(count_number_end22)
    list_count_in_crowdingZone23.append(count_number_end23)
    list_count_in_crowdingZone24.append(count_number_end24)
    list_count_in_crowdingZone25.append(count_number_end25)
    list_count_in_crowdingZone26.append(count_number_end26)
    list_count_in_crowdingZone27.append(count_number_end27)
    list_count_in_crowdingZone28.append(count_number_end28)
    list_count_in_crowdingZone29.append(count_number_end29)
    list_count_in_crowdingZone30.append(count_number_end30)

stimuliInfo.insert(1, 'count_number1',list_count_in_crowdingZone1)
stimuliInfo.insert(1, 'count_number2',list_count_in_crowdingZone2)
stimuliInfo.insert(1, 'count_number3',list_count_in_crowdingZone3)
stimuliInfo.insert(1, 'count_number4',list_count_in_crowdingZone4)
stimuliInfo.insert(1, 'count_number5',list_count_in_crowdingZone5)
stimuliInfo.insert(1, 'count_number6',list_count_in_crowdingZone6)
stimuliInfo.insert(1, 'count_number7',list_count_in_crowdingZone7)
stimuliInfo.insert(1, 'count_number8',list_count_in_crowdingZone8)
stimuliInfo.insert(1, 'count_number9',list_count_in_crowdingZone9)
stimuliInfo.insert(1, 'count_number10',list_count_in_crowdingZone10)
stimuliInfo.insert(1, 'count_number11',list_count_in_crowdingZone11)
stimuliInfo.insert(1, 'count_number12',list_count_in_crowdingZone12)
stimuliInfo.insert(1, 'count_number13',list_count_in_crowdingZone13)
stimuliInfo.insert(1, 'count_number14',list_count_in_crowdingZone14)
stimuliInfo.insert(1, 'count_number15',list_count_in_crowdingZone15)
stimuliInfo.insert(1, 'count_number16',list_count_in_crowdingZone16)
stimuliInfo.insert(1, 'count_number17',list_count_in_crowdingZone17)
stimuliInfo.insert(1, 'count_number18',list_count_in_crowdingZone18)
stimuliInfo.insert(1, 'count_number19',list_count_in_crowdingZone19)
stimuliInfo.insert(1, 'count_number20',list_count_in_crowdingZone20)
stimuliInfo.insert(1, 'count_number21',list_count_in_crowdingZone21)
stimuliInfo.insert(1, 'count_number22',list_count_in_crowdingZone22)
stimuliInfo.insert(1, 'count_number23',list_count_in_crowdingZone23)
stimuliInfo.insert(1, 'count_number24',list_count_in_crowdingZone24)
stimuliInfo.insert(1, 'count_number25',list_count_in_crowdingZone25)
stimuliInfo.insert(1, 'count_number26',list_count_in_crowdingZone26)
stimuliInfo.insert(1, 'count_number27',list_count_in_crowdingZone27)
stimuliInfo.insert(1, 'count_number28',list_count_in_crowdingZone28)
stimuliInfo.insert(1, 'count_number29',list_count_in_crowdingZone29)
stimuliInfo.insert(1, 'count_number30',list_count_in_crowdingZone30)

stimuliInfo.to_excel('try1.xlsx')
stimuliInfo_C  = stimuliInfo[stimuliInfo.crowdingcons == 1] 
stimuliInfo_NC = stimuliInfo[stimuliInfo.crowdingcons == 0] 
#%%=============================================================================
# pd dataFrame add csv
# =============================================================================
totalData = pd.DataFrame()
for i in data_csv:
    data_exp1 =pd.read_csv('../'+i) #data in partent directory
    totalData = totalData.append(data_exp1)

totalData = totalData.reset_index(drop=True)
#%%=============================================================================
# remove outliers #TODO
# =============================================================================
# per numerosity
totalData_21 = totalData[totalData.Numerosity == 21]
totalData_22 = totalData[totalData.Numerosity == 22]
totalData_23 = totalData[totalData.Numerosity == 23]
totalData_24 = totalData[totalData.Numerosity == 24]
totalData_25 = totalData[totalData.Numerosity == 25]
totalData_31 = totalData[totalData.Numerosity == 31]
totalData_32 = totalData[totalData.Numerosity == 32]
totalData_33 = totalData[totalData.Numerosity == 33]
totalData_34 = totalData[totalData.Numerosity == 34]
totalData_35 = totalData[totalData.Numerosity == 35]
totalData_41 = totalData[totalData.Numerosity == 41]
totalData_42 = totalData[totalData.Numerosity == 42]
totalData_43 = totalData[totalData.Numerosity == 43]
totalData_44 = totalData[totalData.Numerosity == 44]
totalData_45 = totalData[totalData.Numerosity == 45]
totalData_49 = totalData[totalData.Numerosity == 49]
totalData_50 = totalData[totalData.Numerosity == 50]
totalData_51 = totalData[totalData.Numerosity == 51]
totalData_52 = totalData[totalData.Numerosity == 52]
totalData_53 = totalData[totalData.Numerosity == 53]
totalData_54 = totalData[totalData.Numerosity == 54]
totalData_55 = totalData[totalData.Numerosity == 55]
totalData_56 = totalData[totalData.Numerosity == 56]
totalData_57 = totalData[totalData.Numerosity == 57]
totalData_58 = totalData[totalData.Numerosity == 58]

# remove obvious outliers
totalData_21 = totalData_21[(totalData['response']< (2*21)) & (totalData['response']>= math.sqrt(21))]
totalData_22 = totalData_22[(totalData['response']< (2*22)) & (totalData['response']>= math.sqrt(22))]
totalData_23 = totalData_23[(totalData['response']< (2*23)) & (totalData['response']>= math.sqrt(23))]
totalData_24 = totalData_24[(totalData['response']< (2*24)) & (totalData['response']>= math.sqrt(24))]
totalData_25 = totalData_25[(totalData['response']< (2*25)) & (totalData['response']>= math.sqrt(25))]
totalData_31 = totalData_31[(totalData['response']< (2*31)) & (totalData['response']>= math.sqrt(31))]
totalData_32 = totalData_32[(totalData['response']< (2*32)) & (totalData['response']>= math.sqrt(32))]
totalData_33 = totalData_33[(totalData['response']< (2*33)) & (totalData['response']>= math.sqrt(33))]
totalData_34 = totalData_34[(totalData['response']< (2*34)) & (totalData['response']>= math.sqrt(34))]
totalData_35 = totalData_35[(totalData['response']< (2*35)) & (totalData['response']>= math.sqrt(35))]
totalData_41 = totalData_41[(totalData['response']< (2*41)) & (totalData['response']>= math.sqrt(41))]
totalData_42 = totalData_42[(totalData['response']< (2*42)) & (totalData['response']>= math.sqrt(42))]
totalData_43 = totalData_43[(totalData['response']< (2*43)) & (totalData['response']>= math.sqrt(43))]
totalData_44 = totalData_44[(totalData['response']< (2*44)) & (totalData['response']>= math.sqrt(44))]
totalData_45 = totalData_45[(totalData['response']< (2*45)) & (totalData['response']>= math.sqrt(45))]
totalData_49 = totalData_49[(totalData['response']< (2*49)) & (totalData['response']>= math.sqrt(49))]
totalData_50 = totalData_50[(totalData['response']< (2*50)) & (totalData['response']>= math.sqrt(50))]
totalData_51 = totalData_51[(totalData['response']< (2*51)) & (totalData['response']>= math.sqrt(51))]
totalData_52 = totalData_52[(totalData['response']< (2*52)) & (totalData['response']>= math.sqrt(52))]
totalData_53 = totalData_53[(totalData['response']< (2*53)) & (totalData['response']>= math.sqrt(53))]
totalData_54 = totalData_54[(totalData['response']< (2*54)) & (totalData['response']>= math.sqrt(54))]
totalData_55 = totalData_55[(totalData['response']< (2*55)) & (totalData['response']>= math.sqrt(55))]
totalData_56 = totalData_56[(totalData['response']< (2*56)) & (totalData['response']>= math.sqrt(56))]
totalData_57 = totalData_57[(totalData['response']< (2*57)) & (totalData['response']>= math.sqrt(57))]
totalData_58 = totalData_58[(totalData['response']< (2*58)) & (totalData['response']>= math.sqrt(58))]

#%% see data now
totalData_temp = pd.concat([totalData_21, 
                            totalData_22,
                            totalData_23,
                            totalData_24,
                            totalData_25,
                            totalData_31,
                            totalData_32,
                            totalData_33,
                            totalData_34,
                            totalData_35,
                            totalData_41,
                            totalData_42,
                            totalData_43,
                            totalData_44,
                            totalData_45,
                            totalData_49,
                            totalData_50,
                            totalData_51,
                            totalData_52,
                            totalData_53,
                            totalData_54,
                            totalData_55,
                            totalData_56,
                            totalData_57,
                            totalData_58], ignore_index=True)
try:
    totalData_temp.drop(totalData_temp.columns[totalData_temp.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
except: NameError
# rename blockNo to winsize which is more meaningful
# totalData.rename(columns={'blockNo':'winsize'}, inplace=True)
# totalData_temp.to_excel('totaldata_temp.xlsx',sheet_name = 'Sheet1')
#%% keep data within 2 std

resp_std21  = totalData_21['response'].std()
resp_mean21 = totalData_21['response'].mean()
resp_min21 = resp_mean21-2*resp_std21
resp_max21 = resp_mean21+2*resp_std21
totalData_21 = totalData_21[(totalData_21['response'] < resp_max21) & (totalData_21['response'] > resp_min21)]

resp_std22  = totalData_22['response'].std()
resp_mean22 = totalData_22['response'].mean()
resp_min22 = resp_mean22-2*resp_std22
resp_max22 = resp_mean22+2*resp_std22
totalData_22 = totalData_22[(totalData_22['response'] < resp_max22) & (totalData_22['response'] > resp_min22)]

resp_std23  = totalData_23['response'].std()
resp_mean23 = totalData_23['response'].mean()
resp_min23 = resp_mean23-2*resp_std23
resp_max23 = resp_mean23+2*resp_std23
totalData_23 = totalData_23[(totalData_23['response'] < resp_max23) & (totalData_23['response'] > resp_min23)]

resp_std24  = totalData_24['response'].std()
resp_mean24 = totalData_24['response'].mean()
resp_min24 = resp_mean24-2*resp_std24
resp_max24 = resp_mean24+2*resp_std24
totalData_24 = totalData_24[(totalData_24['response'] < resp_max24) & (totalData_24['response'] > resp_min24)]

resp_std25  = totalData_25['response'].std()
resp_mean25 = totalData_25['response'].mean()
resp_min25 = resp_mean25-2*resp_std25
resp_max25 = resp_mean25+2*resp_std25
totalData_25 = totalData_25[(totalData_25['response'] < resp_max25) & (totalData_25['response'] > resp_min25)]

resp_std31  = totalData_31['response'].std()
resp_mean31 = totalData_31['response'].mean()
resp_min31 = resp_mean31-2*resp_std31
resp_max31 = resp_mean31+2*resp_std31
totalData_31 = totalData_31[(totalData_31['response'] < resp_max31) & (totalData_31['response'] > resp_min31)]

resp_std32  = totalData_32['response'].std()
resp_mean32 = totalData_32['response'].mean()
resp_min32 = resp_mean32-2*resp_std32
resp_max32 = resp_mean32+2*resp_std32
totalData_32 = totalData_32[(totalData_32['response'] < resp_max32) & (totalData_32['response'] > resp_min32)]

resp_std33  = totalData_33['response'].std()
resp_mean33 = totalData_33['response'].mean()
resp_min33 = resp_mean33-2*resp_std33
resp_max33 = resp_mean33+2*resp_std33
totalData_33 = totalData_33[(totalData_33['response'] < resp_max33) & (totalData_33['response'] > resp_min33)]

resp_std34  = totalData_34['response'].std()
resp_mean34 = totalData_34['response'].mean()
resp_min34 = resp_mean34-2*resp_std34
resp_max34 = resp_mean34+2*resp_std34
totalData_34 = totalData_34[(totalData_34['response'] < resp_max34) & (totalData_34['response'] > resp_min34)]

resp_std35  = totalData_35['response'].std()
resp_mean35 = totalData_35['response'].mean()
resp_min35 = resp_mean35-2*resp_std35
resp_max35 = resp_mean35+2*resp_std35
totalData_35 = totalData_35[(totalData_35['response'] < resp_max35) & (totalData_35['response'] > resp_min35)]

resp_std41  = totalData_41['response'].std()
resp_mean41 = totalData_41['response'].mean()
resp_min41 = resp_mean41-2*resp_std41
resp_max41 = resp_mean41+2*resp_std41
totalData_41 = totalData_41[(totalData_41['response'] < resp_max41) & (totalData_41['response'] > resp_min41)]

resp_std42  = totalData_42['response'].std()
resp_mean42 = totalData_42['response'].mean()
resp_min42 = resp_mean42-2*resp_std42
resp_max42 = resp_mean42+2*resp_std42
totalData_42 = totalData_42[(totalData_42['response'] < resp_max42) & (totalData_42['response'] > resp_min42)]

resp_std43  = totalData_43['response'].std()
resp_mean43 = totalData_43['response'].mean()
resp_min43 = resp_mean43-2*resp_std43
resp_max43 = resp_mean43+2*resp_std43
totalData_43 = totalData_43[(totalData_43['response'] < resp_max43) & (totalData_43['response'] > resp_min43)]

resp_std44  = totalData_44['response'].std()
resp_mean44 = totalData_44['response'].mean()
resp_min44 = resp_mean44-2*resp_std44
resp_max44 = resp_mean44+2*resp_std44
totalData_44 = totalData_44[(totalData_44['response'] < resp_max44) & (totalData_44['response'] > resp_min44)]

resp_std45  = totalData_45['response'].std()
resp_mean45 = totalData_45['response'].mean()
resp_min45 = resp_mean45-2*resp_std45
resp_max45 = resp_mean45+2*resp_std45
totalData_45 = totalData_45[(totalData_45['response'] < resp_max45) & (totalData_45['response'] > resp_min45)]

resp_std49  = totalData_49['response'].std()
resp_mean49 = totalData_49['response'].mean()
resp_min49 = resp_mean49-2*resp_std49
resp_max49 = resp_mean49+2*resp_std49
totalData_49 = totalData_49[(totalData_49['response'] < resp_max49) & (totalData_49['response'] > resp_min49)]

resp_std50  = totalData_50['response'].std()
resp_mean50 = totalData_50['response'].mean()
resp_min50 = resp_mean50-2*resp_std50
resp_max50 = resp_mean50+2*resp_std50
totalData_50 = totalData_50[(totalData_50['response'] < resp_max50) & (totalData_50['response'] > resp_min50)]

resp_std51  = totalData_51['response'].std()
resp_mean51 = totalData_51['response'].mean()
resp_min51 = resp_mean51-2*resp_std51
resp_max51 = resp_mean51+2*resp_std51
totalData_51 = totalData_51[(totalData_51['response'] < resp_max51) & (totalData_51['response'] > resp_min51)]

resp_std52  = totalData_52['response'].std()
resp_mean52 = totalData_52['response'].mean()
resp_min52 = resp_mean52-2*resp_std52
resp_max52 = resp_mean52+2*resp_std52
totalData_52 = totalData_52[(totalData_52['response'] < resp_max52) & (totalData_52['response'] > resp_min52)]

resp_std53  = totalData_53['response'].std()
resp_mean53 = totalData_53['response'].mean()
resp_min53 = resp_mean53-2*resp_std53
resp_max53 = resp_mean53+2*resp_std53
totalData_53 = totalData_53[(totalData_53['response'] < resp_max53) & (totalData_53['response'] > resp_min53)]

resp_std54  = totalData_54['response'].std()
resp_mean54 = totalData_54['response'].mean()
resp_min54 = resp_mean54-2*resp_std54
resp_max54 = resp_mean54+2*resp_std54
totalData_54 = totalData_54[(totalData_54['response'] < resp_max54) & (totalData_54['response'] > resp_min54)]

resp_std55  = totalData_55['response'].std()
resp_mean55 = totalData_55['response'].mean()
resp_min55 = resp_mean55-2*resp_std55
resp_max55 = resp_mean55+2*resp_std55
totalData_55 = totalData_55[(totalData_55['response'] < resp_max55) & (totalData_55['response'] > resp_min55)]

resp_std56  = totalData_56['response'].std()
resp_mean56 = totalData_56['response'].mean()
resp_min56 = resp_mean56-2*resp_std56
resp_max56 = resp_mean56+2*resp_std56
totalData_56 = totalData_56[(totalData_56['response'] < resp_max56) & (totalData_56['response'] > resp_min56)]

resp_std57  = totalData_57['response'].std()
resp_mean57 = totalData_57['response'].mean()
resp_min57 = resp_mean57-2*resp_std57
resp_max57 = resp_mean57+2*resp_std57
totalData_57 = totalData_57[(totalData_57['response'] < resp_max57) & (totalData_57['response'] > resp_min57)]

resp_std58  = totalData_58['response'].std()
resp_mean58 = totalData_58['response'].mean()
resp_min58 = resp_mean58-2*resp_std58
resp_max58 = resp_mean58+2*resp_std58
totalData_58 = totalData_58[(totalData_58['response'] < resp_max58) & (totalData_58['response'] > resp_min58)]

totalData_new = pd.concat([totalData_21, 
                           totalData_22,
                           totalData_23,
                           totalData_24,
                           totalData_25,
                           totalData_31,
                           totalData_32,
                           totalData_33,
                           totalData_34,
                           totalData_35,
                           totalData_41,
                           totalData_42,
                           totalData_43,
                           totalData_44,
                           totalData_45,
                           totalData_49,
                           totalData_50,
                           totalData_51,
                           totalData_52,
                           totalData_53,
                           totalData_54,
                           totalData_55,
                           totalData_56,
                           totalData_57,
                           totalData_58], ignore_index=True)

totalData_new = totalData_new.reset_index(drop=True)
#%%=============================================================================
# insert new index (estimation - N_disk)
# =============================================================================
# #version1
# def caculateNewRsep(row):
#     newResp = row['response'] - row['Numerosity']
#     return newResp
# totalData['resp_index'] =totalData.apply(lambda row: caculateNewRsep(row), axis =1)
# version2
totalData_new['deviation_score'] = totalData_new['response'] - totalData_new['Numerosity']

# a = totalData.drop(totalData.columns[12], axis=1)

#%%=============================================================================
# clean data files
# =============================================================================
to_drop = ['pk','strictResponse','expName','handness','stimuliPresentTime']
totalData_new.drop(columns=to_drop, inplace = True)
# totalData.to_excel('temp2.xlsx',sheet_name = 'try')

# # rename group colums
# def label_group(row):
#     if row['group'] == 1:
#         return 'normal'
#     elif row['group'] == 2:
#         return 'dyslexic'
# totalData['groupName'] = totalData.apply(lambda row: label_group(row), axis =1)

#get imageFile number: file number is the first digit of the stimuli name
# def imageFile_to_number(filename):
#     tempFileNumber = ''
#     for in_file in filename:
#         tempFileNumber = tempFileNumber + in_file
#         if not tempFileNumber.isdigit():
#             tempFileNumber = tempFileNumber[0:len(tempFileNumber)-1]
#             return int(tempFileNumber)
# totalData['fileNumber'] = totalData['imageFile'].map(imageFile_to_number)

#%% Try merge indevidual data file with stimuliInfo
# ws0.7_crowding1_n448_Ndisk57.png --> 448
def imageFile_to_number(filename):
    # find()方法：查找子字符串，若找到返回从0开始的下标值，若找不到返回-1
    # if filename.find('_copy') == -1:
    #     numberEndIndex = filename.find('_Ndisk')
    # else:
    #     numberEndIndex = filename.find('_copy')
    numberEndIndex = filename.find('_Ndisk')
    filename = filename[18:numberEndIndex]
    return filename
def imageFile_to_number2(filename):
    filename = filename[3:6]
    return filename
# totalData['fileNumber'] = totalData['imageFile'].map(imageFile_to_number)

# merge two stimuliinfo with individal data
stimuliInfo_toMerge = pd.read_excel('../fullStimuliInfo.xlsx')# check index number-each row should an unique row
stimuliInfo_toMerge['index_stimuliInfo'] = stimuliInfo_toMerge['index_stimuliInfo'].astype(str)

totalData_new['index_stimuliInfo'] = totalData_new['Display'].map(imageFile_to_number)
totalData_new['winsize'] = totalData_new['Display'].map(imageFile_to_number2)

# make sure columns name are same
totalData_new.rename(columns ={'Numerosity':'N_disk'},inplace = True) 
totalData_new.rename(columns ={'Crowding':'crowdingcons'},inplace = True)

# make sure the colums type are same for both files
totalData_new['crowdingcons']=totalData_new['crowdingcons'].astype(int)
totalData_new['winsize']=totalData_new['winsize'].astype(float)
totalData_new['index_stimuliInfo']=totalData_new['index_stimuliInfo'].astype(str)
totalData_new['N_disk']=totalData_new['N_disk'].astype(int)

# FIXME
# #run while local density was calculated 
# #dorp unnamed colum if needed
# try:
#     totalData_new.drop(totalData_new.columns[totalData_new.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
# except: NameError
# # rename blockNo to winsize which is more meaningful
# # totalData.rename(columns={'blockNo':'winsize'}, inplace=True)
# totalData_new.to_excel('cleanedTotalData_fullinfo_d.xlsx',sheet_name = 'sheet1')

#merge now
totalData_new = pd.merge(totalData_new,stimuliInfo_toMerge, how = 'left', on = ['index_stimuliInfo', 'N_disk', 'crowdingcons','winsize'])
# pp_data.drop_duplicates()

#%%dorp unnamed colum if needed
try:
    totalData_new.drop(totalData_new.columns[totalData_new.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
except: NameError
# rename blockNo to winsize which is more meaningful
# totalData.rename(columns={'blockNo':'winsize'}, inplace=True)
totalData_new.to_excel('cleanedTotalData_fullinfo.xlsx',sheet_name = 'cleanedTotalData')
#%% =============================================================================
# 250 displays into different winsize
# =============================================================================
stimuliInfo_toMerge_03    = stimuliInfo_toMerge[stimuliInfo_toMerge.winsize==0.3]
stimuliInfo_toMerge_04    = stimuliInfo_toMerge[stimuliInfo_toMerge.winsize==0.4]
stimuliInfo_toMerge_05    = stimuliInfo_toMerge[stimuliInfo_toMerge.winsize==0.5]
stimuliInfo_toMerge_06    = stimuliInfo_toMerge[stimuliInfo_toMerge.winsize==0.6]
stimuliInfo_toMerge_07    = stimuliInfo_toMerge[stimuliInfo_toMerge.winsize==0.7]

stimuliInfo_toMerge_03_C  = stimuliInfo_toMerge_03[stimuliInfo_toMerge_03.crowdingcons==1]
stimuliInfo_toMerge_04_C  = stimuliInfo_toMerge_04[stimuliInfo_toMerge_04.crowdingcons==1]
stimuliInfo_toMerge_05_C  = stimuliInfo_toMerge_05[stimuliInfo_toMerge_05.crowdingcons==1]
stimuliInfo_toMerge_06_C  = stimuliInfo_toMerge_06[stimuliInfo_toMerge_06.crowdingcons==1]
stimuliInfo_toMerge_07_C  = stimuliInfo_toMerge_07[stimuliInfo_toMerge_07.crowdingcons==1]

stimuliInfo_toMerge_03_NC = stimuliInfo_toMerge_03[stimuliInfo_toMerge_03.crowdingcons==0]
stimuliInfo_toMerge_04_NC = stimuliInfo_toMerge_04[stimuliInfo_toMerge_04.crowdingcons==0]
stimuliInfo_toMerge_05_NC = stimuliInfo_toMerge_05[stimuliInfo_toMerge_05.crowdingcons==0]
stimuliInfo_toMerge_06_NC = stimuliInfo_toMerge_06[stimuliInfo_toMerge_06.crowdingcons==0]
stimuliInfo_toMerge_07_NC = stimuliInfo_toMerge_07[stimuliInfo_toMerge_07.crowdingcons==0]

#%%=============================================================================
# # if we need to remove any participant?
# # =============================================================================
# eachParticipant  = totalData.groupby(['participant_N']).mean()
# # EachParticipant.to_excel('dataByParticipant.xlsx')
# p_std =eachParticipant['resp_index'].std()
# p_mean=eachParticipant['resp_index'].mean()
# p_max =p_mean +2* p_std
# p_min =p_mean -2* p_std

# pFinal = eachParticipant[(eachParticipant['resp_index'] < p_max) & (eachParticipant['resp_index'] > p_min)]

#%% =============================================================================
# remove outlier participants
# =============================================================================
# finalData = totalData[totalData.participant_N != 2]
#%% =============================================================================
# pivot table
# =============================================================================
#NO.1
# pivotT = pd.pivot_table(totalData_new,index = ['crowdingcons','participant_N'], columns = ['winsize', 'N_disk'],values = ['deviation_score'])
# pivotT.to_excel('try2.xlsx')
# pivotT = pd.pivot_table(totalData,index = ['whichBlocks','CrowdingCons','group','participant'], columns = ['winsize', 'N_disk'],values = ['resp_index'])
#NO.2
#totatC: all crowding conditions
totalC = totalData_new[totalData_new.crowdingcons == 1]
totalNC= totalData_new[totalData_new.crowdingcons == 0]
totalC_N49_58  = totalC.loc[(totalC['winsize'] >= 0.6) & (totalC['winsize'] <= 0.7)]
totalNC_N49_58 = totalNC.loc[(totalNC['winsize'] >= 0.6) & (totalNC['winsize'] <= 0.7)]

totalC_N49_53 = totalC[totalC.winsize == 0.6]
totalC_N54_58 = totalC[totalC.winsize == 0.7]

totalNC_N49_53 = totalNC[totalNC.winsize == 0.6]
totalNC_N54_58 = totalNC[totalNC.winsize == 0.7]

# pivotT_C_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number'], values = ['deviation_score'])
# pivotT_C1_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number1'], values = ['deviation_score'])
# pivotT_C2_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number2'], values = ['deviation_score'])
# pivotT_C3_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number3'], values = ['deviation_score'])
# pivotT_C4_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number4'], values = ['deviation_score'])
# pivotT_C5_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number5'], values = ['deviation_score'])
# pivotT_C6_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number6'], values = ['deviation_score'])
# pivotT_C7_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number7'], values = ['deviation_score'])
# pivotT_C8_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number8'], values = ['deviation_score'])
# pivotT_C9_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number9'], values = ['deviation_score'])
# pivotT_C10_N49_58 = pd.pivot_table(totalC_N49_58, index = ['participant_N'], columns = ['count_number10'], values = ['deviation_score'])

# # pivotT_C = pd.pivot_table(totalC, index = ['participant_N'], columns = ['winsize', 'count_number'],values = ['deviation_score'])
# pivotT_C  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number'],values = ['deviation_score'])
# pivotT_NC = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number'],values = ['deviation_score'])

# pivotT_C1  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number1'],values = ['deviation_score'])
# pivotT_NC1 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number1'],values = ['deviation_score'])

# pivotT_C2  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number2'],values = ['deviation_score'])
# pivotT_NC2 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number2'],values = ['deviation_score'])

# pivotT_C3 = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number3'],values = ['deviation_score'])
# pivotT_NC3 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number3'],values = ['deviation_score'])

# pivotT_C4  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number4'],values = ['deviation_score'])
# pivotT_NC4= pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number4'],values = ['deviation_score'])

# pivotT_C5 = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number5'],values = ['deviation_score'])
# pivotT_NC5 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number5'],values = ['deviation_score'])

# pivotT_C6  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number6'],values = ['deviation_score'])
# pivotT_NC6 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number6'],values = ['deviation_score'])

# pivotT_C7  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number7'],values = ['deviation_score'])
# pivotT_NC7 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number7'],values = ['deviation_score'])

# pivotT_C8  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number8'],values = ['deviation_score'])
# pivotT_NC8 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number8'],values = ['deviation_score'])

# pivotT_C9  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number9'],values = ['deviation_score'])
# pivotT_NC9 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number9'],values = ['deviation_score'])

# pivotT_C10  = pd.pivot_table(totalC,  index = ['participant_N'], columns = [ 'winsize','count_number10'],values = ['deviation_score'])
# pivotT_NC10 = pd.pivot_table(totalNC, index = ['participant_N'], columns = [ 'winsize','count_number10'],values = ['deviation_score'])
#scater plot deviation against No.discs into others' crwoding zone
# # No.3
# crowding_ws7 = totalC[totalC.winsize == 0.7]
# crowding_ws6 = totalC[totalC.winsize == 0.6]
# crowding_ws5 = totalC[totalC.winsize == 0.5]
# crowding_ws4 = totalC[totalC.winsize == 0.4]
# crowding_ws3 = totalC[totalC.winsize == 0.3]

# # crowding_ws7_try1 = crowding_ws7.groupby(['count_number'], as_index = False).mean()
# ax2 = sns.scatterplot(x='count_number9',y = 'deviation_score', data = crowding_ws7, color = 'k')

#%%============================================================================
# write pivot table to excel (if needed)
# =============================================================================
# writer = pd.ExcelWriter('try.xlsx',engine='xlsxwriter')
# pivotT_C.to_excel(writer, sheet_name = 'crowding_countN')
# # pivotT_NC_countNumber.to_excel(writer, sheet_name = 'no_crowdin_count_N')
# # pivotT_C_tradi.to_excel(writer, sheet_name = 'crowding_tradi')
# # pivotT_NC_tradi.to_excel(writer, sheet_name = 'no_crowding_tradi')
# writer.save()
#
# pivotT_C_N49_58.to_excel('c49_58_countN.xlsx')
# pivotT_C1_N49_58.to_excel('c49_58_countN1.xlsx')
# pivotT_C2_N49_58.to_excel('c49_58_countN2.xlsx')
# pivotT_C3_N49_58.to_excel('c49_58_countN3.xlsx')
# pivotT_C4_N49_58.to_excel('c49_58_countN4.xlsx')
# pivotT_C5_N49_58.to_excel('c49_58_countN5.xlsx')
# pivotT_C6_N49_58.to_excel('c49_58_countN6.xlsx')
# pivotT_C7_N49_58.to_excel('c49_58_countN7.xlsx')
# pivotT_C8_N49_58.to_excel('c49_58_countN8.xlsx')
# pivotT_C9_N49_58.to_excel('c49_58_countN9.xlsx')
# pivotT_C10_N49_58.to_excel('c49_58_countN10.xlsx')

# # pivotT.to_excel('try.xlsx')
# pivotT_C.to_excel('c_countN.xlsx')
# pivotT_NC.to_excel('nc_countN.xlsx')

# pivotT_C1.to_excel('c_countN1.xlsx')
# pivotT_NC1.to_excel('nc_countN1.xlsx')

# pivotT_C2.to_excel('c_countN2.xlsx')
# pivotT_NC2.to_excel('nc_countN2.xlsx')

# pivotT_C3.to_excel('c_countN3.xlsx')
# pivotT_NC3.to_excel('nc_countN3.xlsx')

# pivotT_C4.to_excel('c_countN4.xlsx')
# pivotT_NC4.to_excel('nc_countN4.xlsx')

# pivotT_C5.to_excel('c_countN5.xlsx')
# pivotT_NC5.to_excel('nc_countN5.xlsx')

# pivotT_C6.to_excel('c_countN6.xlsx')
# pivotT_NC6.to_excel('nc_countN6.xlsx')

# pivotT_C7.to_excel('c_countN7.xlsx')
# pivotT_NC7.to_excel('nc_countN7.xlsx')

# pivotT_C8.to_excel('c_countN8.xlsx')
# pivotT_NC8.to_excel('nc_countN8.xlsx')

# pivotT_C9.to_excel('c_countN9.xlsx')
# pivotT_NC9.to_excel('nc_countN9.xlsx')

# pivotT_C10.to_excel('c_countN10.xlsx')
# pivotT_NC10.to_excel('nc_countN10.xlsx')
# pivotT_C2.to_excel('try2.xlsx')
#%%=============================================================================
# analysis
# =============================================================================


# (1) see count number for different winsize
color = 'orangered'
color = 'lime'

countNumber = stimuliInfo_toMerge_06_C['count_number'].value_counts()
countNumber=countNumber.sort_index()
ax = countNumber.plot(kind = 'bar', title = 'distribution No. of disc in crowdingzone ellipse actual size', color = color, alpha = 0.9)
ax.set_xlabel('number of disks fall in crowding zone')
ax.set_ylabel('frequency')
ax.set_yticks(np.arange(0, 13, step=1))
# plt.savefig('Distribution ellipse actual size nc ')

N = 15
countNumber = stimuliInfo_toMerge_06_NC['count_number%s' %(N)].value_counts()
countNumber=countNumber.sort_index()
# plt.figure(figsize = (10,6))
ax = countNumber.plot(kind = 'bar', title = 'distribution No. of disc in crowdingzone ellipseSize %s' %(N), color = color, alpha = 0.9)
ax.set_xlabel('number of disks fall in crowding zone')
ax.set_ylabel('frequency')
ax.set_yticks(np.arange(0, 13, step = 1))
plt.savefig('Distribution ellipse size%s c' %(N))

# #plots
# # final_df_C_t1 = final_df_C.groupby(['count_number'], as_index = False).mean()
# # final_df_C_t2 = final_df_C.groupby(['N_disk'], as_index = False).mean()

# # estimation against number of disks in crowding zone under each numerosity
# totalC_57=totalC[(totalC.N_disk == 57)]
# # final_df_C_t.to_excel('try.xlsx')
# # totalC_57 = totalC_57.groupby(['participant_N']).mean()
# fig, ax2 = plt.subplots()
# ax2 = sns.scatterplot(x='count_number', y = 'deviation_score' , data = totalC_57)

# max_x=int(final_df_C_t['count_number'].max())
# min_x=int(final_df_C_t['count_number'].min())
# max_y =int(final_df_C_t['key_resp_3.keys'].max())
# min_y =int(final_df_C_t['key_resp_3.keys'].min())
# ax2.set_xticks(list(range(min_x, max_x+1,1)))
# ax2.set_yticks(list(range(min_y, max_y+1,1)))
# ax2.set_xlabel('numbers in crowding zone')
# ax2.set_ylabel('estimation')
# fig.set_size_inches(11.7, 8.27)



# ax2 = sns.lineplot(x='count_number',y = 'key_resp_3.keys', data = final_df_C_t, color = 'k')
# ax2 = sns.scatterplot(x='count_number',y = 'key_resp_3.keys', data = final_df_C_t, color = 'k')


# ax2.set_ylim((0,70))
# ax2.set_yticks(list(range(0,70,5)))

# %%=============================================================================
# scaterplot file preperation
# =============================================================================

#winsize0.6 crowding
writer06 = pd.ExcelWriter('../totalC_N49_53_scaterdata.xlsx', engine = 'xlsxwriter')

totalC_N49_53_scaterdata    = totalC_N49_53[['count_number',   'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata1   = totalC_N49_53[['count_number1',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata2   = totalC_N49_53[['count_number2',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata3   = totalC_N49_53[['count_number3',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata4   = totalC_N49_53[['count_number4',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata5   = totalC_N49_53[['count_number5',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata6   = totalC_N49_53[['count_number6',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata7   = totalC_N49_53[['count_number7',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata8   = totalC_N49_53[['count_number8',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata9   = totalC_N49_53[['count_number9',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata10  = totalC_N49_53[['count_number10', 'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata11  = totalC_N49_53[['count_number11',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata12  = totalC_N49_53[['count_number12',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata13  = totalC_N49_53[['count_number13',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata14  = totalC_N49_53[['count_number14',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata15  = totalC_N49_53[['count_number15',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata16  = totalC_N49_53[['count_number16',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata17  = totalC_N49_53[['count_number17',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata18  = totalC_N49_53[['count_number18',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata19  = totalC_N49_53[['count_number19',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata20  = totalC_N49_53[['count_number20', 'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata21  = totalC_N49_53[['count_number21',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata22  = totalC_N49_53[['count_number22',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata23  = totalC_N49_53[['count_number23',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata24  = totalC_N49_53[['count_number24',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata25  = totalC_N49_53[['count_number25',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata26  = totalC_N49_53[['count_number26',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata27  = totalC_N49_53[['count_number27',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata28  = totalC_N49_53[['count_number28',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata29  = totalC_N49_53[['count_number29',  'participant_N', 'deviation_score']]
totalC_N49_53_scaterdata30  = totalC_N49_53[['count_number30', 'participant_N', 'deviation_score']]

totalC_N49_53_scaterdata.groupby   (['participant_N','count_number']).mean().to_excel   (writer06, sheet_name =  'actualSize0.25_0.1')
totalC_N49_53_scaterdata1.groupby  (['participant_N','count_number1']).mean().to_excel  (writer06, sheet_name =  '110%0.275_0.11')
totalC_N49_53_scaterdata2.groupby  (['participant_N','count_number2']).mean().to_excel  (writer06, sheet_name =  '120%0.3_0.12')
totalC_N49_53_scaterdata3.groupby  (['participant_N','count_number3']).mean().to_excel  (writer06, sheet_name =  '130%0.325_0.13')
totalC_N49_53_scaterdata4.groupby  (['participant_N','count_number4']).mean().to_excel  (writer06, sheet_name =  '140%')
totalC_N49_53_scaterdata5.groupby  (['participant_N','count_number5']).mean().to_excel  (writer06, sheet_name =  '150%')
totalC_N49_53_scaterdata6.groupby  (['participant_N','count_number6']).mean().to_excel  (writer06, sheet_name =  '160%')
totalC_N49_53_scaterdata7.groupby  (['participant_N','count_number7']).mean().to_excel  (writer06, sheet_name =  '170%')
totalC_N49_53_scaterdata8.groupby  (['participant_N','count_number8']).mean().to_excel  (writer06, sheet_name =  '180%')
totalC_N49_53_scaterdata9.groupby  (['participant_N','count_number9']).mean().to_excel  (writer06, sheet_name =  '190%')
totalC_N49_53_scaterdata10.groupby (['participant_N','count_number10']).mean().to_excel (writer06, sheet_name =  '200%')
totalC_N49_53_scaterdata11.groupby (['participant_N','count_number11']).mean().to_excel (writer06, sheet_name =  '210%')
totalC_N49_53_scaterdata12.groupby (['participant_N','count_number12']).mean().to_excel (writer06, sheet_name =  '220%')
totalC_N49_53_scaterdata13.groupby (['participant_N','count_number13']).mean().to_excel (writer06, sheet_name =  '230%')
totalC_N49_53_scaterdata14.groupby (['participant_N','count_number14']).mean().to_excel (writer06, sheet_name =  '240%')
totalC_N49_53_scaterdata15.groupby (['participant_N','count_number15']).mean().to_excel (writer06, sheet_name =  '250%')
totalC_N49_53_scaterdata16.groupby (['participant_N','count_number16']).mean().to_excel (writer06, sheet_name =  '260%')
totalC_N49_53_scaterdata17.groupby (['participant_N','count_number17']).mean().to_excel (writer06, sheet_name =  '270%')
totalC_N49_53_scaterdata18.groupby (['participant_N','count_number18']).mean().to_excel (writer06, sheet_name =  '280%')
totalC_N49_53_scaterdata19.groupby (['participant_N','count_number19']).mean().to_excel (writer06, sheet_name =  '290%')
totalC_N49_53_scaterdata20.groupby (['participant_N','count_number20']).mean().to_excel (writer06, sheet_name =  '300%')
totalC_N49_53_scaterdata21.groupby (['participant_N','count_number21']).mean().to_excel (writer06, sheet_name =  '310%')
totalC_N49_53_scaterdata22.groupby (['participant_N','count_number22']).mean().to_excel (writer06, sheet_name =  '320%')
totalC_N49_53_scaterdata23.groupby (['participant_N','count_number23']).mean().to_excel (writer06, sheet_name =  '330%')
totalC_N49_53_scaterdata24.groupby (['participant_N','count_number24']).mean().to_excel (writer06, sheet_name =  '340%')
totalC_N49_53_scaterdata25.groupby (['participant_N','count_number25']).mean().to_excel (writer06, sheet_name =  '350%')
totalC_N49_53_scaterdata26.groupby (['participant_N','count_number26']).mean().to_excel (writer06, sheet_name =  '360%')
totalC_N49_53_scaterdata27.groupby (['participant_N','count_number27']).mean().to_excel (writer06, sheet_name =  '370%')
totalC_N49_53_scaterdata28.groupby (['participant_N','count_number28']).mean().to_excel (writer06, sheet_name =  '380%')
totalC_N49_53_scaterdata29.groupby (['participant_N','count_number29']).mean().to_excel (writer06, sheet_name =  '390%')
totalC_N49_53_scaterdata30.groupby (['participant_N','count_number30']).mean().to_excel (writer06, sheet_name =  '400%')
writer06.save()

#winsize0.6 no-crowding
writer06_nc = pd.ExcelWriter('../totalNC_N49_53_scaterdata.xlsx', engine = 'xlsxwriter')

totalNC_N49_53_scaterdata    = totalNC_N49_53[['count_number',   'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata1   = totalNC_N49_53[['count_number1',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata2   = totalNC_N49_53[['count_number2',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata3   = totalNC_N49_53[['count_number3',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata4   = totalNC_N49_53[['count_number4',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata5   = totalNC_N49_53[['count_number5',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata6   = totalNC_N49_53[['count_number6',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata7   = totalNC_N49_53[['count_number7',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata8   = totalNC_N49_53[['count_number8',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata9   = totalNC_N49_53[['count_number9',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata10  = totalNC_N49_53[['count_number10', 'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata11  = totalNC_N49_53[['count_number11',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata12  = totalNC_N49_53[['count_number12',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata13  = totalNC_N49_53[['count_number13',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata14  = totalNC_N49_53[['count_number14',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata15  = totalNC_N49_53[['count_number15',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata16  = totalNC_N49_53[['count_number16',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata17  = totalNC_N49_53[['count_number17',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata18  = totalNC_N49_53[['count_number18',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata19  = totalNC_N49_53[['count_number19',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata20  = totalNC_N49_53[['count_number20', 'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata21  = totalNC_N49_53[['count_number21',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata22  = totalNC_N49_53[['count_number22',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata23  = totalNC_N49_53[['count_number23',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata24  = totalNC_N49_53[['count_number24',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata25  = totalNC_N49_53[['count_number25',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata26  = totalNC_N49_53[['count_number26',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata27  = totalNC_N49_53[['count_number27',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata28  = totalNC_N49_53[['count_number28',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata29  = totalNC_N49_53[['count_number29',  'participant_N', 'deviation_score']]
totalNC_N49_53_scaterdata30  = totalNC_N49_53[['count_number30', 'participant_N', 'deviation_score']]

totalNC_N49_53_scaterdata.groupby   (['participant_N','count_number']).mean().to_excel   (writer06_nc, sheet_name =  'actualSize')
totalNC_N49_53_scaterdata1.groupby  (['participant_N','count_number1']).mean().to_excel  (writer06_nc, sheet_name =  '110%')
totalNC_N49_53_scaterdata2.groupby  (['participant_N','count_number2']).mean().to_excel  (writer06_nc, sheet_name =  '120%')
totalNC_N49_53_scaterdata3.groupby  (['participant_N','count_number3']).mean().to_excel  (writer06_nc, sheet_name =  '130%')
totalNC_N49_53_scaterdata4.groupby  (['participant_N','count_number4']).mean().to_excel  (writer06_nc, sheet_name =  '140%')
totalNC_N49_53_scaterdata5.groupby  (['participant_N','count_number5']).mean().to_excel  (writer06_nc, sheet_name =  '150%')
totalNC_N49_53_scaterdata6.groupby  (['participant_N','count_number6']).mean().to_excel  (writer06_nc, sheet_name =  '160%')
totalNC_N49_53_scaterdata7.groupby  (['participant_N','count_number7']).mean().to_excel  (writer06_nc, sheet_name =  '170%')
totalNC_N49_53_scaterdata8.groupby  (['participant_N','count_number8']).mean().to_excel  (writer06_nc, sheet_name =  '180%')
totalNC_N49_53_scaterdata9.groupby  (['participant_N','count_number9']).mean().to_excel  (writer06_nc, sheet_name =  '190%')
totalNC_N49_53_scaterdata10.groupby (['participant_N','count_number10']).mean().to_excel (writer06_nc, sheet_name =  '200%')
totalNC_N49_53_scaterdata11.groupby (['participant_N','count_number11']).mean().to_excel (writer06_nc, sheet_name =  '210%')
totalNC_N49_53_scaterdata12.groupby (['participant_N','count_number12']).mean().to_excel (writer06_nc, sheet_name =  '220%')
totalNC_N49_53_scaterdata13.groupby (['participant_N','count_number13']).mean().to_excel (writer06_nc, sheet_name =  '230%')
totalNC_N49_53_scaterdata14.groupby (['participant_N','count_number14']).mean().to_excel (writer06_nc, sheet_name =  '240%')
totalNC_N49_53_scaterdata15.groupby (['participant_N','count_number15']).mean().to_excel (writer06_nc, sheet_name =  '250%')
totalNC_N49_53_scaterdata16.groupby (['participant_N','count_number16']).mean().to_excel (writer06_nc, sheet_name =  '260%')
totalNC_N49_53_scaterdata17.groupby (['participant_N','count_number17']).mean().to_excel (writer06_nc, sheet_name =  '270%')
totalNC_N49_53_scaterdata18.groupby (['participant_N','count_number18']).mean().to_excel (writer06_nc, sheet_name =  '280%')
totalNC_N49_53_scaterdata19.groupby (['participant_N','count_number19']).mean().to_excel (writer06_nc, sheet_name =  '290%')
totalNC_N49_53_scaterdata20.groupby (['participant_N','count_number20']).mean().to_excel (writer06_nc, sheet_name =  '300%')
totalNC_N49_53_scaterdata21.groupby (['participant_N','count_number21']).mean().to_excel (writer06_nc, sheet_name =  '310%')
totalNC_N49_53_scaterdata22.groupby (['participant_N','count_number22']).mean().to_excel (writer06_nc, sheet_name =  '320%')
totalNC_N49_53_scaterdata23.groupby (['participant_N','count_number23']).mean().to_excel (writer06_nc, sheet_name =  '330%')
totalNC_N49_53_scaterdata24.groupby (['participant_N','count_number24']).mean().to_excel (writer06_nc, sheet_name =  '340%')
totalNC_N49_53_scaterdata25.groupby (['participant_N','count_number25']).mean().to_excel (writer06_nc, sheet_name =  '350%')
totalNC_N49_53_scaterdata26.groupby (['participant_N','count_number26']).mean().to_excel (writer06_nc, sheet_name =  '360%')
totalNC_N49_53_scaterdata27.groupby (['participant_N','count_number27']).mean().to_excel (writer06_nc, sheet_name =  '370%')
totalNC_N49_53_scaterdata28.groupby (['participant_N','count_number28']).mean().to_excel (writer06_nc, sheet_name =  '380%')
totalNC_N49_53_scaterdata29.groupby (['participant_N','count_number29']).mean().to_excel (writer06_nc, sheet_name =  '390%')
totalNC_N49_53_scaterdata30.groupby (['participant_N','count_number30']).mean().to_excel (writer06_nc, sheet_name =  '400%')
writer06_nc.save()

#winsize0.7 crowding
writer07 = pd.ExcelWriter('../totalC_N54_58_scaterdata.xlsx', engine = 'xlsxwriter')

totalC_N54_58_scaterdata   = totalC_N54_58[['count_number',   'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata1  = totalC_N54_58[['count_number1',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata2  = totalC_N54_58[['count_number2',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata3  = totalC_N54_58[['count_number3',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata4  = totalC_N54_58[['count_number4',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata5  = totalC_N54_58[['count_number5',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata6  = totalC_N54_58[['count_number6',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata7  = totalC_N54_58[['count_number7',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata8  = totalC_N54_58[['count_number8',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata9  = totalC_N54_58[['count_number9',  'participant_N', 'deviation_score']]
totalC_N54_58_scaterdata10 = totalC_N54_58[['count_number10', 'participant_N', 'deviation_score']]


totalC_N54_58_scaterdata.groupby  (['participant_N','count_number']).mean().to_excel  (writer07, sheet_name = 'actualSize')
totalC_N54_58_scaterdata1.groupby (['participant_N','count_number1']).mean().to_excel (writer07, sheet_name = '110%')
totalC_N54_58_scaterdata2.groupby (['participant_N','count_number2']).mean().to_excel (writer07, sheet_name = '120%')
totalC_N54_58_scaterdata3.groupby (['participant_N','count_number3']).mean().to_excel (writer07, sheet_name = '130%')
totalC_N54_58_scaterdata4.groupby (['participant_N','count_number4']).mean().to_excel (writer07, sheet_name = '140%')
totalC_N54_58_scaterdata5.groupby (['participant_N','count_number5']).mean().to_excel (writer07, sheet_name = '150%')
totalC_N54_58_scaterdata6.groupby (['participant_N','count_number6']).mean().to_excel (writer07, sheet_name = '160%')
totalC_N54_58_scaterdata7.groupby (['participant_N','count_number7']).mean().to_excel (writer07, sheet_name = '170%')
totalC_N54_58_scaterdata8.groupby (['participant_N','count_number8']).mean().to_excel (writer07, sheet_name = '180%')
totalC_N54_58_scaterdata9.groupby (['participant_N','count_number9']).mean().to_excel (writer07, sheet_name = '190%')
totalC_N54_58_scaterdata10.groupby(['participant_N','count_number10']).mean().to_excel(writer07, sheet_name = '200%')
# writer07.save()

#winsize0.7 no-crowding
writer07_nc = pd.ExcelWriter('../totalNC_N54_58_scaterdata.xlsx', engine = 'xlsxwriter')

totalNC_N54_58_scaterdata   = totalNC_N54_58[['count_number',   'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata1  = totalNC_N54_58[['count_number1',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata2  = totalNC_N54_58[['count_number2',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata3  = totalNC_N54_58[['count_number3',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata4  = totalNC_N54_58[['count_number4',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata5  = totalNC_N54_58[['count_number5',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata6  = totalNC_N54_58[['count_number6',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata7  = totalNC_N54_58[['count_number7',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata8  = totalNC_N54_58[['count_number8',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata9  = totalNC_N54_58[['count_number9',  'participant_N', 'deviation_score']]
totalNC_N54_58_scaterdata10 = totalNC_N54_58[['count_number10', 'participant_N', 'deviation_score']]


totalNC_N54_58_scaterdata.groupby  (['participant_N','count_number']).mean().to_excel  (writer07_nc, sheet_name = 'actualSize')
totalNC_N54_58_scaterdata1.groupby (['participant_N','count_number1']).mean().to_excel (writer07_nc, sheet_name = '110%')
totalNC_N54_58_scaterdata2.groupby (['participant_N','count_number2']).mean().to_excel (writer07_nc, sheet_name = '120%')
totalNC_N54_58_scaterdata3.groupby (['participant_N','count_number3']).mean().to_excel (writer07_nc, sheet_name = '130%')
totalNC_N54_58_scaterdata4.groupby (['participant_N','count_number4']).mean().to_excel (writer07_nc, sheet_name = '140%')
totalNC_N54_58_scaterdata5.groupby (['participant_N','count_number5']).mean().to_excel (writer07_nc, sheet_name = '150%')
totalNC_N54_58_scaterdata6.groupby (['participant_N','count_number6']).mean().to_excel (writer07_nc, sheet_name = '160%')
totalNC_N54_58_scaterdata7.groupby (['participant_N','count_number7']).mean().to_excel (writer07_nc, sheet_name = '170%')
totalNC_N54_58_scaterdata8.groupby (['participant_N','count_number8']).mean().to_excel (writer07_nc, sheet_name = '180%')
totalNC_N54_58_scaterdata9.groupby (['participant_N','count_number9']).mean().to_excel (writer07_nc, sheet_name = '190%')
totalNC_N54_58_scaterdata10.groupby(['participant_N','count_number10']).mean().to_excel(writer07_nc, sheet_name = '200%')
# writer07_nc.save()