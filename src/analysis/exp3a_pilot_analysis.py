# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-21 00:08
IDE: PyCharm
Introduction: function to analyze exp3a pilot (online) data
"""
import pandas as pd


def insert_is_resp_ref_more(ref_first_val: float, key_resp_keys_val: str):
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


def insert_probeCrowding(D1Crowding: float, D2Crowding: float, ref_first_val: float):
    if ref_first_val == 0.0:
        return D1Crowding
    elif ref_first_val == 1.0:
        return D2Crowding
    else:
        raise ValueError


def insert_exp_condition(ref_c: float, probe_c: float):
    if ref_c == 1.0 and probe_c == 1.0:
        return f"rc_pc"
    elif ref_c == 1.0 and probe_c == 0.0:
        return f"rc_pnc"
    elif ref_c == 0.0 and probe_c == 1.0:
        return f"rnc_pc"
    elif ref_c == 0.0 and probe_c == 0.0:
        return f"rnc_pnc"
    else:
        raise Exception(f"condition {ref_c, probe_c}not in defined experiment conditions")


def cal_one_minus_value(input_value: float) -> float:
    return 1 - input_value


def get_output_results(input_df: pd.DataFrame) -> pd.DataFrame:
    output_results = input_df['is_resp_ref_more'].groupby(
            [input_df["ref_first"], input_df["participantN"],input_df["probeN"],input_df["ref_probe_condi"]]).mean()
    output_results = output_results.unstack().unstack()
    return output_results


def get_piovt_table(input_df: pd.DataFrame) -> pd.DataFrame:
    pivot_table = pd.pivot_table(input_df,
                                 index = ["ref_first", "participantN"],
                                 columns = ["ref_probe_condi", "probeN"],
                                 values = ["is_resp_ref_more"])
    return pivot_table




