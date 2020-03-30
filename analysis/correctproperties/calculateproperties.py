# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 01:56:40 2020

@author: Miao
"""
import ast
import pandas as pd
import numpy as np
from math import pi
from scipy.spatial import distance, ConvexHull
from itertools import combinations

def get_display_properties(displayPositions):
    '''75 unit = 30 cm
        1 unit = 0.4cm
        1D in cm
        density2 in items/deg2'''
    displayPositions_array = np.asarray(displayPositions)
    convexHull_t           = ConvexHull(displayPositions_array)
    convexHull_perimeter   = round((convexHull_t.area/10)*0.4,2)
    occupancyArea          = round((convexHull_t.volume/100)*(0.4**2),2)
    
    ListD = []
    for p in displayPositions:
        eD = (distance.euclidean(p,(0,0))/10)
        ListD.append(eD)

    averageE             = round(sum(ListD)/len(displayPositions) * 0.4,2)
    distances            = [(distance.euclidean(p1,p2)/10*0.4) for p1, p2 in combinations(displayPositions,2)]
    avg_spacing_c        = round(sum(distances)/len(distances)*0.4,2)
    
    aggregateSurface     = round(len(displayPositions)*pi*(0.25**2),4) #0.25 visual degree as radius
    density              = round(aggregateSurface/occupancyArea, 5)
    density_itemsperdeg2 = round(len(displayPositions)/occupancyArea,5)
    
    return convexHull_perimeter, occupancyArea, averageE, avg_spacing_c, aggregateSurface, density, density_itemsperdeg2


def strtolist(posi_list_str):
    posi_list = []
    for i in posi_list_str:
        i = ast.literal_eval(i) # megic! remore ' ' of the str
        posi_list.append(i)
    return posi_list

# read selected display
selecteddispalys = pd.read_excel('cleanedTotalData_fullinfo.xlsx')

# str - list
selecteddispalys['positions'] = strtolist(selecteddispalys['positions_list'].tolist())

# correct density2
selecteddispalys['properties']           = selecteddispalys['positions'].map(get_display_properties)
selecteddispalys['convexHull']           = selecteddispalys['properties'].map(lambda x: x[0])
selecteddispalys['occupancyArea']        = selecteddispalys['properties'].map(lambda x: x[1])
selecteddispalys['averageE']             = selecteddispalys['properties'].map(lambda x: x[2])
selecteddispalys['avg_spacing']          = selecteddispalys['properties'].map(lambda x: x[3])
selecteddispalys['aggregateSurface']     = selecteddispalys['properties'].map(lambda x: x[4])
selecteddispalys['density']              = selecteddispalys['properties'].map(lambda x: x[5])
selecteddispalys['density_itemsperdeg2'] = selecteddispalys['properties'].map(lambda x: x[6])


# write to excel 
with pd.ExcelWriter('try.xlsx') as writer:
    selecteddispalys.to_excel(writer)