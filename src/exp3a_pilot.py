# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 23:18
IDE: PyCharm
Introduction:
"""

from src.preprocess.preprocess_exp3a_pilot import preprocess_exp3a_func, keep_valid_columns, \
    drop_df_nan_rows_according2cols, drop_df_rows_according2_one_col, get_col_boundary
from src.commons.process_dataframe import insert_new_col_from_two_cols, insert_new_col_from_three_cols
from src.analysis.exp3a_pilot_analysis import insert_is_resp_ref_first, insert_probeN, insert_refN

if __name__ == "__main__":
    is_debug = True
    write_to_excel = False
    data_path = "../data/rawdata_exp3a_pilot/"
    filename_prefix = "P"
    filetype = ".csv"
    kept_col_names = ["D1",
                      "D1Crowding",
                      "D1Ndisplay",
                      "D1aggregateSurface",
                      "D1averageE",
                      "D1avg_spacing_c",
                      "D1convexHull_perimeter",
                      "D1density",
                      "D1density_itemsperdeg2",
                      "D1mirror",
                      "D1numerosity",
                      "D1occupancyArea",
                      "D1ref",
                      "D1rotate",
                      "D2",
                      "D2Crowding",
                      "D2Ndisplay",
                      "D2aggregateSurface",
                      "D2averageE",
                      "D2avg_spacing_c",
                      "D2convexHull_perimeter",
                      "D2density",
                      "D2density_itemsperdeg2",
                      "D2mirror",
                      "D2numerosity",
                      "D2occupancyArea",
                      "D2ref",
                      "D2rotate",
                      "group",
                      "key_resp.keys",
                      "key_resp.rt",
                      "participantN",
                      "probe_c",
                      "ref_c",
                      "ref_first"]
    #%% preprocess starts here
    all_df = preprocess_exp3a_func(data_path, filetype, filename_prefix)
    all_df = keep_valid_columns(all_df, kept_col_names)

    # drop practice trials: drop all rows with NaNs in key_resp.keys
    col_to_dropna = ['key_resp.keys']
    all_df = drop_df_nan_rows_according2cols(all_df, col_to_dropna)

    # drop too fast and too slow response
    col_to_drop_rows = "key_resp.rt"
    min_rt = 0.15
    max_rt = 3
    all_df = drop_df_rows_according2_one_col(all_df, col_to_drop_rows, min_rt, max_rt)

    # drop response that are outside 2 standard deviation
    col_rt = "key_resp.rt"
    boundary = get_col_boundary(all_df, col_rt)
    resp_min = boundary[0]
    resp_max = boundary[1]
    # preprocessed data
    all_df = drop_df_rows_according2_one_col(all_df, col_rt, resp_min, resp_max)

    #%% analysis starts here
    # add numerosity difference between D1 and D2
    all_df["dff_D1D2"] = all_df["D1numerosity"] - all_df["D2numerosity"]
    # add correct answer
    insert_new_col_from_two_cols(all_df, "ref_first", "key_resp.keys", "is_resp_ref_first", insert_is_resp_ref_first)
    # add probe numerosity
    insert_new_col_from_three_cols(all_df, "D1numerosity", "D2numerosity", "ref_first", "probeN", insert_probeN)
    # add ref numerosity
    insert_new_col_from_three_cols(all_df, "D1numerosity", "D2numerosity", "ref_first", "refN", insert_refN)

    #%% debug and output
    if is_debug:
        col_names = list(all_df.columns)
        added_probe_df = all_df[["D1numerosity", "D2numerosity", "ref_first", "probeN", "refN"]]

    if write_to_excel:
        all_df.to_excel("preprocess_exp3a_pilot.xlsx")