# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-14 20:21
IDE: PyCharm
Introduction:
"""
import pandas as pd
from collections import Counter

from src.analysis.exp1_raidal_displays_analysis2 import get_angle_range, count_ndisc_in_range, get_beam_n, counter2list, \
    cal_alignment_value
from src.commons.process_dataframe import get_col_names
from src.commons.process_str import str_to_list
from src.point.polar_point import get_polar_coordinates


is_debug = True
indi_display = True
write_to_excel = True

# read stimuli display
PATH = "../displays/"
FILENAME = "update_stim_info_full.xlsx"
stimuli_df = pd.read_excel(PATH + FILENAME)
# get and insert new col "n_beams" into stimuli dataframe
# number of beams that contains 1, 2, 3, 4, 5, 6 disc
stimuli_df["beam_n_size12"] = stimuli_df["positions_list"].apply(get_beam_n, args = (12,))
stimuli_df["beam_n_size6"] = stimuli_df["positions_list"].apply(get_beam_n, args = (6,))
stimuli_df["beam_n_size3"] = stimuli_df["positions_list"].apply(get_beam_n, args = (3,))
# weight for each value
weight = [0, 0, 3, 4, 5, 6]
# cal alignment values
stimuli_df["align_v_size12"] = stimuli_df["beam_n_size12"].apply(cal_alignment_value,
                                                                 args = (weight, False))
stimuli_df["align_v_size12_count"] = stimuli_df["beam_n_size12"].apply(cal_alignment_value,
                                                                       args = (weight, True))
stimuli_df["align_v_size6"] = stimuli_df["beam_n_size6"].apply(cal_alignment_value,
                                                               args = (weight, False))
stimuli_df["align_v_size6_count"] = stimuli_df["beam_n_size6"].apply(cal_alignment_value,
                                                                     args = (weight, True))
stimuli_df["align_v_size3"] = stimuli_df["beam_n_size3"].apply(cal_alignment_value,
                                                               args = (weight, False))
stimuli_df["align_v_size3_count"] = stimuli_df["beam_n_size3"].apply(cal_alignment_value,
                                                                     args = (weight, True))
# individual display alignment value
if indi_display:
    display_n = 120  # 0-249
    posis_str = stimuli_df.positions_list[display_n]
    posis = str_to_list(posis_str)
    # get polar positions for a single display
    polar_posis = get_polar_coordinates(posis)

    # some parameters, started and ended where
    ini_start_angle = polar_posis[0][0]
    angle_size = 3
    ini_end_angle = ini_start_angle + angle_size
    # get the ranges
    my_range = get_angle_range(polar_posis, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
    # get number of discs in each range
    ndisc_list = list()
    for beam in my_range:
        ndisc = count_ndisc_in_range(polar_posis, beam[0], beam[1])
        ndisc_list.append(ndisc)
    # get number of beams that contains 1, 2, 3, 4, 5, 6 discs
    count_beams = Counter(ndisc_list)
    n_beams6 = counter2list(count_beams)

if is_debug:
    col_names = get_col_names(stimuli_df)

if write_to_excel:
    stimuli_df.to_excel("try.xlsx")