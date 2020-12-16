"""
TODO: What does this code do?
"""
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List

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

# __prefix means: this function is a private function 
# which only be used as a helper sub-function in a bigger function
def __add_ranges_to_map(step_ranges_map:Dict[int, list], range_list, step:int):
    if step not in step_ranges_map.keys():
        step_ranges_map[step] = [range_list]
    else:
        step_ranges_map[step].append(range_list)

def __get_count_list(curr_positions:list) -> list:
    curr_positions_list = process_str.str_to_list(curr_positions)
    polar = polar_point.get_polar_coordinates(curr_positions_list)
    count_list = count_point.get_point_count_list(polar)
    return count_list

def __add_current_positions_to_map(steps:List[int], count_list:list, step_ranges_map:Dict[int, list]):
    for step in steps:
        range_list = count_point.get_range_count(count_list, step)
        __add_ranges_to_map(step_ranges_map, range_list, step)

def get_step_ranges_map(step_range:Tuple[int], all_positions_list:list):
    # key: step, value: range_list
    step_ranges_map = dict()
    step_start, step_end = step_range[0], step_range[1]
    steps = [i for i in range(step_start, step_end)]

    for curr_positions in all_positions_list:
        count_list = __get_count_list(curr_positions)
        __add_current_positions_to_map(steps, count_list, step_ranges_map)

    return step_ranges_map

# FIXME: draw picture of current range_list
def draw_current_rangelist(step_ranges_map:Dict[int, list], step:int, countlist_index:int):
    curr_rangelist = step_ranges_map[step][countlist_index]
    # TODO: draw picture
    # FIXME: not need to return list
    return curr_rangelist

if __name__ == '__main__':
    is_debug = False

    # (1) Read stimuli display
    path = "../displays/"
    filename = "update_stim_info_full.xlsx"
    simuli_df = pd.read_excel(path + filename)

    # (2) Get step_ranges_map: key: step, value: range_list
    step_range = (0, 2)
    all_positions_list = simuli_df.positions_list
    step_ranges_map = get_step_ranges_map(step_range, all_positions_list)

    # (3) Draw picture of current range_list
    curr_step = 1
    curr_countlist_index = 10
    curr_rangelist = draw_current_rangelist(step_ranges_map, curr_step, curr_countlist_index)

    # Optional: only for debug
    if is_debug:
        c_names = get_temp_data(simuli_df)
        # draw_temp(polar) # polar in sub_function cannot run here