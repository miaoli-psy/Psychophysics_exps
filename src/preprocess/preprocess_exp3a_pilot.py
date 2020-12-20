# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-20 21:07
IDE: PyCharm
Introduction: functions for preprocessed data of crowding and numerosity exp3a (online pilot)
"""
from src.preprocess.sub import merge_all_data
import pandas as pd
import copy
import math


def preprocess_exp3a_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


def keep_valid_columns(df: pd.DataFrame, kept_columns_list: list) -> pd.DataFrame:
    all_col_name_list = list(df.columns)
    all_col_name_copy_list = copy.deepcopy(all_col_name_list)
    drop_name_list = list()
    for name in all_col_name_copy_list:
        if name not in kept_columns_list:
            drop_name_list.append(name)
    df = df.drop(drop_name_list, axis = 1)
    return df


def drop_df_nan_rows_according2cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    :param df:
    :param cols: list of column names that dropna applied on
    :return:
    """
    df = df.dropna(subset = cols)
    return df


def drop_df_rows_according2_one_col(df: pd.DataFrame, col_name: str, lowerbondary: float,
                                    upperbondary: float) -> pd.DataFrame:
    """
    :param df:
    :param col:  column name(str)
    :param lowerbondary:
    :param upperbondary:
    :return:
    """
    df = df[(df[col_name] < upperbondary) & (df[col_name] > lowerbondary)]
    return df


def __cal_std_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    std = df[col_name].std()
    return std


def __cal_mean_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    mean = df[col_name].mean()
    return mean


def get_col_boundary(df: pd.DataFrame, col_name: str, n_std = 2) -> tuple:
    mean = __cal_mean_of_one_col(df, col_name)
    std = __cal_std_of_one_col(df, col_name)
    return mean - n_std * std, mean + n_std * std