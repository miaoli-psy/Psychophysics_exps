# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:41 2020
@author: Miao
ms1 figure 2e - a quarter of a sample crowding display
"""

from math import atan2, pi
from scipy.spatial import distance
# https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145014176
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def drawEllipse_crowding(e_posi, black_disc_posi, red_disc_posi, crowding_posi, ka, kb, ellipseColor_r = 'royalblue',
                         savefig = False):
    """
    crowding display: show discs that falls into others crowding zones.
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0, 0))
        eccentricities.append(eccentricities0)
    # radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0 = angle_rad0 * 180 / pi
        angle_deg.append(angle_deg0)

    # crowding disc
    eccentricities_c = []
    for i in range(len(crowding_posi)):
        eccentricities0 = distance.euclidean(crowding_posi[i], (0, 0))
        eccentricities_c.append(eccentricities0)
    angle_deg_c = []
    for ang in range(len(crowding_posi)):
        angle_rad0 = atan2(crowding_posi[ang][1], crowding_posi[ang][0])
        angle_deg0 = angle_rad0 * 180 / pi
        angle_deg_c.append(angle_deg0)
    my_e = [Ellipse(xy = crowding_posi[j], width = eccentricities_c[j] * ka * 2, height = eccentricities_c[j] * kb * 2,
                    angle = angle_deg_c[j], linestyle = "--")
            for j in range(len(crowding_posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (8, 6))
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_edgecolor(ellipseColor_r)
        e.set_fill(False)

    # show the discs on the ellipses-flower
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4, alpha = 0.3)
    for dot in black_disc_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4)
    for dot in red_disc_posi:
        plt.plot(dot[0], dot[1], color = 'orangered', marker = 'o', markersize = 4)

    # add concentric circles
    for posi in black_disc_posi:
        ax.add_patch(
                plt.Circle((0, 0), distance.euclidean(posi, (0, 0)), alpha = 0.5, linestyle = "--", fill = False))
    # fixation
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 10)

    # x, y limit
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])

    # 边框不可见
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # 坐标不可见
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.patch.set_facecolor('lightgray')
    plt.show()
    if savefig:
        fig.savefig('try.png', bbox_inches = 'tight', pad_inches = 0)


if __name__ == '__main__':
    exp1_c_demo = [(20.0, -170.0), (230.0, -100.0), (300.0, -20.0), (120.0, -210.0), (100.0, -80.0), (210.0, -10.0),
                   (170.0, -100.0), (50.0, -100.0), (250.0, -180.0), (150.0, -50.0), (80.0, -60.0), (100.0, -10.0),
                   (90.0, -130.0), (20.0, -130.0), (100.0, -170.0)]
    central_disc = [(100, -170.0), (80.0, -60.0), (300.0, -20.0), (20.0, -170.0)]
    extra_disc = [(90.0, -130.0), (120, -210), (100.0, -80.0), (210.0, -10.0), (20.0, -130.0)]
    drawEllipse_crowding(exp1_c_demo, central_disc, extra_disc, central_disc, ka = 0.35, kb = 0.12,
                         ellipseColor_r = 'orangered', savefig = True)