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

# =============================================================================
# positions
# =============================================================================
centerposi = [(140.0, -150.0), (60.0, 170.0), (260.0, -110.0), (-140.0, 120.0), (170.0, -40.0), (-180.0, -160.0),
              (-250.0, 160.0), (140.0, 20.0), (170.0, 180.0), (-260.0, 30.0), (-60.0, 80.0), (-60.0, 160.0),
              (240.0, 30.0), (0.0, -170.0), (-100.0, -20.0), (110.0, -50.0), (140.0, 100.0), (-140.0, -80.0),
              (290.0, 140.0), (50.0, -130.0), (-150.0, 0.0), (-300.0, -110.0), (-90.0, -150.0), (0.0, 110.0),
              (-80.0, -80.0), (70.0, -80.0), (-110.0, 40.0), (80.0, 60.0), (-140.0, 220.0), (80.0, -220.0),
              (0.0, -100.0), (60.0, 100.0), (0.0, 220.0)]

## 100 pairs
extra_c = [(170.0, -160.0), (50.0, 150.0), (280.0, -140.0), (-110.0, 90.0), (190.0, -30.0), (-210.0, -180.0),
           (-210.0, 150.0), (110.0, 20.0), (140.0, 160.0), (-230.0, 40.0), (-70.0, 100.0), (-70.0, 190.0),
           (200.0, 30.0), (10.0, -190.0), (-120.0, -20.0), (100.0, -40.0), (110.0, 80.0), (-110.0, -70.0),
           (250.0, 140.0), (60.0, -160.0), (-130.0, 10.0), (-270.0, -80.0), (-70.0, -140.0), (0.0, 130.0),
           (-90.0, -100.0), (80.0, -100.0), (-100.0, 30.0), (100.0, 70.0), (-110.0, 190.0), (80.0, -190.0),
           (0.0, -120.0), (70.0, 120.0), (10.0, 180.0)]
extra_nc = [(120.0, -180.0), (20.0, 180.0), (270.0, -50.0), (-150.0, 90.0), (170.0, -10.0), (-200.0, -140.0),
            (-220.0, 190.0), (130.0, 40.0), (180.0, 150.0), (-260.0, 60.0), (-80.0, 70.0), (-90.0, 150.0), (240.0, 0.0),
            (-20.0, -180.0), (-100.0, -40.0), (120.0, -30.0), (160.0, 70.0), (-160.0, -60.0), (260.0, 200.0),
            (30.0, -140.0), (-140.0, -20.0), (-300.0, -70.0), (-100.0, -130.0), (-20.0, 110.0), (-70.0, -100.0),
            (60.0, -90.0), (-120.0, 20.0), (90.0, 50.0), (-170.0, 180.0), (130.0, -200.0), (-10.0, -100.0),
            (80.0, 90.0), (30.0, 220.0)]

## 50% pairs
extra_c_50p = [(150.0, -30.0), (-140.0, -130.0), (150.0, 150.0), (-230.0, 20.0), (-50.0, 140.0), (110.0, 80.0),
               (-110.0, -60.0), (-70.0, -140.0), (190.0, -30.0), (-210.0, -200.0), (200.0, 210.0), (-290.0, 40.0),
               (-70.0, 180.0), (170.0, 120.0), (-160.0, -100.0), (-110.0, -160.0), (80.0, 200.0), (290.0, -130.0),
               (-130.0, 100.0), (-290.0, 180.0), (-70.0, 100.0), (0.0, -130.0), (240.0, 140.0), (50.0, -110.0),
               (-240.0, -80.0), (0.0, 130.0), (-100.0, -90.0), (-130.0, 50.0), (90.0, 70.0), (-110.0, 170.0),
               (90.0, -190.0), (0.0, -120.0), (70.0, 120.0)]
extra_nc_50p = [(170.0, -140.0), (-170.0, 100.0), (-80.0, 160.0), (-90.0, -30.0), (-70.0, -90.0), (-120.0, 30.0),
                (70.0, 80.0), (50.0, 110.0), (110.0, -170.0), (-110.0, 150.0), (-30.0, 180.0), (-100.0, 0.0),
                (-90.0, -70.0), (-100.0, 60.0), (90.0, 40.0), (80.0, 90.0), (80.0, 160.0), (160.0, -60.0),
                (-270.0, 120.0), (130.0, 50.0), (210.0, 140.0), (-250.0, -20.0), (-80.0, 70.0), (150.0, 70.0),
                (-160.0, -60.0), (270.0, 180.0), (70.0, -130.0), (-150.0, 30.0), (-270.0, -150.0), (-120.0, -130.0),
                (20.0, 110.0), (-20.0, -100.0), (-30.0, 210.0)]

