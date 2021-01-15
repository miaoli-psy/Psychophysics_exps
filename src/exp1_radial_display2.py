# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-14 20:21
IDE: PyCharm
Introduction:
"""
import pandas as pd

from src.analysis.exp1_raidal_displays_analysis2 import get_angle_range, count_ndisc_in_range
from src.commons.process_dataframe import get_col_names
from src.commons.process_str import str_to_list
from src.point.polar_point import get_polar_coordinates

if __name__ == '__main__':
    is_debug = True
    indi_display = True

    # Read stimuli display
    PATH = "../displays/"
    FILENAME = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILENAME)

    # individual display alignment value
    if indi_display:
        display_n = 51 # 0-249
        posis = stimuli_df.positions_list[display_n]
        posis = str_to_list(posis)
        # get polar positions for a single display
        polar_posis = get_polar_coordinates(posis)

        # check how close between the nearest two disc
        diff = []
        for index, polar_posi in enumerate(polar_posis):
            if index > 0:
                diff.append(polar_posi[0]-polar_posis[index-1][0])
        # some parameters, started and ended where
        ini_start_angle = polar_posis[0][0]
        angle_size = 12
        ini_end_angle = ini_start_angle + angle_size
        # get the ranges
        my_range = get_angle_range(polar_posis, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
        # get number of discs in each range
        ndisc_list = list()
        for beam in my_range:
            ndisc = count_ndisc_in_range(polar_posis, beam[0], beam[1])
            ndisc_list.append(ndisc)




    if is_debug:
        col_names = get_col_names(stimuli_df)