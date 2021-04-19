# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-04-19 16:30
IDE: PyCharm
Introduction:
"""
from src.commons.process_dataframe import get_sub_df_according2col_value


def cal_ds_mean(df, crowdingcon, col_name = "crowdingcons"):
    """
    calculate
    """
    if crowdingcon == 1:
        return get_sub_df_according2col_value(df, col_name, 1).mean()
    elif crowdingcon == 0:
        return get_sub_df_according2col_value(df, col_name, 0).mean()
    elif crowdingcon == 2:
        return get_sub_df_according2col_value(df, col_name, 2).mean()
    else:
        Exception(f"crowdingcon = {crowdingcon} is not recognized, use 1 or 0 or 2")


def cal_ds_std(df, crowdingcon, col_name = "crowdingcons"):
    if crowdingcon == 1:
        return get_sub_df_according2col_value(df, col_name, 1).std()
    elif crowdingcon == 0:
        return get_sub_df_according2col_value(df, col_name, 0).std()
    elif crowdingcon == 2:
        return get_sub_df_according2col_value(df, col_name, 2).std()
    else:
        Exception(f"crowdingcon = {crowdingcon} is not recognized, use 1 or 0 or 2")