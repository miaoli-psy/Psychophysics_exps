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
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.exp1_alignment_analysis import add_color_code_by_crowdingcons, add_color_code_5levels, \
    get_analysis_dataframe, get_data_to_analysis, normalize_deviation, normalize_zerotoone, rename_norm_col, add_legend
from src.commons.process_dataframe import keep_valid_columns, insert_new_col, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF2, KEPT_COL_NAMES3


def calculate_residuals(input_df):
    lin_fit_results_Y = sm.ols(formula = "deviation_score_norm ~ N_disk", data = input_df).fit()
    input_df["rY"] = lin_fit_results_Y.resid

    lin_fit_results_X = sm.ols(formula = "count_number_norm ~ N_disk", data = input_df).fit()
    input_df["rX"] = lin_fit_results_X.resid


def get_partical_pearson_r(df):
    return df.at["pearson", "r"]


def draw_text(fig):
    fig.text(0.16, 0.89, "(a) numerosity range: 21-25", fontsize = 14)
    fig.text(0.44, 0.89, "(b) numerosity range: 31-35", fontsize = 14)
    fig.text(0.71, 0.89, "(c) numerosity range: 41-45", fontsize = 14)
    fig.text(0.16, 0.47, "(d) numerosity range: 49-53", fontsize = 14)
    fig.text(0.44, 0.47, "(e) numerosity range: 54-58", fontsize = 14)
    fig.text(0.71, 0.47, "(f) all numerosities", fontsize = 14)

