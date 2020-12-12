# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:56:42 2020

@author: Miao
"""
import pandas as pd
from shapely.geometry import LineString
from shapely import affinity
import matplotlib.pyplot as plt
from scipy.spatial import distance
# =============================================================================
# read stimuli display
# =============================================================================
path = "../displays/"
stimuli_df = pd.read_excel(path+"update_stim_info_full.xlsx")

# check df coloum names
c_names = stimuli_df.columns.to_list()

# =============================================================================
# theta = 0 deg (a line)
# =============================================================================

try_posi = [(-90.0, -80.0), (20.0, 100.0), (-80.0, 80.0), (-140.0, -60.0), (100.0, -100.0), (-140.0, 40.0), (140.0, -20.0), (-120.0, -10.0), (110.0, 40.0), (-120.0, 80.0), (-20.0, -100.0), (100.0, 70.0), (-70.0, 110.0), (-60.0, -100.0), (150.0, 10.0), (10.0, -110.0), (-30.0, 100.0), (50.0, -110.0), (110.0, -60.0), (50.0, 100.0), (80.0, 90.0)]

#find the coordinate that is the furthest to the center

def find_furthest_distance(inputposilist):
    """
    inputposilist:all postions for one display
    output: the distance between the center and the furthest disc position
    """
    distances = [distance.euclidean((0,0), d) for d in inputposilist]
    return max(distances)

def get_started_line(inputposilist):
    """
    inputposilist:all positions for one displays
    output: the started LineString
    """
    linetip = find_furthest_distance(inputposilist)
    return LineString([(0, 0), (0,linetip)])


start_line = get_started_line(try_posi)
plt.plot(*start_line.xy)







# =============================================================================
# theta = 12 deg (around 11.42 deg, defined by the size of crowding zones)
# =============================================================================



# rotated_a = affinity.rotate(line, 20)
# rotated_b = affinity.rotate(geom = b, angle = -20, origin=((0,0)), use_radians=False)) #negative anlge: clockwise