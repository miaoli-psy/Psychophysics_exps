# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 22:54:41 2020

@author: Miao
"""
import pandas as pd

# https://www.liaoxuefeng.com/wiki/1016959663602400/1017454145014176
from src.commons.draw_displays import drawEllipses, draw_disc_only, drawEllipse_full, drawEllipse_crowding, \
    drawEllipses_homo, draw_mix_color_discs
from src.commons.process_str import str_to_list
from src.constants.sample_display_posi import SamplePosiExp1, SampleDensity

# ms2 demo displays
ms2_display_demo = pd.read_csv("demo_posi.csv")
centerposi = str_to_list(ms2_display_demo.iloc[0]['base_posi'])
# extra discs posis 0-100% pairs, radial and tangential displays
extra_r_0 = str_to_list(ms2_display_demo.iloc[0]["extra_r_0"])
extra_r_25 = str_to_list(ms2_display_demo.iloc[0]["extra_r_25"])
extra_r_50 = str_to_list(ms2_display_demo.iloc[0]["extra_r_50"])
extra_r_75 = str_to_list(ms2_display_demo.iloc[0]["extra_r_75"])
extra_r_100 = str_to_list(ms2_display_demo.iloc[0]["extra_r_100"])
extra_t_0 = str_to_list(ms2_display_demo.iloc[0]["extra_t_0"])
extra_t_25 = str_to_list(ms2_display_demo.iloc[0]["extra_t_25"])
extra_t_50 = str_to_list(ms2_display_demo.iloc[0]["extra_t_50"])
extra_t_75 = str_to_list(ms2_display_demo.iloc[0]["extra_t_75"])
extra_t_100 = str_to_list(ms2_display_demo.iloc[0]["extra_t_100"])
# extra discs for discs triplets
extra_r_triplet = str_to_list(ms2_display_demo.iloc[0]["tri_r"])
extra_t_triplet = str_to_list(ms2_display_demo.iloc[0]["tri_t"])

if __name__ == '__main__':
    exp1_demo = True
    exp1_process = False
    exp2_demo = False
    density_demo = False
    if exp1_demo:
        # exp 1 display sample
        draw_disc_only(SamplePosiExp1.exp1_c)
        draw_disc_only(SamplePosiExp1.exp1_nc)
        # exp 1 display with ellipses no-crowding
        drawEllipses(posi = SamplePosiExp1.exp1_nc, ka = 0.25, kb = 0.1, ellipseColor = 'white', ellipsetransp = 0.5)
        # exp1 display with ellipses crowding
        drawEllipses(posi = SamplePosiExp1.exp1_c, ka = 0.1, kb = 0.25, ellipseColor = 'white', ellipsetransp = 0.5)

        drawEllipse_full(SamplePosiExp1.exp1_c, [], ka=0.25, kb=0.1, ellipseColor_r='white', ellipseColor_t='white', name_str=100)

    if exp1_process:
        endN = len(SamplePosiExp1.exp1_c)
        for i in range(0, endN):
            drawEllipses(posi=SamplePosiExp1.exp1_c[:i], ka=0.1, kb=0.25, ellipseColor='white', ellipsetransp=0.5, name_str = i)

    if exp2_demo:
        # drawEllipse_full(SamplePosiExp2.centerposi, [], ka = 0.25, kb = 0.1, ellipseColor_r = 'white',
        #                  ellipseColor_t = 'white')
        drawEllipse_full(centerposi, extra_r_triplet, ka = 0.25, kb = 0.1, ellipseColor_r = 'white', ellipseColor_t = 'white', name_str = 100 )
        draw_disc_only(centerposi + extra_r_triplet)
        draw_mix_color_discs(centerposi, extra_r_100)

        drawEllipse_full(centerposi, extra_t_triplet, ka = 0.25, kb = 0.1, ellipseColor_r = 'white', ellipseColor_t = 'white', extra_disc_color = 'royalblue')
        draw_disc_only(centerposi + extra_t_triplet)
        draw_mix_color_discs(centerposi, extra_t_100)


        # drawEllipses(SamplePosiExp2.centerposi, extra_posi = SamplePosiExp2.extra_c, ellipseColor = 'white', ka = 0.25,
        #              kb = 0.1, extra_disc_color = "orangered")
        # drawEllipses(SamplePosiExp2.centerposi, extra_posi = SamplePosiExp2.extra_nc, ellipseColor = 'white', ka = 0.25,
        #              kb = 0.1, extra_disc_color = "royalblue")

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