if __name__ == '__main__':
    is_debug = True
    save_fig = False
    winsize_list = [0.3, 0.4, 0.5, 0.6, 0.7]
    # TODO set parameters
    crowdingcons = 2  # 0, 1, 2 for no-crowding, crowding and all
    # read stimuli info and data
    PATH_DATA = "../data/exp1_rerun_data/"
    STIM_PATH = "../displays/"
    FILENAME_DATA = "cleanedTotalData_fullinfo_v3.xlsx"
    FILENAME_STIM = "update_stim_info_full.xlsx"
    data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)
    stim_to_merge = pd.read_excel(STIM_PATH + FILENAME_STIM)
    stimuli_to_merge = keep_valid_columns(stim_to_merge, KEPT_COL_NAMES3)
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
    df_list_beforegb = [get_sub_df_according2col_value(my_data, "winsize", winsize) for winsize in winsize_list]
    df_list = [get_data_to_analysis(df, "deviation_score", "count_number", "N_disk", "list_index", "colorcode",
                                    "colorcode5levels") for df in df_list_beforegb]
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
    [calculate_residuals(df) for df in df_list]
    # %% combined r
    my_data_combined = pd.concat(df_list, axis = 0, sort = True)
    partial_corr_all = pg.partial_corr(my_data_combined,
                                       x = x,
                                       y = y,
                                       covar = "N_disk",
                                       method = method)
    # %% plot partial corr deviation score and count number
    # ini plot
    sns.set(style = "white", color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    # some parameters
    x = "rX"
    y = "rY"
    jitter = 0.001
    ci = None
    color = "gray"
    x_label = "Residuals of liner regression predicting normalized "
    x_label2 = "number of discs falls into others' crowding zones from numerosity"
    y_label = "Residuals of liner regression predicting"
    y_label2 = "normalized deviation score from numerosity"
    # plot starts here
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
    ax_dic = {0: ax1, 1: ax2, 2: ax3, 3: ax4, 4: ax5, 5: ax6}
    # plot for separate ws
    for index, df in enumerate(df_list):
        sns.regplot(x = x, y = y, data = df, x_jitter = jitter, ax = ax_dic[index],
                    scatter_kws = {'facecolors': df['colorcode5levels']}, color = color, ci = ci)
    # plot combined all ws
    sns.regplot(x = x, y = y, data = my_data_combined, x_jitter = jitter, ax = ax6,
                scatter_kws = {'facecolors': my_data_combined['colorcode']}, color = color, ci = ci)

    for curr_ax in ax_dic.values():
        # set x, y lim
        curr_ax.set_xlim(-0.5, 1)
        # curr_ax.set_ylim(-1.1, 1.1)
        # set x, y label
        if curr_ax == ax5:
            curr_ax.set(xlabel = x_label + x_label2, ylabel = "")
            curr_ax.xaxis.label.set_size(20)
        else:
            curr_ax.set(xlabel = "", ylabel = "")
        # add legend
        if curr_ax == ax1:
            colors_c = ["#ffd6cc", "#ffad99", "#ff8566", "#ff5c33", "#ff3300"]
            colors_nc = ["#ccccff", "#9999ff", "#6666ff", "#3333ff", "#0000ff"]
            circle_legend = add_legend(colors_c, colors_nc)
            ax1.legend(handles = circle_legend, labelspacing = 0.01,
                       ncol = 2, columnspacing = 0.01, borderpad = None,
                       frameon = False, bbox_to_anchor = (0.6, 0., 0.5, 0.5))

    # some text
    # numerosity ranges
    draw_text(fig = fig)
    # y-label
    fig.text(0.06, 0.5, y_label, va = 'center', rotation = 'vertical', fontsize = 20)
    fig.text(0.08, 0.5, y_label2, va = 'center', rotation = 'vertical', fontsize = 20)

    # peasorn r
    fig.text(0.28, 0.85, "r = %s" % (round(partial_corr_res_list[0].at['pearson', 'r'], 2)), va = "center",
             fontsize = 15)
    fig.text(0.56, 0.85, "r = %s" % (round(partial_corr_res_list[1].at['pearson', 'r'], 2)), va = "center",
             fontsize = 15)
    fig.text(0.83, 0.85, "r = %s" % (round(partial_corr_res_list[2].at['pearson', 'r'], 2)), va = "center",
             fontsize = 15)
    fig.text(0.28, 0.43, "r = %s" % (round(partial_corr_res_list[3].at['pearson', 'r'], 2)), va = "center",
             fontsize = 15)
    fig.text(0.56, 0.43, "r = %s" % (round(partial_corr_res_list[4].at['pearson', 'r'], 2)), va = "center",
             fontsize = 15)
    fig.text(0.83, 0.43, "r = %s" % (round(partial_corr_all.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    plt.show()
    if save_fig:
        fig.savefig("try.svg")
    # %% rs for increasing ellipse sizes
    count_number_dict = {1:  "count_number1",
                         2:  "count_number2",
                         3:  "count_number3",
                         4:  "count_number4",
                         5:  "count_number5",
                         6:  "count_number6",
                         7:  "count_number7",
                         8:  "count_number8",
                         9:  "count_number9",
                         10: "count_number10"}
    df_list_separate_count_n = list()  # length:10 (e size 1-10); each value is a list of length 5 (5 winsize)
    for count_numbern in count_number_dict.values():
        sub_df_list = [get_data_to_analysis(df, "deviation_score", count_numbern, "N_disk", "list_index", "colorcode",
                                            "colorcode5levels") for df in df_list_beforegb]
        df_list_separate_count_n.append(sub_df_list)

    partial_corr_res_spe_list = list()
    for index, esize_list in enumerate(df_list_separate_count_n):
        partial_corr_result = [
            pg.partial_corr(indi_df, x = count_number_dict[index + 1], y = "deviation_score", covar = covar,
                            method = method) for indi_df in esize_list]
        partial_corr_res_spe_list.append(partial_corr_result)
    # arrange data
    rs_all = list()
    for df_list in partial_corr_res_spe_list:
        rs = [get_partical_pearson_r(sub_df) for sub_df in df_list]
        rs_all.append(rs)
    df_rs = pd.DataFrame(rs_all, columns = ["w03", "w04", "w05", "w06", "w07"])
    df_rs["esize"] = np.array([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])

    # plot starts here
    figb, ((bx1, bx2, bx3), (bx4, bx5, bx6)) = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
    bx_dic = {0: bx1, 1: bx2, 2: bx3, 3: bx4, 4: bx5, 5: bx6}
    bx_dic = {"w03": bx1, "w04": bx2, "w05": bx3, "w06": bx4, "w07": bx5}
    for wsize, bx in bx_dic.items():
        sns.regplot(x = "esize", y = wsize, data = df_rs, ax = bx, order = 2, color = color, ci = 95)

    for curr_ax in bx_dic.values():
        # set x, y lim
        curr_ax.set_xlim(1, 2)
        # curr_ax.set_xscale('log')
        # x-label
        if curr_ax == bx5:
            curr_ax.set(xlabel = "ellipse size", ylabel = "")
            curr_ax.xaxis.label.set_size(20)
        else:
            curr_ax.set(xlabel = "", ylabel = "")
        # some text
    # numerosity ranges
    draw_text(fig = figb)
    figb.text(0.06, 0.5, "partial corr between deviation score and", va = 'center', rotation = 'vertical', fontsize = 20)
    figb.text(0.08, 0.5, "number of discs falls into ohters' crowding zones", va = 'center', rotation = 'vertical', fontsize = 20)

    plt.show()

    if is_debug:
        col_names = list(all_df.columns)