## 0% pair
extra_c_0p = [(130.0, -120.0), (200.0, -90.0), (-120.0, 100.0), (150.0, -50.0), (-170.0, -130.0), (120.0, 20.0),
              (130.0, 140.0), (-50.0, 140.0), (10.0, -150.0), (120.0, 90.0), (-120.0, -80.0), (50.0, -110.0),
              (-130.0, 0.0), (-70.0, -120.0), (-100.0, 30.0), (50.0, 90.0), (150.0, -170.0), (290.0, -120.0),
              (-160.0, 150.0), (200.0, -50.0), (-210.0, -190.0), (160.0, 20.0), (210.0, 220.0), (-80.0, 170.0),
              (0.0, -190.0), (160.0, 110.0), (-160.0, -100.0), (60.0, -160.0), (-170.0, 0.0), (-110.0, -160.0),
              (-130.0, 40.0), (70.0, 120.0), (-70.0, 100.0)]
extra_nc_0p = [(170.0, -140.0), (-170.0, 100.0), (-80.0, 160.0), (-90.0, -30.0), (-70.0, -90.0), (-120.0, 30.0),
               (70.0, 80.0), (50.0, 110.0), (110.0, -170.0), (-110.0, 150.0), (-30.0, 180.0), (-100.0, 0.0),
               (-90.0, -70.0), (-100.0, 60.0), (90.0, 40.0), (80.0, 90.0), (80.0, 160.0), (160.0, -60.0),
               (-270.0, 120.0), (130.0, 50.0), (210.0, 140.0), (-250.0, -20.0), (-80.0, 70.0), (150.0, 70.0),
               (-160.0, -60.0), (270.0, 180.0), (70.0, -130.0), (-150.0, 30.0), (-270.0, -150.0), (-120.0, -130.0),
               (20.0, 110.0), (-20.0, -100.0), (-30.0, 210.0)]

baseline = [(-120.0, -20.0), (-270.0, 30.0), (-40.0, -180.0), (-10.0, 180.0), (-160.0, 10.0), (-110.0, -70.0),
            (-80.0, -90.0), (-50.0, 120.0), (-130.0, 60.0), (70.0, 130.0), (-150.0, -120.0), (250.0, 160.0),
            (-160.0, 160.0), (-230.0, 200.0), (-230.0, -70.0), (230.0, -200.0), (110.0, 220.0), (110.0, 90.0),
            (-80.0, 210.0), (80.0, -160.0), (50.0, 190.0), (-90.0, 140.0), (-110.0, -160.0), (-270.0, -220.0),
            (140.0, 60.0), (-170.0, -50.0), (150.0, -160.0), (300.0, 60.0), (100.0, 10.0), (-300.0, 120.0),
            (120.0, -100.0), (20.0, -200.0), (30.0, 140.0), (-60.0, -120.0), (210.0, -40.0), (190.0, -110.0),
            (300.0, -70.0), (50.0, -90.0), (-10.0, 130.0), (-190.0, 50.0), (-100.0, 10.0), (20.0, -120.0),
            (140.0, 150.0), (220.0, 50.0), (80.0, -220.0), (100.0, -50.0), (150.0, 10.0), (-80.0, 60.0), (140.0, -30.0),
            (-160.0, -200.0), (90.0, 60.0), (-20.0, -120.0), (-100.0, 90.0), (10.0, 100.0), (-290.0, -120.0),
            (70.0, 90.0), (180.0, 100.0), (80.0, -110.0), (-210.0, -10.0), (-220.0, 110.0), (-210.0, -140.0),
            (100.0, -20.0), (-60.0, 80.0), (-90.0, -220.0), (190.0, 220.0), (40.0, 100.0)]

