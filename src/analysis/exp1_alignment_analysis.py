# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-11 21:41
IDE: PyCharm
Introduction:
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.commons.process_dataframe import get_sub_df_according2col_value


def add_color_code_by_crowdingcons(crowding_cons: str):
    if crowding_cons == 0:
        return "royalblue"
    elif crowding_cons == 1:
        return "orangered"
    else:
        raise Exception(f"crowding_cons == {crowding_cons} is not recognized. O for no-crowding, 1 for crowding")


def add_color_code_by_winsize(N_disk: str):
    if 21 <= N_disk <= 25:
        return "cornflowerblue"
    elif 31 <= N_disk <= 35:
        return "orange"
    elif 41 <= N_disk <= 45:
        return "limegreen"
    elif 49 <= N_disk <= 53:
        return "red"
    elif 54 <= N_disk <= 58:
        return "mediumpurple"
    else:
        raise Exception(f"N_disk == {N_disk} is not recognized. 24-25, 31-35, 41-45, 49-53, 54-58 are allowed")


def get_analysis_dataframe(my_data, crowding):
    if crowding == 1:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 1)
    elif crowding == 0:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 0)
    elif crowding == 2:
        return my_data
    else:
        raise Exception(f"crowding == {crowding} is not recognized. 0 for no-crowding, 1 for crowding, 2 for all")


def __get_groupby_df(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str,
                     col_name4: str):
    return input_df[val_col].groupby(
            [input_df[col_name1], input_df[col_name2], input_df[col_name3], input_df[col_name4]]).mean()


def __convert_index2column(input_df: pd.DataFrame, col_name1: str, col_name2: str, col_name3: str, col_name4: str):
    return input_df.reset_index(level = [col_name1, col_name2, col_name3, col_name4])


def get_data_to_analysis(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str,
                         col_name4: str):
    grouped = __get_groupby_df(input_df, val_col, col_name1, col_name2, col_name3, col_name4)
    return __convert_index2column(grouped, col_name1, col_name2, col_name3, col_name4)


def normalize_deviation(input_df: pd.DataFrame):
    """
    :param input_df:dataframe contains col "deviation_score"
    :return: new dataframe contains only normalized "deviation_score" range within(-1, 1)
    """
    min_max_scaler = MinMaxScaler(feature_range = (-1, 1))
    return pd.DataFrame(min_max_scaler.fit_transform(input_df[["deviation_score"]]), columns = ["deviation_score"])


def normalize_alignment_v(input_df: pd.DataFrame, alignment_col: str):
    """
    :param input_df: dataframe contains col alignment values
    :param alignment_col: alignment_col name
    :return: new dataframe contains only normalized alignment_col range within(0, 1)
    """
    min_max_scaler = MinMaxScaler(feature_range = (0, 1))
    return pd.DataFrame(min_max_scaler.fit_transform(input_df[[alignment_col]]), columns = [alignment_col])


def rename_norm_col(input_df: pd.DataFrame, old_name: str, new_name: str):
    return input_df.rename(columns = {old_name: new_name})
