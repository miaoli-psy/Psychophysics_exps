# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:41 2020

@author: Miao
"""
# https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145014176
from src.commons.draw_displays import drawEllipses, draw_disc_only, drawEllipse_full, drawEllipse_crowding, drawEllipses_homo
from src.constants.sample_display_posi import SamplePosiExp1, SamplePosiExp2, SampleDensity

if __name__ == '__main__':
    exp1_demo = False
    exp2_demo = False
    density_demo = True
    if exp1_demo:
        # exp 1 display sample
        draw_disc_only(SamplePosiExp1.exp1_c)
        draw_disc_only(SamplePosiExp1.exp1_nc)
        # exp 1 display with ellipses no-crowding
        drawEllipses(posi = SamplePosiExp1.exp1_nc, ka = 0.25, kb = 0.1, ellipseColor = 'white', ellipsetransp = 0.5)
        # exp1 display with ellipses crowding
        drawEllipses(posi = SamplePosiExp1.exp1_c, ka = 0.1, kb = 0.25, ellipseColor = 'white', ellipsetransp = 0.5)

    if exp2_demo:
        drawEllipse_full(SamplePosiExp2.centerposi, [], ka = 0.25, kb = 0.1, ellipseColor_r = 'white',
                         ellipseColor_t = 'white')
        drawEllipse_full(SamplePosiExp2.centerposi, SamplePosiExp2.extra_c, ka = 0.25, kb = 0.1, ellipseColor_r = 'white',
                         ellipseColor_t = 'white')
        draw_disc_only(SamplePosiExp2.centerposi + SamplePosiExp2.extra_c)
        drawEllipse_full(SamplePosiExp2.centerposi, SamplePosiExp2.extra_nc, ka = 0.25, kb = 0.1, ellipseColor_r = 'white',
                         ellipseColor_t = 'white', extra_disc_color = 'royalblue')
        draw_disc_only(SamplePosiExp2.centerposi + SamplePosiExp2.extra_nc)
        drawEllipses(SamplePosiExp2.centerposi, extra_posi = SamplePosiExp2.extra_c, ellipseColor = 'white', ka = 0.25,
                     kb = 0.1, extra_disc_color = "orangered")
        drawEllipses(SamplePosiExp2.centerposi, extra_posi = SamplePosiExp2.extra_nc, ellipseColor = 'white', ka = 0.25,
                     kb = 0.1, extra_disc_color = "royalblue")
        drawEllipses(SamplePosiExp2.baseline, ellipseColor="white", ka = 0.14, kb = 0.14)
        draw_disc_only(SamplePosiExp2.baseline)

    if density_demo:
        drawEllipses(posi = SampleDensity.increase, ka = 0.155, kb = 0.155, ellipseColor = 'white', ellipsetransp = 0.5)
        drawEllipses_homo(posi = SampleDensity.homo, ka = 31, kb = 31, ellipseColor = 'white', ellipsetransp = 0.5)


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