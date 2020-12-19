# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 23:18
IDE: PyCharm
Introduction:
"""

from scr.preprocess import preprocess_exp3a_pilot


data_path = "../data/rawdata_exp3a_pilot/"
filename_prefix = "P"
filetype = ".csv"
all_df = preprocess_exp3a_pilot.preprocess_exp3a_func(data_path, filetype, filename_prefix)