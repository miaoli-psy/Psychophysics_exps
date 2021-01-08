# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-08 18:29
IDE: PyCharm
Introduction:
"""


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


