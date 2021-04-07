# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-04-05 23:12
IDE: PyCharm
Introduction: ms1 figure 2 - alignment value display demo
"""
import math
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.exp1_raidal_displays_analysis2 import get_angle_range, get_angle_range_no_overlap
from src.constants.sample_display_posi import SamplePosiExp1
from src.point.polar_point import get_polar_coordinates
from typing import List, Tuple


def get_start_angle(posilist: List[Tuple[float]]):
    # get sorted polar posi
    c_polar_sort = get_polar_coordinates(posilist, sort = True)
    # get ranges with beam size of 6 deg
    my_range_overlap = get_angle_range(c_polar_sort, ini_start_angle = c_polar_sort[0][0],
                                       ini_end_angle = c_polar_sort[0][0] + 6)
    my_range = get_angle_range_no_overlap(my_range_overlap, start_n = 0)
    # start theta takes the first value of each range
    theta_list = [range[0] for range in my_range]
    # degree to radians
    theta_list = [math.radians(theta) for theta in theta_list]
    # align start line to the center of the discs
    theta_list = [theta + math.radians(6) / 2 for theta in theta_list]
    return theta_list


# # polar positions
# c_polar = get_polar_coordinates(c_posis, sort = False)
# # match Cartesian with polar
# posi_dict = dict()
# for i in range(0, len(c_posis)):
#     posi_dict[c_polar[i]] = c_posis[i]
# c_polar_sort = get_polar_coordinates(c_posis, sort = True)
#
# # some parameters, started and ended where
# ini_start_angle = c_polar_sort[0][0]
# angle_size = 6
# ini_end_angle = ini_start_angle + angle_size
# # get the ranges
# my_range_overlap = get_angle_range(c_polar_sort, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
#
# # get thetas
# my_range = get_angle_range_no_overlap(my_range_overlap, start_n = 0)
# # print(my_range)
#
# start_thetas = [range[0] for range in my_range]
# start_thetas = [math.radians(theta) for theta in start_thetas]
# start_thetas = [theta + math.radians(6) / 2 for theta in start_thetas]
# start_thetas = start_thetas[:10]

if __name__ == '__main__':
    # TODO crowding demo or no-crowding demo
    crowding = 1
    savefig = True
    # input positions
    if crowding == 1:
        posis = SamplePosiExp1.exp1_c
    elif crowding == 0:
        posis = SamplePosiExp1.exp1_nc
    # get start angle to draw
    start_thetas = get_start_angle(posis)
    # plot starts here
    fig, ax = plt.subplots(subplot_kw = {'projection': 'polar'}, figsize = (4, 3))
    # ini discs plot in polar coordinates
    for polar_posi in get_polar_coordinates(posis, sort = True):
        ax.plot(math.radians(polar_posi[0]), polar_posi[1], "ko", markersize = 2)
    # beams
    # data: how long the blue beam region
    data = np.full((len(start_thetas),), 500)
    # where each beam starts
    theta = np.array(start_thetas)
    # size of the beam = 6 deg
    width = np.full((len(start_thetas),), math.radians(6))
    # plot
    ax.bar(theta, data, alpha = 0.5, width = width)
    # set plot parameter
    ax.set_rlim(0, 500)
    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_frame_on(False)
    ax.axes.get_xaxis().set_visible(False)
    plt.show()
    if savefig:
        fig.savefig('try_beam.svg', bbox_inches = 'tight', pad_inches = 0)