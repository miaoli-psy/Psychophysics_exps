# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:15:04 2020

@author: Miao
"""
import os, math
import pandas as pd

from src.commons.process_dataframe import get_col_names, get_sub_df_according2col_value
from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col


def get_std(df: pd.DataFrame, col_name: str):
    return df[col_name].std()


def get_mean(df: pd.DataFrame, col_name: str):
    return df[col_name].mean()


if __name__ == '__main__':
    debug = False
    write_to_excel = False

    # read the totalData file
    all_df = pd.read_excel('../../data/exp2_data_online/clean_totalData.xlsx', index_col = 0)

    # drop obvious wrong response
    col_to_drop_rows = "responseN"
    min_res = 10
    max_res = 100
    all_df = drop_df_rows_according2_one_col(all_df, col_to_drop_rows, min_res, max_res)

    # drop outside 3 strd
    n_discs = [34, 36, 38, 40, 42, 44,
               58, 60, 62, 64, 66, 68]

    df_list = [get_sub_df_according2col_value(all_df, "Numerosity", n) for n in n_discs]

    col_to_process = "responseN"
    prepro_df_list = list()
    for numerosity, sub_df in zip(n_discs, df_list):
        lower_bondary = get_mean(sub_df, col_to_process) - 3 * get_std(sub_df, col_to_process)
        upper_bondary = get_mean(sub_df, col_to_process) + 3 * get_std(sub_df, col_to_process)
        new_sub_df = drop_df_rows_according2_one_col(sub_df, col_to_process, lower_bondary, upper_bondary)
        prepro_df_list.append(new_sub_df)

    mydata = pd.concat(prepro_df_list, ignore_index = True)

    if write_to_excel:
        mydata.to_excel('try.xlsx')

    if debug:
        col_names = get_col_names(all_df)
