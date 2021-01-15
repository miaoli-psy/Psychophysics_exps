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

    # Read stimuli display
    PATH = "../displays/"
    FILENAME = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILENAME)

    posis = stimuli_df.positions_list[51]
    posis = str_to_list(posis)
    polar_posis = get_polar_coordinates(posis)

    diff = []
    for index, polar_posi in enumerate(polar_posis):
        if index > 0:
            diff.append(polar_posi[0]-polar_posis[index-1][0])


    myrange = get_angle_range(polar_posis, 7.13, 15.13)





    if is_debug:
        col_names = get_col_names(stimuli_df)