exp1_c = [(20.0, -170.0), (230.0, -100.0), (-60.0, -140.0), (300.0, -20.0), (-110.0, 160.0), (60.0, 140.0),
          (230.0, 90.0), (100.0, 70.0), (120.0, -210.0), (-20.0, 210.0), (-200.0, 100.0), (-70.0, 80.0),
          (-250.0, -160.0), (100.0, -80.0), (-260.0, 30.0), (-260.0, 180.0), (210.0, -10.0), (-140.0, -160.0),
          (300.0, 160.0), (-180.0, -10.0), (-80.0, 130.0), (170.0, -100.0), (180.0, 90.0), (-140.0, 80.0),
          (-20.0, -110.0), (50.0, -100.0), (-100.0, -60.0), (-110.0, 60.0), (250.0, -180.0), (140.0, 20.0),
          (140.0, 180.0), (-40.0, -200.0), (150.0, -50.0), (-140.0, 0.0), (-10.0, 130.0), (-130.0, -70.0),
          (-150.0, 210.0), (130.0, 100.0), (40.0, 110.0), (80.0, -60.0), (200.0, 210.0), (100.0, -10.0),
          (-140.0, -220.0), (-100.0, -10.0), (90.0, -130.0), (-60.0, -80.0), (-10.0, 100.0), (-220.0, -100.0),
          (80.0, 170.0), (-10.0, 170.0), (20.0, -130.0), (-290.0, -220.0), (100.0, -170.0)]

exp1_nc = [(50.0, 150.0), (-170.0, 140.0), (0.0, -150.0), (-190.0, 10.0), (-180.0, 80.0), (200.0, -50.0),
           (100.0, -140.0), (290.0, 80.0), (220.0, 150.0), (150.0, -70.0), (80.0, -210.0), (-210.0, -60.0),
           (-120.0, 30.0), (280.0, -180.0), (-120.0, 170.0), (-260.0, -210.0), (140.0, 190.0), (-110.0, -70.0),
           (130.0, 10.0), (-50.0, -210.0), (150.0, 80.0), (0.0, 100.0), (-60.0, -110.0), (-280.0, 60.0),
           (-300.0, 210.0), (-60.0, 190.0), (-90.0, 80.0), (-120.0, -30.0), (-130.0, -130.0), (10.0, 180.0),
           (40.0, -110.0), (210.0, -220.0), (300.0, -30.0), (-60.0, 120.0), (-140.0, -200.0), (130.0, 40.0),
           (110.0, -80.0), (-20.0, -100.0), (-300.0, -30.0), (90.0, 60.0), (-200.0, -110.0), (90.0, 110.0),
           (-70.0, -80.0), (30.0, -220.0), (110.0, -30.0), (70.0, -80.0), (-30.0, 110.0), (230.0, 20.0),
           (300.0, -110.0), (-100.0, 50.0), (-60.0, 80.0), (-100.0, 0.0), (50.0, 90.0)]

exp1_crowding = [(20.0, -170.0), (230.0, -100.0), (-60.0, -140.0), (300.0, -20.0), (-110.0, 160.0), (60.0, 140.0),
                 (230.0, 90.0), (100.0, 70.0), (120.0, -210.0), (-20.0, 210.0), (-200.0, 100.0), (-70.0, 80.0),
                 (-250.0, -160.0), (100.0, -80.0), (-260.0, 30.0), (-260.0, 180.0), (210.0, -10.0), (-140.0, -160.0),
                 (300.0, 160.0), (-180.0, -10.0), (-80.0, 130.0), (170.0, -100.0), (180.0, 90.0), (-140.0, 80.0),
                 (-20.0, -110.0), (50.0, -100.0), (-100.0, -60.0), (-110.0, 60.0), (250.0, -180.0), (140.0, 20.0),
                 (140.0, 180.0), (-40.0, -200.0), (150.0, -50.0), (-140.0, 0.0), (-10.0, 130.0), (-130.0, -70.0),
                 (-150.0, 210.0), (130.0, 100.0), (40.0, 110.0), (80.0, -60.0), (200.0, 210.0), (100.0, -10.0),
                 (-140.0, -220.0), (-100.0, -10.0), (90.0, -130.0), (-60.0, -80.0), (-10.0, 100.0), (-220.0, -100.0),
                 (80.0, 170.0), (-10.0, 170.0), (20.0, -130.0), (-290.0, -220.0), (100.0, -170.0)]

