# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:56:42 2020
@author: Miao
"""
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Dict

from commons import process_str
from point import polar_point, count_point

# =============================================================================
# theta = 12 deg (around 11.42 deg, defined by the size of crowding zones)
# =============================================================================

def get_temp_data(simuli_df):
    # check df coloum names
    c_names = simuli_df.columns.to_list()
    return c_names

def draw_temp(polar:list):
    x_val = [x[0] for x in polar]
    y_val = [x[1] for x in polar]
    fig, ax = plt.subplots()
    ax.plot(x_val, y_val)

def get_step_ranges_map(step_range:Tuple[int], all_positions:list):
    # key: step, value: range_list
    step_ranges_map = dict()
    step_start, step_end = step_range[0], step_range[1]
    steps = [i for i in range(step_start, step_end)]

    for curr_positions in all_positions:
        curr_positions_list = process_str.str_to_list(curr_positions)
        polar = polar_point.get_polar_coordinates(curr_positions_list)
        count_list = count_point.get_point_count_list(polar)
        for step in steps:
            range_list = count_point.get_range_count(count_list, step)
            if step not in step_ranges_map.keys():
                step_ranges_map[step] = [range_list]
            else:
                step_ranges_map[step].append(range_list)
    return step_ranges_map

if __name__ == '__main__':
    is_debug = False

    # read stimuli display
    path = "../displays/"
    filename = "update_stim_info_full.xlsx"
    simuli_df = pd.read_excel(path + filename)

    step_range = (0, 2)
    all_positions = simuli_df.positions_list
    # key: step, value: range_list
    step_ranges_map = get_step_ranges_map(step_range, all_positions)


    # TODO: draw picture of range_list
    if is_debug:
        c_names = get_temp_data(simuli_df)
        # draw_temp(polar)