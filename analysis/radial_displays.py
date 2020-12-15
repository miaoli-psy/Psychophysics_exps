# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:56:42 2020
@author: Miao
"""
import pandas as pd
import matplotlib.pyplot as plt

from commons import process_str
from point import polar_point, count_point

# =============================================================================
# theta = 12 deg (around 11.42 deg, defined by the size of crowding zones)
# =============================================================================


# rotated_a = affinity.rotate(line, 20)
# rotated_b = affinity.rotate(geom = b, angle = -20, origin=((0,0)), use_radians=False)) #negative anlge: clockwise

def get_temp_data(simuli_df):
    # check df coloum names
    c_names = simuli_df.columns.to_list()
    return c_names

def draw_temp(polar:list):
    x_val = [x[0] for x in polar]
    y_val = [x[1] for x in polar]
    fig, ax = plt.subplots()
    ax.plot(x_val, y_val)


if __name__ == '__main__':
    is_debug = False

    # read stimuli display
    path = "../displays/"
    filename = "update_stim_info_full.xlsx"
    simuli_df = pd.read_excel(path + filename)

    try_posi = process_str.str_to_list(simuli_df.positions_list[0])
    polar = polar_point.get_polar_coordinates(try_posi)
    count_list = count_point.get_point_count_list(polar)
    range_list = count_point.get_range_count(count_list, step = 10)

    # steps = [i for i in range(0, 46)]
    # for step in steps:
    #     range_list = get_range_list(try_posi, step)
    #     # TODO: draw picture of range_list

    if is_debug:
        c_names = get_temp_data(simuli_df)
        draw_temp(polar)