exp1_no_crowding = [(-240.0, -190.0), (-90.0, -130.0), (-270.0, -90.0), (-50.0, -210.0), (210.0, 170.0),
                    (-300.0, 190.0), (300.0, -190.0), (-40.0, 160.0), (60.0, -140.0), (120.0, 50.0), (-260.0, 10.0),
                    (250.0, -30.0), (300.0, 130.0), (140.0, -80.0), (30.0, 190.0), (100.0, 170.0), (190.0, 30.0),
                    (120.0, -120.0), (-180.0, 80.0), (20.0, -190.0), (-40.0, -100.0), (-110.0, -50.0), (180.0, -210.0),
                    (260.0, -90.0), (-270.0, 70.0), (70.0, 100.0), (-190.0, 170.0), (120.0, 120.0), (-80.0, 70.0),
                    (80.0, -60.0), (-110.0, -80.0), (-180.0, -20.0), (150.0, -10.0), (-10.0, 120.0), (30.0, 100.0),
                    (-180.0, -220.0), (-60.0, 100.0), (-130.0, 180.0), (-10.0, 220.0), (-140.0, 10.0), (20.0, -100.0),
                    (-110.0, -20.0), (130.0, -40.0), (-10.0, -130.0), (-90.0, 50.0), (60.0, -90.0), (-100.0, 30.0),
                    (-110.0, -220.0), (120.0, -220.0), (100.0, 20.0), (-90.0, 210.0), (-180.0, -100.0), (100.0, 70.0)]


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

    fig.savefig('try.png', bbox_inches = 'tight', pad_inches = 0)


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

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (8, 6))

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
    fig.savefig('try.png', bbox_inches = 'tight', pad_inches = 0)


def drawEllipse_crowding(e_posi, black_disc_posi, red_disc_posi, crowding_posi, ka, kb, ellipseColor_r = 'royalblue',
                         ellipseColor_t = 'royalblue'):
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

    # tangential
    angle_deg2 = []
    for ang in range(len(e_posi)):
        angle_rad0_2 = atan2(e_posi[ang][1], e_posi[ang][0])
        angle_deg0_2 = angle_rad0_2 * 180 / pi + 90
        angle_deg2.append(angle_deg0_2)
    # my_e2 = [Ellipse(xy = e_posi[j], width = eccentricities[j] * ka * 2, height = eccentricities[j] * kb * 2,
    #                  angle = angle_deg[j] + 90)
    #          for j in range(len(e_posi))]

    fig, ax = plt.subplots(subplot_kw = {'aspect': 'equal'}, figsize = (8, 6))
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        # e.set_alpha(0.5)
        # e.set_facecolor(ellipseColor_r)
        e.set_edgecolor(ellipseColor_r)
        e.set_fill(False)
    # for e2 in my_e2:
    #     ax.add_artist(e2)
    #     e2.set_clip_box(ax.bbox)
    #     e2.set_alpha(0.5)
    #     e2.set_facecolor(ellipseColor_t)

    # show the discs on the ellipses-flower
    for dot in e_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4, alpha = 0.3)
    for dot in black_disc_posi:
        plt.plot(dot[0], dot[1], color = 'k', marker = 'o', markersize = 4)
    for dot in red_disc_posi:
        plt.plot(dot[0], dot[1], color = 'orangered', marker = 'o', markersize = 4)

    # add concentric circles
    ax.add_patch(
        plt.Circle((0, 0), distance.euclidean((100, 170), (0, 0)), alpha = 0.5, linestyle = "--", fill = False))
    ax.add_patch(plt.Circle((0, 0), distance.euclidean((80, 60), (0, 0)), alpha = 0.5, linestyle = "--", fill = False))
    # for dot in extra_nc:
    #     plt.plot(dot[0], dot[1], color = 'r', marker = 'o', markersize = 2)
    # plt.show()
    plt.plot(0, 0, color = 'k', marker = '+', markersize = 10)
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
    fig.savefig('try.png', bbox_inches = 'tight', pad_inches = 0)


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

    fig.savefig('try.png', bbox_inches = 'tight', pad_inches = 0)


