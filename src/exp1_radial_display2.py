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

    # start_angle = 0
    # end_angle = 12
    # count = 0
    #
    # res_dict = dict()
    # for index, polar_posi in enumerate(polar_posis):
    #     current_angle = polar_posi[0]
    #     if start_angle <= current_angle <= end_angle:
    #         count += 1
    #     else:
    #         start_angle = current_angle
    #         end_angle = start_angle + 12
    #         if end_angle > 360:
    #             end_angle = end_angle - 360
    #         count = 1
    #     res_dict.update({(start_angle, end_angle): count})


    # range: (real point angle,  real point angle + init_end_angle)
    # def get_all_ranges(angle_range:tuple, polar_posis:list):

    # TODO: Step1: 先成所有你想到的range;
    # TODO: Step2: 写一个函数，得到给定range内的点. if range_start > range_end 特殊处理
    # TODO: 需要全部重新写

    # 起始点尽可能接近0, 即必须满足init_start_angle - diff < 0, otherwise find the smaller init_start_angle
    # range (start_angle, init_start_angle + diff)
    init_start_angle, diff = 0, 12
    start_angle = init_start_angle
    end_angle = init_start_angle + diff

    res_dict = {(start_angle, end_angle): 0}
    # skipped_start_angles: (0, init_start_angle)
    skipped_start_angles = list()
    # skipped_last_angles: (last angle, 0), last angle is the first angle + diff > 360
    skipped_last_angles = list()
    stop_angle = None

    # Step1: (init_start_angle, last start angle)
    # if last start angle + diff > 360 go to step 2
    for index, polar_posi in enumerate(polar_posis):
        current_angle = polar_posi[0]
        # if curr_angle < start_angle, skip it, and count it later
        if current_angle < start_angle:
            skipped_start_angles.append(current_angle)
            continue
        # count posi in range, FIXME: make sure <=, >=, >, <
        elif start_angle <= current_angle <= end_angle:
            res_dict[(start_angle, end_angle)] += 1
        # Get new start, end
        elif current_angle > end_angle:
            start_angle = current_angle
            end_angle = start_angle + diff
            # if > 360, put them into skipped angle and re-count
            if end_angle > 360:
                stop_angle = end_angle - 360
                skipped_last_angles = [posi[0] for posi in polar_posi[index:]]
                break
            # <= 360 Get new start, end
            else:
                # new key
                res_dict[(start_angle, end_angle)] = 1

    # Step2: (last start angle, stop angle), if last start angle + diff > 360
    # stop angle = last start angle + diff
    new_skipped_angles = list()
    if stop_angle:
        # (last start angle, 0)
        res_dict[(start_angle, stop_angle)] = len(skipped_last_angles)

        # (0, stop angle)
        for current_angle in skipped_start_angles:
            if 0 <= current_angle <= stop_angle:
                res_dict[(start_angle, stop_angle)] += 1
            elif current_angle > stop_angle:
                new_skipped_angles.append(current_angle)

    # Step3: (0, init_start_angle) only handle skipped start angles
    if new_skipped_angles and skipped_start_angles:
        skipped_start_angles = new_skipped_angles
    if skipped_start_angles:
        new_start = skipped_start_angles[0]
        new_end = new_start + diff
        res_dict[(new_start, new_end)] = len(skipped_start_angles)



    if is_debug:
        col_names = get_col_names(stimuli_df)