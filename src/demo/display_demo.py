# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:41 2020

@author: Miao
"""

# =============================================================================
# import modules
# =============================================================================
from math import atan2, pi
from scipy.spatial import distance
# https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145014176
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from src.constants.sample_display_posi import SamplePosiExp1


# =============================================================================
# draw ellipse
# =============================================================================
def drawEllipse_full(e_posi, extra_posi, ka, kb, ellipseColor_r = 'orangered', ellipseColor_t = 'royalblue'):
    """
    This function allows to draw more than one ellipse. The parameter is
    a list of coordinate (must contain at least two coordinates)
    The radial and tangential ellipses for the same coordinates are drawn.
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
    my_e = [Ellipse(xy = e_posi[j], width = eccentricities[j] * ka * 2, height = eccentricities[j] * kb * 2,
                    angle = angle_deg[j])
            for j in range(len(e_posi))]

    # tangential
    angle_deg2 = []
    for ang in range(len(e_posi)):
        angle_rad0_2 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0_2 = angle_rad0_2 * 180 / pi + 90
        angle_deg2.append(angle_deg0_2)
    my_e2 = [Ellipse(xy = e_posi[j], width = eccentricities[j] * ka * 2, height = eccentricities[j] * kb * 2,
                     angle = angle_deg[j] + 90)
             for j in range(len(e_posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(0.5)
        e.set_facecolor(ellipseColor_r)
    for e2 in my_e2:
        ax.add_artist(e2)
        e2.set_clip_box(ax.bbox)
        e2.set_alpha(0.5)
        e2.set_facecolor(ellipseColor_t)

    # show the discs on the ellipses-flower
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)
    # plt.show()
    for dot1 in extra_posi:
        plt.plot(dot1[0], dot1[1], color = 'r', marker = 'o', markersize = 2)
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)
    # plt.show()
    # ax.set_xlim([-800, 800])
    # ax.set_ylim([-500, 500])
    ax.set_xlim([-400, 400])
    ax.set_ylim([-260, 260])
    # ax.set_title('wS_%s_eS_%s_%s_E.png' %(newWindowSize,ka,kb))

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

    fig.savefig('efull%s.svg' % (str(e_posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)


def drawEllipses(posi, ka, kb, ellipseColor, ellipsetransp = 0.5):
    eccentricities2 = []
    for i in range(len(posi)):
        eccentricities0 = distance.euclidean(posi[i], (0, 0))
        eccentricities2.append(eccentricities0)
    # radial
    angle_deg3 = []
    for ang in range(len(posi)):
        angle_rad0s = atan2(posi[ang][1], posi[ang][0])
        angle_deg0s = angle_rad0s * 180 / pi
        angle_deg3.append(angle_deg0s)

    my_e = [Ellipse(xy = posi[j], width = eccentricities2[j] * ka * 2, height = eccentricities2[j] * kb * 2,
                    angle = angle_deg3[j])
            for j in range(len(posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))

    for e in my_e:
        ax.add_artist(e)
        # random color?
        e.set_clip_box(ax.bbox)
        # e.set_alpha(np.random.rand())
        e.set_alpha(ellipsetransp)
        # e.set_facecolor(np.random.rand(3))
        # change face color here
        if ellipseColor == 'orangered':
            e.set_facecolor('orangered')  # 'royalblue'
        else:
            e.set_facecolor(ellipseColor)
        # e.set_facecolor('royalblue')

    # plot central discs
    for dot in posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)

    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
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
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()
    fig.savefig('e%s.svg' % (str(posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)


def draw_disc_only(e_posi):
    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (4, 3))
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 2)
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 4)

    # set x,y lim
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
    # set background color
    ax.patch.set_facecolor('lightgray')
    plt.show()

    fig.savefig('disc%s.svg' % (str(e_posi)[0:15]), bbox_inches = 'tight', pad_inches = 0)


if __name__ == '__main__':
    # exp 1 display sample
    draw_disc_only(SamplePosiExp1.exp1_c)
    draw_disc_only(SamplePosiExp1.exp1_nc)
    # exp 1 display with ellipses no-crowding
    drawEllipses(posi = SamplePosiExp1.exp1_nc, ka = 0.25, kb = 0.1, ellipseColor = 'white', ellipsetransp = 0.5)
    # exp1 display with ellipses crowding
    drawEllipses(posi = SamplePosiExp1.exp1_c, ka = 0.1, kb = 0.25, ellipseColor = 'white', ellipsetransp = 0.5)

    # drawEllipse_full(centerposi, [], 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_c, 0.25, 0.1)
    # drawEllipse_crowding(centerposi, [], 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_nc, 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_c_50p, 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_nc_50p, 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_c_0p, 0.25, 0.1)
    # drawEllipse_full(centerposi, extra_nc_0p, 0.25, 0.1)
    # drawEllipses(baseline,ellipseColor="white",ka = 0.14,kb = 0.14)
    # drawEllipses(exp1_c, 0.1, 0.25, ellipseColor = '2')
    # drawEllipses(exp1_nc, 0.25, 0.1, ellipseColor = '2')

    # drawEllipse_full(extra_nc,centerposi , 0.25, 0.1)
    #
    # draw_disc_only(exp1_nc)
    #
    # drawEllipses(posi = exp1_crowding, ka=0.1, kb=0.25, ellipseColor = 'royalblue', ellipsetransp = 0.5)

    # =============================================================================
    # exp2 - displays demo varing pairs
    # =============================================================================

    # drawEllipse_full(centralc_75_paris, extra_c_75_paris, 0.25,0.1)
    # drawEllipse_full(centralc_25_paris, extra_c_25_paris, 0.25,0.1)