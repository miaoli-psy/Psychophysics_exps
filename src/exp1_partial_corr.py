# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-24 23:19
IDE: PyCharm
Introduction: cal partial corr for all angle size (1-12deg)
"""
import exp1_alignment
import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns

from src.analysis.exp1_alignment_analysis import normalize_deviation, normalize_alignment_v, rename_norm_col, \
    get_data_to_analysis
from src.commons.process_dataframe import get_sub_df_according2col_value, process_col

# all possible anlge sizes
alignment = ["align_v_size12",
             "align_v_size11",
             "align_v_size10",
             "align_v_size9",
             "align_v_size8",
             "align_v_size7",
             "align_v_size6",
             "align_v_size5",
             "align_v_size4",
             "align_v_size3",
             "align_v_size2",
             "align_v_size1"]

# get data to cal partial corr
my_data = exp1_alignment.my_data
winsize03 = get_sub_df_according2col_value(my_data, "winsize", 0.3)
winsize04 = get_sub_df_according2col_value(my_data, "winsize", 0.4)
winsize05 = get_sub_df_according2col_value(my_data, "winsize", 0.5)
winsize06 = get_sub_df_according2col_value(my_data, "winsize", 0.6)
winsize07 = get_sub_df_according2col_value(my_data, "winsize", 0.7)


def get_partial_corr_df(indx_align_n = 0, w03 = winsize03, w04 = winsize04, w05 = winsize05, w06 = winsize06,
                        w07 = winsize07):
    """
    get one partial corr dataframe for given angle size, indicated by indx_align_n
    """
    w03 = get_data_to_analysis(w03, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                               "colorcode5levels")
    w04 = get_data_to_analysis(w04, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                               "colorcode5levels")
    w05 = get_data_to_analysis(w05, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                               "colorcode5levels")
    w06 = get_data_to_analysis(w06, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                               "colorcode5levels")
    w07 = get_data_to_analysis(w07, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                               "colorcode5levels")

    method = "pearson"
    try:
        partial_corr_03 = pg.partial_corr(w03, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                          method = method)
    except Exception:
        partial_corr_03 = pd.DataFrame()

    try:
        partial_corr_04 = pg.partial_corr(w04, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                          method = method)
    except Exception:
        partial_corr_04 = pd.DataFrame()

    try:
        partial_corr_05 = pg.partial_corr(w05, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                          method = method)
    except Exception:
        partial_corr_05 = pd.DataFrame()
    partial_corr_06 = pg.partial_corr(w06, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                      method = method)
    partial_corr_07 = pg.partial_corr(w07, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                      method = method)

    # normalization
    w03_norm_deviation = normalize_deviation(w03)
    w04_norm_deviation = normalize_deviation(w04)
    w05_norm_deviation = normalize_deviation(w05)
    w06_norm_deviation = normalize_deviation(w06)
    w07_norm_deviation = normalize_deviation(w07)

    w03_norm_align_v = normalize_alignment_v(w03, alignment_col = alignment[indx_align_n])
    w04_norm_align_v = normalize_alignment_v(w04, alignment_col = alignment[indx_align_n])
    w05_norm_align_v = normalize_alignment_v(w05, alignment_col = alignment[indx_align_n])
    w06_norm_align_v = normalize_alignment_v(w06, alignment_col = alignment[indx_align_n])
    w07_norm_align_v = normalize_alignment_v(w07, alignment_col = alignment[indx_align_n])
    # rename normed cols
    old_name_dev = "deviation_score"
    new_name_dev = "deviation_score_norm"
    old_name_alig = alignment[indx_align_n]
    new_name_alig = alignment[indx_align_n] + "_norm"
    w03_norm_deviation = rename_norm_col(w03_norm_deviation, old_name_dev, new_name_dev)
    w04_norm_deviation = rename_norm_col(w04_norm_deviation, old_name_dev, new_name_dev)
    w05_norm_deviation = rename_norm_col(w05_norm_deviation, old_name_dev, new_name_dev)
    w06_norm_deviation = rename_norm_col(w06_norm_deviation, old_name_dev, new_name_dev)
    w07_norm_deviation = rename_norm_col(w07_norm_deviation, old_name_dev, new_name_dev)
    w03_norm_align_v = rename_norm_col(w03_norm_align_v, old_name_alig, new_name_alig)
    w04_norm_align_v = rename_norm_col(w04_norm_align_v, old_name_alig, new_name_alig)
    w05_norm_align_v = rename_norm_col(w05_norm_align_v, old_name_alig, new_name_alig)
    w06_norm_align_v = rename_norm_col(w06_norm_align_v, old_name_alig, new_name_alig)
    w07_norm_align_v = rename_norm_col(w07_norm_align_v, old_name_alig, new_name_alig)
    # contact orig dataframe with new normalized dataframe
    w03 = pd.concat([w03, w03_norm_deviation, w03_norm_align_v], axis = 1)
    w04 = pd.concat([w04, w04_norm_deviation, w04_norm_align_v], axis = 1)
    w05 = pd.concat([w05, w05_norm_deviation, w05_norm_align_v], axis = 1)
    w06 = pd.concat([w06, w06_norm_deviation, w06_norm_align_v], axis = 1)
    w07 = pd.concat([w07, w07_norm_deviation, w07_norm_align_v], axis = 1)
    # new data to cal partial corr
    my_data_new = pd.concat([w03, w04, w05, w06, w07], axis = 0, sort = True)

    partial_corr_all = pg.partial_corr(my_data_new, x = "deviation_score", y = alignment[indx_align_n],
                                       covar = "N_disk",
                                       method = method)

    partial_corr = pd.concat(
            [partial_corr_03, partial_corr_04, partial_corr_05, partial_corr_06, partial_corr_07, partial_corr_all],
            axis = 0)
    return partial_corr

def convert_indx2_angle_size(index:str) -> str:
    if index == 0:
        return 12
    elif index == 1:
        return 11
    elif index == 2:
        return 10
    elif index == 3:
        return 9
    elif index == 4:
        return 8
    elif index == 5:
        return 7
    elif index == 6:
        return 6
    elif index == 7:
        return 5
    elif index == 8:
        return 4
    elif index == 9:
        return 3
    elif index == 10:
        return 2
    elif index == 11:
        return 1
    else:
        raise Exception(f"index == {index} is not recognized, allow 0-11")


if __name__ == '__main__':
    has_plot = True

    partial_corr_df_list = list()
    winsize = [0.3, 0.4, 0.5, 0.6, 0.7, 1]
    winsize_short = [0.6, 0.7, 1]
    for i in range(0, 12):
        partial_corr_df = get_partial_corr_df(indx_align_n = i)
        if not i == 11:
            align_v = [i]*6
            partial_corr_df['winsize'] = pd.Series(winsize).values
            partial_corr_df['angle_size'] = pd.Series(align_v).values
        else:
            align_v = [i]*3
            partial_corr_df['winsize'] = pd.Series(winsize_short).values
            partial_corr_df['angle_size'] = pd.Series(align_v).values
        partial_corr_df_list.append(partial_corr_df)

    partial_corr = pd.concat(partial_corr_df_list, axis = 0, sort = True)
    process_col(partial_corr, "angle_size", convert_indx2_angle_size)


    if has_plot:
        x = "angle_size"
        y = "r"
        y2 = "p-val"
        color = "gray"

        partial_corr_03 = get_sub_df_according2col_value(partial_corr, "winsize", 0.3 )
        partial_corr_04 = get_sub_df_according2col_value(partial_corr, "winsize", 0.4 )
        partial_corr_05 = get_sub_df_according2col_value(partial_corr, "winsize", 0.5 )
        partial_corr_06 = get_sub_df_according2col_value(partial_corr, "winsize", 0.6 )
        partial_corr_07 = get_sub_df_according2col_value(partial_corr, "winsize", 0.7 )
        partial_corr_all= get_sub_df_according2col_value(partial_corr, "winsize", 1)
        fig, axes = plt.subplots(2, 3, figsize = (13, 6), sharex = True, sharey = True)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_03, ax = axes[0, 0], color = color)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_04, ax = axes[0, 1], color = color)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_05, ax = axes[0, 2], color = color)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_06, ax = axes[1, 0], color = color)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_07, ax = axes[1, 1], color = color)
        sns.regplot(x = x, y = y, order = 2, data = partial_corr_all, ax = axes[1, 2], color = color)
        # set x,y label
        axes[0, 0].set(xlabel = "", ylabel = "")
        axes[0, 1].set(xlabel = "", ylabel = "")
        axes[0, 2].set(xlabel = "", ylabel = "")
        axes[1, 0].set(xlabel = "", ylabel = "")
        axes[1, 1].set(xlabel = "Angle Size", ylabel = "")
        axes[1, 1].xaxis.label.set_size(15)
        axes[1, 2].set(xlabel = "", ylabel = "")
        # set x tick
        axes[0, 0].get_xaxis().set_ticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

        axes[0, 0].set_xlim(0, 13)
        axes[0, 1].set_xlim(0, 13)
        axes[0, 2].set_xlim(0, 13)
        axes[1, 0].set_xlim(0, 13)
        axes[1, 1].set_xlim(0, 13)
        axes[1, 2].set_xlim(0, 13)
        # some text
        fig.text(0.15, 0.89, "(a) numerosity range: 21-25", fontsize = 15)
        fig.text(0.43, 0.89, "(b) numerosity range: 31-35", fontsize = 15)
        fig.text(0.70, 0.89, "(c) numerosity range: 41-45", fontsize = 15)
        fig.text(0.15, 0.47, "(d) numerosity range: 49-53", fontsize = 15)
        fig.text(0.43, 0.47, "(e) numerosity range: 54-58", fontsize = 15)
        fig.text(0.70, 0.47, "(e) all numerosities", fontsize = 15)

        fig.text(0.07, 0.5, 'Partial corr', va = 'center', rotation = 'vertical', fontsize = 15)
        plt.show()