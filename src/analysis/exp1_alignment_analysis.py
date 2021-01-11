# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-11 21:41
IDE: PyCharm
Introduction:
"""
import pandas as pd


def __get_groupby_df(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str):
    return input_df[val_col].groupby(
            [input_df[col_name1], input_df[col_name2], input_df[col_name3]]).mean()


def __convert_index2column(input_df: pd.DataFrame, col_name1: str, col_name2: str, col_name3: str):
    return input_df.reset_index(level = [col_name1, col_name2, col_name3])


def get_data_to_analysis(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str):
    grouped = __get_groupby_df(input_df, val_col, col_name1, col_name2, col_name3)
    return __convert_index2column(grouped, col_name1, col_name2, col_name3)
