# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:56:42 2020
@author: Miao
"""
import pandas as pd
import matplotlib.pyplot as plt

from commons import process_str, position


def get_point_count_list(polar:list) -> list:
    # polar:                                 [(angle, distance),etc]
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    count_list = [[i, 0] for i in range(360)]
    for point in polar:
        # point: (angle, distance)
        angle = point[0]
        # angle_num: [angle, point_count_number]
        angle_num = count_list[angle]
        point_count_number = angle_num[1]
        angle_num[1] = point_count_number + 1
    return count_list

def get_point_num_in_range(count_list:list, curr_range:list) -> int:
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    # curr_range: angle range [start: end)
    # point_num: how many disc in curr_range
    point_num = 0
    start, end = curr_range[0], curr_range[1]
    if start < end:
        for angle_num in count_list[start:end]:
            point_num += angle_num[1]
    else:
        for angle_num in count_list[start:]:
            point_num += angle_num[1]
        for angle_num in count_list[0:end]:
            point_num += angle_num[1]
    return point_num

def get_range_count(count_list:list, step:int) -> list:
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    # res_count: [[[angle, angle+step), num1], [[angle+1, angle+step+1), num2], etc]
    range_step = list()
    res_count = list()
    # build ranges
    for angle_num in count_list:
        angle = angle_num[0]
        next_degree = angle + step
        if next_degree <= 359:
            range_step.append([angle, next_degree])
        else:
            range_step.append([angle, next_degree-360])
    # give numbers for range
    for curr_range in range_step:
        res_count.append([curr_range, get_point_num_in_range(count_list, curr_range)])
    return res_count


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
    polar = position.get_polar_coordinates(try_posi)
    count_list = get_point_count_list(polar)
    range_list = get_range_count(count_list, step = 10)

    # steps = [i for i in range(0, 46)]
    # for step in steps:
    #     range_list = get_range_list(try_posi, step)
    #     # TODO: draw picture of range_list

    if is_debug:
        c_names = get_temp_data(simuli_df)
        draw_temp(polar)