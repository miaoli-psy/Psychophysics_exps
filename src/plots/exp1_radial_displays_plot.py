# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-28 14:42
IDE: PyCharm
Introduction:
"""
from typing import Tuple, Dict, List
import matplotlib.pyplot as plt

def draw_ndisc_at_ray(formate_list):
    x_val = [x[0] for x in formate_list]
    y_val = [x[1] for x in formate_list]
    plt.plot(x_val, y_val, 'og')
    plt.show()


# FIXME: draw picture of current range_list
def draw_current_rangelist(step_ranges_map: Dict[int, list], step: int, countlist_index: int):
    curr_rangelist = step_ranges_map[step][countlist_index]
    # TODO: draw picture

    # FIXME: not need to return list
    return curr_rangelist