# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 18:45:24 2020

@author: MiaoLi
"""
import pandas as pd
import ast,sys
from collections import OrderedDict
from shapely.geometry import Polygon, Point
sys.path.append('C:\\Users\\MiaoLi\\Desktop\\SCALab\\Programming\\crowdingnumerositygit\\GenerationAlgorithm\\VirtualEllipseFunc')
import m_defineEllipses
#%% =============================================================================
# import stimulus displays
# =============================================================================
stimuliInfo = pd.read_excel('../updated_stim_info_QsDensities.xlsx')
posi_lists_temp = stimuliInfo['positions'].tolist()

posi_list=[]
for i in posi_lists_temp:
    i = ast.literal_eval(i)# megic! remore ' ' of the str
    posi_list.append(i)

#%%=============================================================================
# inspect number of discs into others' crowding zones (increase major axis, keey minor axis the same)
# =============================================================================

# creat 10 empty lists, eg:list_count_in_crowdingZone1 = []
for i in range(1,11):
    locals()['list_count_in_crowdingZone'+str(i)] = []

for indexPosiList, display_posi in enumerate(posi_list):
    for i in range(1,11):
        locals()['ellipse'+str(i)] = []
    for posi in display_posi:
        e1  = m_defineEllipses.defineVirtualEllipses(posi, 0.275, 0.1)
        e2  = m_defineEllipses.defineVirtualEllipses(posi, 0.3, 0.1)
        e3  = m_defineEllipses.defineVirtualEllipses(posi, 0.325, 0.1)
        e4  = m_defineEllipses.defineVirtualEllipses(posi, 0.35, 0.1)
        e5  = m_defineEllipses.defineVirtualEllipses(posi, 0.375, 0.1)
        e6  = m_defineEllipses.defineVirtualEllipses(posi, 0.4, 0.1)
        e7  = m_defineEllipses.defineVirtualEllipses(posi, 0.425, 0.1)
        e8  = m_defineEllipses.defineVirtualEllipses(posi, 0.45, 0.1)
        e9  = m_defineEllipses.defineVirtualEllipses(posi, 0.475, 0.1)
        e10 = m_defineEllipses.defineVirtualEllipses(posi, 0.5, 0.1)

        ellipse1.append(e1) 
        ellipse2.append(e2) 
        ellipse3.append(e3) 
        ellipse4.append(e4) 
        ellipse5.append(e5) 
        ellipse6.append(e6) 
        ellipse7.append(e7) 
        ellipse8.append(e8) 
        ellipse9.append(e9) 
        ellipse10.append(e10)
    
    final_ellipse1  = list(OrderedDict.fromkeys(ellipse1))
    final_ellipse2  = list(OrderedDict.fromkeys(ellipse2))
    final_ellipse3  = list(OrderedDict.fromkeys(ellipse3))
    final_ellipse4  = list(OrderedDict.fromkeys(ellipse4))
    final_ellipse5  = list(OrderedDict.fromkeys(ellipse5))
    final_ellipse6  = list(OrderedDict.fromkeys(ellipse6))
    final_ellipse7  = list(OrderedDict.fromkeys(ellipse7))
    final_ellipse8  = list(OrderedDict.fromkeys(ellipse8))
    final_ellipse9  = list(OrderedDict.fromkeys(ellipse9))
    final_ellipse10 = list(OrderedDict.fromkeys(ellipse10))

    for i in range(1, 11):
        locals()['count_in_crowdingZone' + str(i)] = 0

    for i1, i2, i3, i4, i5, i6, i7, i8, i9, i10,\
         in zip(final_ellipse1,\
                final_ellipse2,\
                final_ellipse3,\
                final_ellipse4,\
                final_ellipse5,\
                final_ellipse6,\
                final_ellipse7,\
                final_ellipse8,\
                final_ellipse9,\
                final_ellipse10):
        ellipsePolygon1   = m_defineEllipses.ellipseToPolygon([i1])[0]
        ellipsePolygon2   = m_defineEllipses.ellipseToPolygon([i2])[0]
        ellipsePolygon3   = m_defineEllipses.ellipseToPolygon([i3])[0]
        ellipsePolygon4   = m_defineEllipses.ellipseToPolygon([i4])[0]
        ellipsePolygon5   = m_defineEllipses.ellipseToPolygon([i5])[0]
        ellipsePolygon6   = m_defineEllipses.ellipseToPolygon([i6])[0]
        ellipsePolygon7   = m_defineEllipses.ellipseToPolygon([i7])[0]
        ellipsePolygon8   = m_defineEllipses.ellipseToPolygon([i8])[0]
        ellipsePolygon9   = m_defineEllipses.ellipseToPolygon([i9])[0]
        ellipsePolygon10  = m_defineEllipses.ellipseToPolygon([i10])[0]

        epPolygon1   = Polygon(ellipsePolygon1)
        epPolygon2   = Polygon(ellipsePolygon2)
        epPolygon3   = Polygon(ellipsePolygon3)
        epPolygon4   = Polygon(ellipsePolygon4)
        epPolygon5   = Polygon(ellipsePolygon5)
        epPolygon6   = Polygon(ellipsePolygon6)
        epPolygon7   = Polygon(ellipsePolygon7)
        epPolygon8   = Polygon(ellipsePolygon8)
        epPolygon9   = Polygon(ellipsePolygon9)
        epPolygon10  = Polygon(ellipsePolygon10)

        for posi in display_posi:
            if epPolygon1.contains(Point(posi)) == True:
                count_in_crowdingZone1 += 1
            if epPolygon2.contains(Point(posi)) == True:
                count_in_crowdingZone2 += 1
            if epPolygon3.contains(Point(posi)) == True:
                count_in_crowdingZone3 += 1
            if epPolygon4.contains(Point(posi)) == True:
                count_in_crowdingZone4 += 1
            if epPolygon5.contains(Point(posi)) == True:
                count_in_crowdingZone5 += 1
            if epPolygon6.contains(Point(posi)) == True:
                count_in_crowdingZone6 += 1
            if epPolygon7.contains(Point(posi)) == True:
                count_in_crowdingZone7 += 1
            if epPolygon8.contains(Point(posi)) == True:
                count_in_crowdingZone8 += 1
            if epPolygon9.contains(Point(posi)) == True:
                count_in_crowdingZone9 += 1
            if epPolygon10.contains(Point(posi)) == True:
                count_in_crowdingZone10 += 1
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

stimuliInfo = stimuliInfo.assign(
        ncount_number1  = list_count_in_crowdingZone1,\
        ncount_number2  = list_count_in_crowdingZone2,\
        ncount_number3  = list_count_in_crowdingZone3,\
        ncount_number4  = list_count_in_crowdingZone4,\
        ncount_number5  = list_count_in_crowdingZone5,\
        ncount_number6  = list_count_in_crowdingZone6,\
        ncount_number7  = list_count_in_crowdingZone7,\
        ncount_number8  = list_count_in_crowdingZone8,\
        ncount_number9  = list_count_in_crowdingZone9,\
        ncount_number10 = list_count_in_crowdingZone10)

#%% =============================================================================
# merge data with stimuliInfo
# =============================================================================
totalData_new = pd.read_excel('../cleanedTotalData_fullinfo.xlsx')
to_drop = ['pk',
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

stimuliInfo['crowdingcons']     = stimuliInfo['crowdingcons'].astype(int)
stimuliInfo['winsize']          = stimuliInfo['winsize'].astype(float)
stimuliInfo['index_stimuliInfo']= stimuliInfo['index_stimuliInfo'].astype(str)
stimuliInfo['N_disk']           = stimuliInfo['N_disk'].astype(int)
stimuliInfo.to_excel('update_stim_info.xlsx')

#TODO: Check 2 df coloums that are to be merged
# for col in totalData_new.columns:
#     print(col)
# for col in updated_stim_info_df.columns:
#     print(col)
totalData_new = pd.merge(totalData_new,stimuliInfo, how = 'left', on = ['index_stimuliInfo', 'N_disk', 'crowdingcons','winsize'])






















