# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-08 18:29
IDE: PyCharm
Introduction:
"""
import numpy as np
import copy
from src.commons.fitfuncs import fit_poisson_cdf
from src.commons.process_number import cal_eccentricity


def __pix_to_deg_tuple(input_tuple, changeN = 1, k = 3.839 / 100):
    if changeN == 1:
        return round(input_tuple[0] * k, 4), input_tuple[1]
    elif changeN == 2:
        return round(input_tuple[0] * k, 4), round(input_tuple[1] * k, 4)
    else:
        raise Exception(f"changeN {changeN} should be 1 or 2")


def dict_pix_to_deg(input_dict, changeN):
    """Convert pix to deg for a given dictionary format,
    changeN is 1 or 2, to let the function works for the first
    or both elements of the tuple"""
    dict_deg = {}
    for key, values in input_dict.items():
        new_display = []
        for display in values:
            new_posi = []
            for posi in display:
                new_posi.append(__pix_to_deg_tuple(posi, changeN))
            new_display.append(new_posi)
        dict_deg.update({key: new_display})
    return dict_deg


def avrg_dict_pix_to_deg(input_dict, changeN):
    """Convert pix to deg for a given dictionary format,
    changeN is 1 or 2, to let the function works for the first
    or both elements of the tuple"""
    dict_deg = {}
    for key, display in input_dict.items():
        new_posi = []
        for posi in display:
            new_posi.append(__pix_to_deg_tuple(posi, changeN))
        dict_deg.update({key: new_posi})
    return dict_deg

def __max_eccentricities(dis_list):
    """returns the max_x_axis and the corrosponding posi"""
    e = []
    for posi in dis_list:
        e_temp = cal_eccentricity(posi)
        e.append(e_temp)
    # this only give the index of one posi, it my have more posis that are all max...
    # doens't matter in this case.
    max_posi = dis_list[e.index(max(e))]
    max_x_axis = int(max(e))
    # min_posi = dis_list[e.index(min(e))]
    return max_x_axis, max_posi


def __get_point_number(x_axis: int, list_point: list):
    """for each x-axis, calculate the number of discs"""
    number = 0
    points = []
    for point in list_point:
        if cal_eccentricity((x_axis, 0)) >= cal_eccentricity(point):
            number += 1
            points.append(point)
    return number, points


def __get_x_y(list_point: list) -> list:
    x_max = abs(__max_eccentricities(list_point)[0])
    list_result, y = [], 0
    for x in range(int(x_max) + 2):
        new_y, points = __get_point_number(x, list_point)
        if new_y != y:
            y = new_y
            list_result.append((x, y))
            # For degug: see the x,y point details
            # print("x,y: " ,x, ",",y, "points: ", points)
    return list_result


def get_result_dict(posis_dict):
    """calculates the local density"""
    result_dict = {}
    for key, posis in posis_dict.items():
        result_list_t = []
        for posi in posis:
            result_t = __get_x_y(posi)
            result_list_t.append(result_t)
        result_dict.update({key: result_list_t})
    return result_dict


def get_avrg_result_dict(posis_dict):
    result_dict = dict()
    for key, posi in posis_dict.items():
        result_t = __get_x_y(posi)
        result_dict.update({key: result_t})
    return result_dict


def interplote_result_dict_start(result_dict: dict) -> dict:
    """make sure every display local density starts from (100,...)"""
    for key, values in result_dict.items():
        for value in values:
            if value[0][0] != 100:
                value.insert(0, (100, 0))
    return result_dict


def interplote_avrg_result_dict_start(result_dict: dict) -> dict:
    """make sure every display local density starts from (100,...)"""
    for key, value in result_dict.items():
        if value[0][0] != 100:
            value.insert(0, (100, 0))
    return result_dict


def normolizedLD(y_val: list):
    return [float(i) / max(y_val) for i in y_val]


def get_fitted_res_cdf_poisson(input_dict) -> list:
    res_list = list()
    for numerosity, loc_density_list in input_dict.items():
        for loc_density in loc_density_list:
            x_value = list()
            y_value = list()
            for loc_tuple in loc_density:
                x_value.append(loc_tuple[0])
                y_value.append(loc_tuple[1])
            np_array = np.array([x_value, normolizedLD(y_value)]).transpose()
            res_list.append(fit_poisson_cdf(np_array))
    return res_list


def get_data2fit(input_list):
    x_value = [loc_tuple[0] for loc_tuple in input_list]
    y_value = [loc_tuple[1] for loc_tuple in input_list]
    np_array = np.array([x_value, normolizedLD(y_value)]).transpose()
    return np_array


def get_data_to_fit_list(input_list):
    data_to_fit = copy.deepcopy(input_list)
    for curr_dict in data_to_fit:
        for k, v_s in curr_dict.items():
            new_v = [get_data2fit(v) for v in v_s]
            curr_dict[k] = new_v
    return data_to_fit


def get_avrg_data_to_fit(input_dict):
    data_to_fit = copy.deepcopy(input_dict)
    for k, v in data_to_fit.items():
        new_v = get_data2fit(v)
        data_to_fit[k] = new_v
    return data_to_fit


def get_fitted_power_list(inputlist, deg = 2):
    fitted_power_list = copy.deepcopy(inputlist)
    for index, curr_dict in enumerate(fitted_power_list):
        for k, v_s in curr_dict.items():
            new_v = [np.polyfit(x = v[:, 0], y = v[:, 1], deg = deg)[0] for v in v_s]
            curr_dict[k] = new_v
    return fitted_power_list


def get_data_to_ttest(inputlist):
    ttest_data = list()
    for curr_dict in inputlist:
        curr_list = list()
        for v_list in curr_dict.values():
            curr_list += v_list
        ttest_data.append(curr_list)
    return ttest_data


def get_sample_plot_x_y(input_dict, key, list_index):
    x, y = list(), list()
    for loc_tuple in input_dict[key][list_index]:
        x.append(loc_tuple[0])
        y.append(loc_tuple[1])
    return np.array([x, normolizedLD(y)]).transpose()


def get_avrg_dict(inpudict):
    """This function returns the accumulation display that contain the same numerosity
    eg. 5 displays with numerosity 21 --> 1 display contains 105 discs"""
    avrg_dic = {}
    for numerosity, lists in inpudict.items():
        avrg_nmrsty = []
        for plist in lists:
            for posi in plist:
                avrg_nmrsty.append(posi)
        avrg_dic.update({numerosity: avrg_nmrsty})
    return avrg_dic