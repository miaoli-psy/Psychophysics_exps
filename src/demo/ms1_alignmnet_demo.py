# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-04-05 23:12
IDE: PyCharm
Introduction: ms1 figure 2 - alignment value display demo
"""
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

from src.analysis.exp1_raidal_displays_analysis2 import get_angle_range, get_angle_range_no_overlap
from src.constants.sample_display_posi import SamplePosiExp1
from src.point.polar_point import get_polar_coordinates
# https://www.debug8.com/python/t_58112.html

c_posis = SamplePosiExp1.exp1_c

# polar positions
c_polar = get_polar_coordinates(c_posis, sort = False)
# match Cartesian with polar
posi_dict = dict()
for i in range(0, len(c_posis)):
    posi_dict[c_polar[i]] = c_posis[i]

c_polar_sort = get_polar_coordinates(c_posis, sort = True)

# subset_posi = []
# for i in range(0, 10):
#     subset_posi.append(posi_dict[c_polar_sort[i]])
# c_polar_sort = get_polar_coordinates(subset_posi, sort = True)
#
# c_polar_sort = c_polar_sort[-3:]

# some parameters, started and ended where
ini_start_angle = c_polar_sort[0][0]
angle_size = 6
ini_end_angle = ini_start_angle + angle_size
# get the ranges
my_range_overlap = get_angle_range(c_polar_sort, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)

# get thetas
my_range = get_angle_range_no_overlap(my_range_overlap, start_n = 0)
# print(my_range)

start_thetas = [range[0] for range in my_range]
start_thetas = [math.radians(theta) for theta in start_thetas]
start_thetas = [theta+math.radians(6)/2 for theta in start_thetas]
# start_thetas = start_thetas[:10]

#%% plot starts here
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize = (8, 6))
# ini discs
for polar_posi in c_polar_sort:
    ax.plot(math.radians(polar_posi[0]), polar_posi[1], "ko", markersize = 2)
# bars
data = np.full((len(start_thetas),), 500)
theta = np.array(start_thetas)
width = np.full((len(start_thetas),), math.radians(6))

ax.bar(theta, data, alpha=0.5, width=width)
ax.set_rlim(0, 500)
ax.grid(False)
ax.set_yticklabels([])
ax.set_frame_on(False)
ax.axes.get_xaxis().set_visible(False)
plt.show()

fig.savefig('try_beam3.svg', bbox_inches = 'tight', pad_inches = 0)