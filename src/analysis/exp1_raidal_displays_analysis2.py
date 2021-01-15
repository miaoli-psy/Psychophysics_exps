# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-15 17:26
IDE: PyCharm
Introduction:
"""


def get_angle_range(polar_posi_list, ini_start_angle = 0, ini_end_angle = 12):
    """
    :param polar_posi_list: a list of polar positions
    :param ini_start_angle: the first beam start edge, where to start
    :param ini_end_angle: : the first beam end edge
    :return: a list of range (place holder)
    """
    angle_size = ini_end_angle - ini_start_angle
    range_list = [(ini_start_angle, ini_end_angle)]

    start_angle = ini_start_angle
    for polar_posi in polar_posi_list:
        if polar_posi[0] > start_angle:
            start_angle = polar_posi[0]
            end_angle = start_angle + angle_size
            if end_angle < 360:
                range_list.append((start_angle, end_angle))
            if end_angle > 360:
                range_list.append((start_angle, end_angle - 360))
                break
    return range_list


def count_ndisc_in_range(polar_posi_list, range_start, range_end):
    """
    :param polar_posi_list: a list of polar positions
    :param range_start: angle of the starting edge
    :param range_end: angle of the ending edge
    :return: the number of discs within the region
    """
    if range_start < range_end:
        count = 0
        for polar_posi in polar_posi_list:
            if range_start <= polar_posi[0] < range_end:
                count += 1
        return count
    else:
        count = 0
        for polar_posi in polar_posi_list:
            if range_start <= polar_posi[0] < 360:
                count += 1
                print(polar_posi)
            elif 0 <= polar_posi[0] < range_end:
                count += 1
                print(polar_posi)
    return count