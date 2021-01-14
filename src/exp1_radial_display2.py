# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-14 20:21
IDE: PyCharm
Introduction:
"""
import pandas as pd

from src.analysis.exp1_radial_displays_analysis import get_col_names
from src.commons.process_str import str_to_list
from src.point.polar_point import get_polar_coordinates

if __name__ == '__main__':
    is_debug = True

    # Read stimuli display
    PATH = "../displays/"
    FILENAME = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILENAME)

    posis = stimuli_df.positions_list[248]
    posis = str_to_list(posis)
    polar_posis = get_polar_coordinates(posis)

    diff = []
    for index, polar_posi in enumerate(polar_posis):
        if index > 0:
            diff.append(polar_posi[0]-polar_posis[index-1][0])

    start_angle = 0
    end_angle = 12
    count = 0

    res_dict = dict()
    for index, polar_posi in enumerate(polar_posis):
        if start_angle <= polar_posi[0] <= end_angle:
            count += 1
        else:
            start_angle = polar_posi[0]
            end_angle = start_angle + 12
            if end_angle > 360:
                end_angle = end_angle - 360
            count = 1
        res_dict.update({(start_angle, end_angle): count})


    if is_debug:
        col_names = get_col_names(stimuli_df)