# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-28 14:40
IDE: PyCharm
Introduction:
"""

from src.commons import process_str
from src.point import polar_point, count_point
from typing import Tuple, Dict, List


def get_col_names(simuli_df):
    # check df coloum names
    c_names = simuli_df.columns.to_list()
    return c_names


# __prefix means: this function is a private function
# which only be used as a helper sub-function in a bigger function
def get_draw_ndisc_formate(curr_rangelist):
    # [[[0,1], 0],...] -> [(0.5, 0)...]
    # [[[1,3], 1],...] -> [(2.0, 1)...]
    formate_list = list()
    for index, l in enumerate(curr_rangelist):
        angle_new = (l[0][0] + l[0][1]) / 2
        formate_list.append((angle_new, l[1]))
    return formate_list


def __add_ranges_to_map(step_ranges_map: Dict[int, List[list]], range_list, step: int):
    is_need_initial_key_in_dict = (step not in step_ranges_map.keys())
    if is_need_initial_key_in_dict:
        step_ranges_map[step] = [range_list]
    else:
        step_ranges_map[step].append(range_list)


def __get_count_list(curr_positions: list) -> list:
    curr_positions_list = process_str.str_to_list(curr_positions)
    polar = polar_point.get_polar_coordinates(curr_positions_list)
    count_list = count_point.get_point_count_list(polar)
    return count_list


def __add_current_positions_to_map(steps: List[int], count_list: list, step_ranges_map: Dict[int, list]):
    for step in steps:
        range_list = count_point.get_range_count(count_list, step)
        __add_ranges_to_map(step_ranges_map, range_list, step)


def get_step_ranges_map(step_range: Tuple[int], all_positions_list: list):
    # key: step, value: range_list
    step_ranges_map = dict()
    step_start, step_end = step_range[0], step_range[1]
    steps = [i for i in range(step_start, step_end)]

    for curr_positions in all_positions_list:
        # count_list: disc num for given angle: [[angle, point_count_number], etc]
        count_list = __get_count_list(curr_positions)
        __add_current_positions_to_map(steps, count_list, step_ranges_map)

    return step_ranges_map