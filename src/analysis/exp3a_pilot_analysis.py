# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-21 00:08
IDE: PyCharm
Introduction: function to analyze exp3a pilot (online) data
"""


def insert_is_resp_ref_first(ref_first_val: float, key_resp_keys_val: str):
    if ref_first_val == 1.0:
        if key_resp_keys_val == "f":
            return 1
        elif key_resp_keys_val == "j":
            return 0
    elif ref_first_val == 0.0:
        if key_resp_keys_val == "f":
            return 0
        elif key_resp_keys_val == "j":
            return 1
    else:
        raise Exception(f"Invalid ref_first value: {ref_first_val} "
                        f"or Invalid key_resp_keys_val value: {key_resp_keys_val}")


def insert_probeN(D1numerosity: float, D2numerosity: float, ref_first_val: float):
    if ref_first_val == 0.0:
        return D1numerosity
    elif ref_first_val == 1.0:
        return D2numerosity
    else:
        raise ValueError


def insert_refN(D1numerosity: float, D2numerosity: float, ref_first_val: float):
    if ref_first_val == 1.0:
        return D1numerosity
    elif ref_first_val == 0.0:
        return D2numerosity
    else:
        raise ValueError


def insert_refCrowing(D1Crowding: float, D2Crowding: float, ref_first_val: float):
    if ref_first_val == 1.0:
        return D1Crowding
    elif ref_first_val == 0.0:
        return D2Crowding
    else:
        raise ValueError


def inset_probeCrowding(D1Crowding: float, D2Crowding: float, ref_first_val: float):
    if ref_first_val == 0.0:
        return D1Crowding
    elif ref_first_val == 1.0:
        return D2Crowding
    else:
        raise ValueError