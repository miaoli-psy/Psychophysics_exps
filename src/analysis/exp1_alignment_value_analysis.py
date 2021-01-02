# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 22:27
IDE: PyCharm
Introduction:
"""
import pandas as pd


def get_pivot_table(input_df: pd.DataFrame, index, columns, values) -> pd.DataFrame:
    """
    :param input_df:
    :param index, cp;imns and values: list of strs - df col names
    :return: pivot table
    """
    pivot_table = pd.pivot_table(input_df,
                                 index = index,
                                 columns = columns,
                                 values = values)
    return pivot_table
