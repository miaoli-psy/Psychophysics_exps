# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-02-01 15:03
IDE: PyCharm
Introduction: Calculate partial corr between deviation score and number of discs' into others crowding zones.
Polt the parr corr results

"""
import pandas as pd
import pingouin as pg

from src.analysis.exp1_alignment_analysis import add_color_code_by_crowdingcons, add_color_code_5levels, \
    get_analysis_dataframe, get_data_to_analysis, normalize_deviation, normalize_zerotoone, rename_norm_col
from src.commons.process_dataframe import keep_valid_columns, insert_new_col, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF2, KEPT_COL_NAMES3

if __name__ == '__main__':
    is_debug = True
    winsize_list = [0.3, 0.4, 0.5, 0.6, 0.7]
    # TODO set parameters
    crowdingcons = 2  # 0, 1, 2 for no-crowding, crowding and all
    # read stimuli info and data
    PATH_DATA = "../data/exp1_rerun_data/"
    STIM_PATH = "../displays/"
    FILENAME_DATA = "cleanedTotalData_fullinfo_v2.xlsx"
    FILENAME_STIM = "update_stim_info_full.xlsx"
    data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)
    stim_to_merge = pd.read_excel(STIM_PATH + FILENAME_STIM)
    stimuli_to_merge = keep_valid_columns(stim_to_merge, KEPT_COL_NAMES_STIMU_DF2)
    # merge data with stimuli info
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = "left",
                      on = ["index_stimuliInfo", "N_disk", "crowdingcons", "winsize"])
    # %% preprocess
    my_data = keep_valid_columns(all_df, KEPT_COL_NAMES3)
    # add color coded for crowding and no-crowding displays
    insert_new_col(my_data, "crowdingcons", 'colorcode', add_color_code_by_crowdingcons)
    # color coded
    insert_new_col_from_two_cols(my_data, "N_disk", "crowdingcons", "colorcode5levels", add_color_code_5levels)
    # %% correlations
    my_data = get_analysis_dataframe(my_data, crowding = crowdingcons)
    # data for each winsize
    df_list = [get_sub_df_according2col_value(my_data, "winsize", winsize) for winsize in winsize_list]
    df_list = [get_data_to_analysis(df, "deviation_score", "count_number", "N_disk", "list_index", "colorcode",
                                    "colorcode5levels") for df in df_list]
    # partial corr parameters
    method = "pearson"
    x = "count_number"
    y = "deviation_score"
    covar = "N_disk"
    partial_corr_res_list = [pg.partial_corr(df, x = x, y = y, covar = covar, method = method) for df in df_list]
    # %% normalization
    df_list_norm_deviation = [normalize_deviation(df) for df in df_list]
    df_list_norm_countn = [normalize_zerotoone(df, to_normalize_col = "count_number") for df in df_list]
    # rename normed cols
    old_name_dev = "deviation_score"
    new_name_dev = "deviation_score_norm"
    old_name_countn = "count_number"
    new_name_countn = "count_number_norm"
    df_list_norm_deviation = [rename_norm_col(df, old_name_dev, new_name_dev) for df in df_list_norm_deviation]
    df_list_norm_countn = [rename_norm_col(df, old_name_countn, new_name_countn) for df in df_list_norm_countn]
    # contact orig dataframe with new normalized dataframe
    df_list = [pd.concat([df, df_list_norm_deviation[index], df_list_norm_countn[index]], axis = 1) for index, df in
               enumerate(df_list)]
    # %% cal residuals (to plot)


    if is_debug:
        col_names = list(all_df.columns)