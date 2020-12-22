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
from src.commons.process_dataframe import insert_new_col_from_two_cols, insert_new_col_from_three_cols, \
    get_sub_df_according2col_value, process_cols, process_col, insert_new_col, get_processed_cols_df
from src.analysis.exp3a_pilot_analysis import insert_is_resp_ref_more, insert_probeN, insert_refN, \
    insert_refCrowing, cal_one_minus_value, get_output_results, get_piovt_table, \
    insert_exp_condition, insert_probeCrowding
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm
import matplotlib.pyplot as plt

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
    # %% preprocess starts here
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

    # %% output data
    pt = get_piovt_table(all_df)

    # to_minus_one_cols = refnc_problenc_results.columns
    # processed_refnc_problenc_results = get_processed_cols_df(refnc_problenc_results, to_minus_one_cols, cal_one_minus_value)

    # # %% get means
    # refc_problec_results.loc['mean'] = refc_problec_results.mean()
    # refc_problenc_results.loc['mean'] = refc_problenc_results.mean()
    # refnc_problec_results.loc['mean'] = refnc_problec_results.mean()
    # refnc_problenc_results.loc['mean'] = refnc_problenc_results.mean()
    #
    # # %% plot average
    # probe_numerosity = np.array([46, 44, 42, 40, 38, 36, 34])
    # yValues_rc_pc = refc_problec_results.values[12]
    # yValues_rc_pnc = refc_problenc_results.values[12]
    # yValues_rnc_pc = refnc_problec_results.values[12]
    # yValues_rnc_pnc = refnc_problenc_results.values[12]
    #
    # fig, ax = plt.subplots()
    # ax.plot(probe_numerosity, yValues_rc_pc, alpha = .5, color = 'green', marker = 'o', label = "ref c; probe c")
    # ax.plot(probe_numerosity, yValues_rc_pnc, alpha = .5, color = 'blue', marker = 'o', label = "ref c; probe nc")
    # ax.plot(probe_numerosity, yValues_rnc_pc, alpha = .5, color = 'red', marker = 'o', label = "ref nc; probe c")
    # ax.plot(probe_numerosity, yValues_rnc_pnc, alpha = .5, color = 'pink', marker = 'o', label = "ref nc; probe nc")
    # ax.legend()
    #
    # ax.set_xlabel("probe numerosity")
    # ax.set_ylim([0, 1])
    # ax.set_ylabel("proportion ref more")
    #
    # plt.show()
    #
    # # %%plot individual
    # y_rc_pc = refc_problec_results.values
    # fig2, ax2 = plt.subplots()
    # for y_val in y_rc_pc:
    #     ax2.scatter(probe_numerosity, y_val, alpha = .3, color = "grey")
    # ax2.plot(probe_numerosity, yValues_rc_pc, alpha = .8, color = 'green', marker = 'o', label = "ref c; probe c")
    # ax2.legend()
    # ax2.set_xlabel("probe numerosity")
    # ax2.set_ylabel("proportion ref more")
    # ax2.set_ylim([0, 1])
    # plt.show()
    #
    # y_rc_pnc = refc_problenc_results.values
    # fig3, ax3 = plt.subplots()
    # for y_val in y_rc_pnc:
    #     ax3.scatter(probe_numerosity, y_val, alpha = .3, color = "grey")
    # ax3.plot(probe_numerosity, yValues_rc_pnc, alpha = .8, color = 'blue', marker = 'o', label = "ref c; probe nc")
    # ax3.legend()
    # ax3.set_xlabel("probe numerosity")
    # ax3.set_ylabel("proportion ref more")
    # ax3.set_ylim([0, 1])
    # plt.show()
    #
    # y_rnc_pc = refnc_problec_results.values
    # fig4, ax4 = plt.subplots()
    # for y_val in y_rnc_pc:
    #     ax4.scatter(probe_numerosity, y_val, alpha = .3, color = "grey")
    # ax4.plot(probe_numerosity, yValues_rnc_pc, alpha = .8, color = 'red', marker = 'o', label = "ref nc; probe c")
    # ax4.legend()
    # ax4.set_xlabel("probe numerosity")
    # ax4.set_ylabel("proportion ref more")
    # ax4.set_ylim([0, 1])
    # plt.show()
    #
    # y_rnc_pnc = refnc_problenc_results.values
    # fig5, ax5 = plt.subplots()
    # for y_val in y_rnc_pnc:
    #     ax5.scatter(probe_numerosity, y_val, alpha = .3, color = "grey")
    # ax5.plot(probe_numerosity, yValues_rnc_pnc, alpha = .8, color = 'pink', marker = 'o', label = "ref nc; probe nc")
    # ax5.legend()
    # ax5.set_xlabel("probe numerosity")
    # ax5.set_ylabel("proportion ref more")
    # plt.show()
    # %% fit CDF
    # x values
    # xValues = np.array([46, 44, 42, 40, 38, 36, 34])
    # subjects = 12
    # condition = 1
    #
    # mu = np.zeros((subjects, condition))
    # sigma = np.zeros((subjects, condition))
    # yValues = refc_problec_results.values
    # yyy = yValues[1]
    #
    # # cumulative gaussian fit
    # t = np.linspace(46, 34, 1000)
    # testrefratios = np.array([0.2, 0.4, 0.6, 0.8, 0.9, 1., 1.1, 1.2, 1.4, 1.6, 1.8])
    # Pn_final = np.array([0., 0., 0.03, 0.35, 0.47, 0.57, 0.68, 0.73, 0.76, 0.85, 0.91])
    # Pd_final = np.array([0., 0.03, 0.36, 0.85, 0.97, 0.98, 0.98, 0.99, 1., 1., 1.])
    #
    # # mu1, sigma1 = curve_fit(norm.cdf, testrefratios, Pn_final, p0 = [0, 1])[0]
    # # plt.plot(t, norm.cdf(t, mu1, sigma1), alpha = .5)
    # # plt.show()
    #
    # # for sub in range(0, subjects):
    # mu, sigma = curve_fit(norm.cdf, xValues, yyy, p0 = [0, 1])[0]
    # plt.plot(t, norm.cdf(t, mu, sigma), alpha = .5)
    # plt.show()

    # %% debug and output
    if is_debug:
        col_names = list(all_df.columns)
        sub_df_cols2check = ["D1numerosity",
                             "D2numerosity",
                             "D1Crowding",
                             "D2Crowding",
                             "ref_first",
                             "key_resp.keys",
                             "is_resp_ref_more",
                             "probeN",
                             "refN",
                             "probeCrowding",
                             "refCrowding",
                             "ref_probe_condi"]
        df2check = all_df[sub_df_cols2check]

    if write_to_excel:
        all_df.to_excel("preprocess_exp3a_pilot.xlsx")
        pt.to_excel("pivot_table_exp3a_pilot.xlsx")