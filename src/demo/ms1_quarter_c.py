# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:41 2020
@author: Miao
ms1 figure 2e - a quarter of a sample crowding display
"""

# https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145014176
from src.commons.draw_displays import drawEllipse_crowding

if __name__ == '__main__':
    exp1_c_demo = [(20.0, -170.0), (230.0, -100.0), (300.0, -20.0), (120.0, -210.0), (100.0, -80.0), (210.0, -10.0),
                   (170.0, -100.0), (50.0, -100.0), (250.0, -180.0), (150.0, -50.0), (80.0, -60.0), (100.0, -10.0),
                   (90.0, -130.0), (20.0, -130.0), (100.0, -170.0)]
    central_disc = [(100, -170.0), (80.0, -60.0), (300.0, -20.0), (20.0, -170.0)]
    extra_disc = [(90.0, -130.0), (120, -210), (100.0, -80.0), (210.0, -10.0), (20.0, -130.0)]
    drawEllipse_crowding(exp1_c_demo, central_disc, extra_disc, central_disc, ka = 0.35, kb = 0.12,
                         ellipseColor_r = 'orangered', savefig = True)