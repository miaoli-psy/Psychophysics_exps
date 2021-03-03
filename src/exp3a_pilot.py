# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 23:18
IDE: PyCharm
Introduction:
"""
from src.constants.exp3a_pilot_constants import KEPT_COL_NAMES, SUB_DF_COLS2CHECK
from src.plots.exp3a_pilot_plot import drawplot
from src.preprocess.preprocess_exp3a_pilot import preprocess_exp3a_func
from src.preprocess.sub.get_data2analysis import drop_df_nan_rows_according2cols, drop_df_rows_according2_one_col, \
    get_col_boundary
from src.commons.process_dataframe import insert_new_col_from_two_cols, insert_new_col_from_three_cols, \
    get_sub_df_according2col_value, process_cols, process_col, insert_new_col, get_processed_cols_df, keep_valid_columns
from src.analysis.exp3a_pilot_analysis import insert_is_resp_ref_more, insert_probeN, insert_refN, \
    insert_refCrowing, cal_one_minus_value, get_output_results, get_piovt_table, \
    insert_exp_condition, insert_probeCrowding

if __name__ == "__main__":
    is_debug = True
    write_to_excel = False
    save_plots = False
    DATA_PATH = "../data/exp3_data/exp3_pilot_data/rawdata/"
    FILENAME_PREFIX = "P"
    FILETYPE = ".csv"
    # %% preprocess starts here
    all_df = preprocess_exp3a_func(DATA_PATH, FILETYPE, FILENAME_PREFIX)
    all_df = keep_valid_columns(all_df, KEPT_COL_NAMES)

    # drop practice trials: drop all rows with NaNs in key_resp.keys
    col_to_dropna = ['key_resp.keys']
    all_df = drop_df_nan_rows_according2cols(all_df, col_to_dropna)

    # drop too fast and too slow response
    col_to_drop_rows = "key_resp.rt"
    min_rt = 0.15
    max_rt = 3
    all_df = drop_df_rows_according2_one_col(all_df, col_to_drop_rows, min_rt, max_rt)

    # drop response that are outside 3 standard deviation
    col_rt = "key_resp.rt"
    boundary = get_col_boundary(all_df, col_rt)
    resp_min = boundary[0]
    resp_max = boundary[1]
    # preprocessed data
    all_df = drop_df_rows_according2_one_col(all_df, col_rt, resp_min, resp_max)

    # %% analysis starts here
    # add numerosity difference between D1 and D2
    all_df["dff_D1D2"] = all_df["D1numerosity"] - all_df["D2numerosity"]
    # add correct answer
    insert_new_col_from_two_cols(all_df, "ref_first", "key_resp.keys", "is_resp_ref_more", insert_is_resp_ref_more)
    # add probe numerosity
    insert_new_col_from_three_cols(all_df, "D1numerosity", "D2numerosity", "ref_first", "probeN", insert_probeN)
    # add ref numerosity
    insert_new_col_from_three_cols(all_df, "D1numerosity", "D2numerosity", "ref_first", "refN", insert_refN)
    # add probe crowding condition
    insert_new_col_from_three_cols(all_df, "D1Crowding", "D2Crowding", "ref_first", "probeCrowding",
                                   insert_probeCrowding)
    # add ref crowding condition
    insert_new_col_from_three_cols(all_df, "D1Crowding", "D2Crowding", "ref_first", "refCrowding", insert_refCrowing)

    # %% experiment conditions
    # indicate different condition with extra columns
    insert_new_col_from_two_cols(all_df, "ref_c", "probe_c", "ref_probe_condi", insert_exp_condition)

    # exp conditions in separate df for plots
    refc = get_sub_df_according2col_value(all_df, "refCrowding", 1)
    refnc = get_sub_df_according2col_value(all_df, "refCrowding", 0)
    # below are four exp conditions
    refcprobec = get_sub_df_according2col_value(refc, "probeCrowding", 1)
    refcprobenc = get_sub_df_according2col_value(refc, "probeCrowding", 0)
    refncprobec = get_sub_df_according2col_value(refnc, "probeCrowding", 1)
    refncprobenc = get_sub_df_according2col_value(refnc, "probeCrowding", 0)

    # %% output dataframe
    # pivot table
    pt = get_piovt_table(all_df)
    # groupby()
    results_df = get_output_results(all_df)
    # add means of result_df
    results_df.loc["mean_across_all_participants"] = results_df.mean()
    # add means across participants by different group (ref first or not)
    results_df.loc["mean_of_probe_first_participants"] = results_df.iloc[0:5].mean()
    results_df.loc["mean_of_ref_first_participants"] = results_df.iloc[6:11].mean()

    # %% plots
    x_values = [34, 36, 38, 40, 42, 44, 46]
    condi_list = ["rc_pc", "rc_pnc", "rnc_pc", "rnc_pnc"]

    # %% debug and output
    if is_debug:
        col_names = list(all_df.columns)
        df2check = all_df[SUB_DF_COLS2CHECK]

    if write_to_excel:
        all_df.to_excel("preprocess_exp3a_pilot.xlsx")
        pt.to_excel("pivot_table_exp3a_pilot.xlsx")

    if save_plots:
        # row number: possible 0-14; 0-11 (12 participants) 12 all participants, 13 probe first group, 14 ref first
        # group
        for row in range(15):
            drawplot(results_df, x_values, condi_list, row_number = row)
