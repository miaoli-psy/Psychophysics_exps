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


def draw_ndisc_at_ray(formate_list, xlabel = "theta", ylabel = "Number of discs at alone the line", style = "og"):
    ax = plt.subplot()
    x_val = [x[0] for x in formate_list]
    y_val = [x[1] for x in formate_list]
    ax.plot(x_val, y_val, style)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

