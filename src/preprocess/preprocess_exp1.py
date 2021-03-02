# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 21:35
IDE: PyCharm
Introduction:
"""
from src.commons.process_dataframe import keep_valid_columns, get_sub_df_according2col_value, insert_new_col, \
    rename_df_col, change_col_value_type, insert_new_col_from_two_cols
from src.commons.process_str import imageFile_to_number2, imageFile_to_number
from src.constants.exp1_constants import KEPT_COL_NAMES_exp1
from src.preprocess.sub import merge_all_data
import pandas as pd

from src.preprocess.sub.get_data2analysis import drop_df_rows_according2_one_col


def preprocess_exp1rerun_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


def get_std(df: pd.DataFrame, col_name: str):
    return df[col_name].std()


def get_mean(df: pd.DataFrame, col_name: str):
    return df[col_name].mean()


def get_deviation(resp: int, numerosity: int) -> int:
    return resp - numerosity


if __name__ == '__main__':
    write_to_excel = True
    DATA_PATH = "../../data/exp1_rerun_data/rawdata/"
    FILENAME_PREFIX = "a"
    FILETYPE = ".csv"

    # read raw data
    all_df = preprocess_exp1rerun_func(DATA_PATH, FILETYPE, FILENAME_PREFIX)

    # preprocess
    all_df = keep_valid_columns(all_df, KEPT_COL_NAMES_exp1)

    # drop obvious wrong response
    col_to_drop_rows = "response"
    min_res = 10
    max_res = 100
    all_df = drop_df_rows_according2_one_col(all_df, col_to_drop_rows, min_res, max_res)

    # drop response outside 3 strd
    n_discs = [21, 22, 23, 24, 25,
               31, 32, 33, 34, 35,
               41, 42, 43, 44, 45,
               49, 50, 51, 52, 53,
               54, 55, 56, 57, 58]

    df_list = [get_sub_df_according2col_value(all_df, "Numerosity", n) for n in n_discs]

    col_to_process = "response"
    prepro_df_list = list()
    for sub_df in df_list:
        lower_bondary = get_mean(sub_df, col_to_process) - 3 * get_std(sub_df, col_to_process)
        upper_bondary = get_mean(sub_df, col_to_process) + 3 * get_std(sub_df, col_to_process)
        new_sub_df = drop_df_rows_according2_one_col(sub_df, col_to_process, lower_bondary, upper_bondary)
        prepro_df_list.append(new_sub_df)
    mydata = pd.concat(prepro_df_list, ignore_index = True)

    # add columns/rename columns
    insert_new_col(mydata, "Display", "winsize", imageFile_to_number2)
    insert_new_col(mydata, "Display", "index_stimuliInfo", imageFile_to_number)
    rename_df_col(mydata, "Numerosity", "N_disk")
    rename_df_col(mydata, "Crowding", "crowdingcons")
    # deviation
    insert_new_col_from_two_cols(mydata, "response", "N_disk", "deviation_score", get_deviation)
    # make sure col val type
    change_col_value_type(mydata, "crowdingcons", int)
    change_col_value_type(mydata, "winsize", float)
    change_col_value_type(mydata, "index_stimuliInfo", str)
    change_col_value_type(mydata, "N_disk", int)

    # write to excel
    if write_to_excel:
        mydata.to_excel("try.xlsx")