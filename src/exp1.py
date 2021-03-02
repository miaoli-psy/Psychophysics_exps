# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-21 10:49
IDE: PyCharm
Introduction: Results exp1: deviation scores as a function of numerosity
"""
import exp1_radial_display2
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from src.analysis.exp1_alignment_analysis import add_color_code_5levels, get_analysis_dataframe
from src.analysis.exp1_analysis import get_data_to_analysis
from src.commons.process_dataframe import keep_valid_columns, get_col_names, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF2, KEPT_COL_NAMES2

if __name__ == '__main__':
    is_debug = True
    # TODO set parameters
    # read stimuli and data
    PATH_DATA = "../data/exp1_rerun_data/"
    FILENAME_DATA = "cleanedTotalData_fullinfo_v3.xlsx"
    stimuli_to_merge = exp1_radial_display2.stimuli_df
    data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)

    # remove duplicated cols
    stimuli_to_merge = keep_valid_columns(stimuli_to_merge, KEPT_COL_NAMES_STIMU_DF2)
    # merge stimuli file with data
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = "left",
                      on = ["index_stimuliInfo", "N_disk", "crowdingcons", "winsize"])
    # %% preprocess
    my_data = keep_valid_columns(all_df, KEPT_COL_NAMES2)
    # color coded
    insert_new_col_from_two_cols(my_data, "N_disk", "crowdingcons", "colorcode5levels", add_color_code_5levels)
    # %% for each numerosity range
    winsizes = [0.3, 0.4, 0.5, 0.6, 0.7]
    # 5 df in a list
    data_sep_ws = [get_sub_df_according2col_value(my_data, "winsize", winsize) for winsize in winsizes]
    # transform each df: groupby
    data_sep_ws_to_plot = [get_data_to_analysis(sub_df, "deviation_score", "N_disk", "participant_N", "crowdingcons", "colorcode5levels") for sub_df in data_sep_ws]
    # %%
    # ini plot
    sns.set(style = "white", color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    # some parameters
    x = "N_disk"
    y = "deviation_score"
    hue = "crowdingcons"
    errwidth = 1
    capsize = 0.01
    alpha = 0.5
    palette = ["royalblue", "orangered"]
    ci = 68
    # plot starts here
    fig, axes = plt.subplots(2, 3, figsize = (13, 6), sharex = False, sharey = True)
    sns.barplot(x = x, y = y, data = data_sep_ws_to_plot[0], ax = axes[0, 0], hue = hue, capsize = capsize, errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)
    sns.barplot(x = x, y = y, data = data_sep_ws_to_plot[1], ax = axes[0, 1], hue = hue, capsize = capsize, errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)
    sns.barplot(x = x, y = y, data = data_sep_ws_to_plot[2], ax = axes[0, 2], hue = hue, capsize = capsize, errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)
    sns.barplot(x = x, y = y, data = data_sep_ws_to_plot[3], ax = axes[1, 0], hue = hue, capsize = capsize, errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)
    sns.barplot(x = x, y = y, data = data_sep_ws_to_plot[4], ax = axes[1, 1], hue = hue, capsize = capsize, errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)

    # remove defalt legend
    axes[0, 0].get_legend().set_visible(False)
    axes[0, 1].get_legend().set_visible(False)
    axes[0, 2].get_legend().set_visible(False)
    axes[1, 0].get_legend().set_visible(False)
    axes[1, 1].get_legend().set_visible(False)
    # customize legend
    handles, labels = axes[0, 1].get_legend_handles_labels()
    labels = ["no-crowding", "crowding"]
    axes[0, 1].legend(handles, labels, loc = "best", fontsize = 12)

    # set x,y label
    axes[0, 0].set(xlabel = "", ylabel = "")
    axes[0, 1].set(xlabel = "", ylabel = "")
    axes[0, 2].set(xlabel = "", ylabel = "")
    axes[1, 0].set(xlabel = "", ylabel = "")
    axes[1, 1].set(xlabel = "Numerosity", ylabel = "")
    axes[1, 1].xaxis.label.set_size(20)

    fig.text(0.08, 0.5, 'Deviation Score', va = 'center', rotation = 'vertical', fontsize = 20)

    # remoing the borders and ticks of the last subplot
    axes[1, 2].spines["top"].set_visible(False)
    axes[1, 2].spines["left"].set_visible(False)
    axes[1, 2].spines["right"].set_visible(False)
    axes[1, 2].spines["bottom"].set_visible(False)
    # removing the tick marks
    axes[1, 2].tick_params(bottom = False, left = False)

    # removing the x label
    axes[1, 2].xaxis.set_visible(False)

    plt.show()

    if is_debug:
        col_names = get_col_names(stimuli_to_merge)