if __name__ == '__main__':
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

    # centralc_75_paris= [(170.0, -110.0), (-250.0, 0.0), (70.0, 220.0), (130.0, 40.0), (150.0, -200.0), (20.0, -150.0), (-170.0, -210.0), (260.0, 60.0), (-130.0, 120.0), (-140.0, 50.0), (-180.0, -100.0), (-40.0, 110.0), (190.0, 150.0), (-270.0, 190.0), (-100.0, 20.0), (160.0, -10.0), (0.0, -100.0), (-60.0, -150.0), (-100.0, -70.0), (-30.0, 190.0), (300.0, -180.0), (40.0, 130.0), (70.0, 90.0), (70.0, -110.0), (-290.0, -180.0), (-10.0, -220.0), (300.0, -50.0), (100.0, -20.0), (-160.0, -20.0), (-150.0, 210.0), (0.0, 100.0), (-50.0, -90.0), (-80.0, 70.0)]

    # extra_c_75_paris = [(-30.0, 100.0), (160.0, 150.0), (60.0, 80.0), (-120.0, 160.0), (-50.0, 130.0), (220.0, 160.0), (80.0, 110.0), (-180.0, 220.0), (140.0, -80.0), (110.0, 40.0), (110.0, -170.0), (20.0, -180.0), (-160.0, -170.0), (300.0, 80.0), (-150.0, 150.0), (-110.0, 40.0), (-160.0, -90.0), (-300.0, 210.0), (-120.0, 20.0), (180.0, 0.0), (0.0, -110.0), (-70.0, -170.0), (-80.0, -60.0), (-40.0, 210.0), (40.0, 110.0), (-240.0, -170.0), (-10.0, -180.0), (250.0, -40.0), (120.0, -20.0), (-130.0, -10.0), (0.0, 110.0), (-60.0, -110.0), (-90.0, 80.0)]

    # centralc_25_paris = [(-290.0, 140.0), (210.0, -220.0), (-50.0, -140.0), (-160.0, 220.0), (-170.0, 80.0), (-120.0, -130.0), (200.0, -110.0), (20.0, 100.0), (-60.0, 200.0), (280.0, 220.0), (-30.0, 110.0), (110.0, -120.0), (120.0, 0.0), (220.0, 110.0), (-190.0, -90.0), (130.0, -50.0), (70.0, -220.0), (280.0, -30.0), (20.0, -140.0), (130.0, 200.0), (-280.0, -30.0), (-90.0, 80.0), (-100.0, -50.0), (20.0, 180.0), (-300.0, -200.0), (90.0, 60.0), (-130.0, 0.0), (160.0, 50.0), (-40.0, -220.0), (-160.0, -220.0), (60.0, -90.0), (110.0, 120.0), (-60.0, -80.0)]

    # extra_c_25_paris = [(-50.0, -120.0), (-150.0, 70.0), (-100.0, -110.0), (160.0, -90.0), (-20.0, 100.0), (180.0, 90.0), (-150.0, -70.0), (110.0, -50.0), (-80.0, 70.0), (30.0, 160.0), (-110.0, -10.0), (120.0, 40.0), (-60.0, -170.0), (-210.0, 100.0), (-140.0, -140.0), (230.0, -130.0), (-30.0, 130.0), (240.0, 140.0), (-220.0, -110.0), (150.0, -50.0), (-110.0, 100.0), (10.0, 200.0), (-150.0, -10.0), (190.0, 50.0), (30.0, 110.0), (-50.0, 160.0), (80.0, -190.0), (-250.0, -30.0), (-120.0, -60.0), (100.0, 70.0), (-40.0, -180.0), (-160.0, -180.0), (70.0, -100.0)]

    # drawEllipse_full(centralc_75_paris, extra_c_75_paris, 0.25,0.1)
    # drawEllipse_full(centralc_25_paris, extra_c_25_paris, 0.25,0.1)

    # =============================================================================
    # exp 1 display sample
    # =============================================================================
    # draw_disc_only(exp1_crowding)
    # # exp 1 display with ellipses no-crowding
    # drawEllipses(posi = exp1_no_crowding, ka = 0.25, kb = 0.1, ellipseColor = 'orangered', ellipsetransp = 0.5)
    # # exp1 display with ellipses crowding

    # ms1 figure 2e
    exp1_c_demo = [(20.0, -170.0), (230.0, -100.0), (300.0, -20.0), (120.0, -210.0), (100.0, -80.0), (210.0, -10.0),
                   (170.0, -100.0), (50.0, -100.0), (250.0, -180.0), (150.0, -50.0), (80.0, -60.0), (100.0, -10.0),
                   (90.0, -130.0), (20.0, -130.0), (100.0, -170.0)]
    central_disc = [(100, -170.0), (80.0, -60.0)]
    extra_disc = [(90.0, -130.0), (120, -210), (100.0, -80.0)]
    drawEllipse_crowding(exp1_c_demo, central_disc, extra_disc, central_disc, ka = 0.35, kb = 0.12,
                         ellipseColor_r = 'orangered',
                         ellipseColor_t = 'white')