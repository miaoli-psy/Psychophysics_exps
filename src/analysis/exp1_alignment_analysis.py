# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-11 21:41
IDE: PyCharm
Introduction:
"""
import pandas as pd

from src.commons.process_dataframe import get_sub_df_according2col_value


def add_color_code(crowding_cons: str):
    if crowding_cons == 0:
        return "royalblue"
    elif crowding_cons == 1:
        return "orangered"
    else:
        raise Exception(f"crowding_cons == {crowding_cons} is not recognized. O for no-crowding, 1 for crowding")


def get_analysis_dataframe(my_data, crowding):
    if crowding == 1:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 1)
    elif crowding == 0:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 0)
    elif crowding == 2:
        return my_data
    else:
        raise Exception(f"crowding == {crowding} is not recognized. 0 for no-crowding, 1 for crowding, 2 for all")


def __get_groupby_df(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str, col_name4: str):
    return input_df[val_col].groupby(
            [input_df[col_name1], input_df[col_name2], input_df[col_name3], input_df[col_name4]]).mean()


def __convert_index2column(input_df: pd.DataFrame, col_name1: str, col_name2: str, col_name3: str, col_name4: str):
    return input_df.reset_index(level = [col_name1, col_name2, col_name3, col_name4])


def get_data_to_analysis(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str, col_name4: str):
    grouped = __get_groupby_df(input_df, val_col, col_name1, col_name2, col_name3, col_name4)
    return __convert_index2column(grouped, col_name1, col_name2, col_name3, col_name4)