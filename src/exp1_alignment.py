# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 20:02
IDE: PyCharm
Introduction:
"""
import pandas as pd
from scipy.stats import stats
import matplotlib.pyplot as plt
import seaborn as sns

from src.analysis.exp1_alignment_analysis import get_data_to_analysis
from src.commons.process_dataframe import change_col_value_type, keep_valid_columns, get_pivot_table, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF, KEPT_COL_NAMES

if __name__ == '__main__':
    is_debug = True
    write_to_excel = True

    # read stimuli info and data
    PATH_STIMULI = "../displays/"
    PATH_DATA = "../data/exp1_rerun_data/"
    STIMULI_FILENAME = "exp1_stim_info.xlsx"
    DATA_FILENAME = "cleanedTotalData_fullinfo_v2.xlsx"

    stimuli_to_merge_ori = pd.read_excel(PATH_STIMULI + STIMULI_FILENAME)
    data_to_merge = pd.read_excel(PATH_DATA + DATA_FILENAME)

    # unify col value type
    change_col_value_type(stimuli_to_merge_ori, "crowdingcons", int)
    change_col_value_type(stimuli_to_merge_ori, "winsize", float)
    change_col_value_type(stimuli_to_merge_ori, "index_stimuliInfo", str)
    change_col_value_type(stimuli_to_merge_ori, "N_disk", int)

    change_col_value_type(data_to_merge, "crowdingcons", int)
    change_col_value_type(data_to_merge, "winsize", float)
    change_col_value_type(data_to_merge, "index_stimuliInfo", str)
    change_col_value_type(data_to_merge, "N_disk", int)

    # remove duplicated cols
    stimuli_to_merge = keep_valid_columns(stimuli_to_merge_ori, KEPT_COL_NAMES_STIMU_DF)

    # merge data with stimuli info
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = 'left',
                      on = ['index_stimuliInfo', 'N_disk', 'crowdingcons', 'winsize'])

    # %% preprocess
    my_data = keep_valid_columns(all_df, KEPT_COL_NAMES)

    # %% output
    alignment = ["alig_v_angle6_step6_cont",
                 "alig_v_angle12_step12_cont",
                 "alig_v_angle6_step1_count",
                 "alig_v_angle12_step1_count",
                 "alig_v_line_step1_cont",
                 "alig_v_angle6_step1_squared_w",
                 "alig_v_angle12_step1_squared_w",
                 "alig_v_angle6_step1",
                 "alig_v_angle12_step1",
                 "alig_v_angle6_step6",
                 "alig_v_angle12_step12"]

    # index of alignment list
    n = 8
    # pivot table
    pt = get_pivot_table(my_data,
                         index = ["participant_N"],
                         columns = ["winsize", "crowdingcons", alignment[n]],
                         values = ["deviation_score"])
    # %% correlation
    my_data_c = get_sub_df_according2col_value(my_data, "crowdingcons", 1)
    # data for each winsize
    w03_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.3)
    w04_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.4)
    w05_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.5)
    w06_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.6)
    w07_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.7)

    # w03_c = w03_c["deviation_score"].groupby(
    #         [w03_c["alig_v_angle12_step1"], w03_c["N_disk"], w03_c["list_index"]]).mean()
    # # convert index to column
    # w03_c = w03_c.reset_index(level = ["alig_v_angle12_step1", "list_index", "N_disk"])

    # which alignment value 0-4
    n = 10
    w03_c = get_data_to_analysis(w03_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w04_c = get_data_to_analysis(w04_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w05_c = get_data_to_analysis(w05_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w06_c = get_data_to_analysis(w06_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w07_c = get_data_to_analysis(w07_c, "deviation_score", alignment[n], "N_disk", "list_index")

    r03, p03 = stats.pearsonr(w03_c["deviation_score"], w03_c[alignment[n]])
    r04, p04 = stats.pearsonr(w04_c["deviation_score"], w04_c[alignment[n]])
    r05, p05 = stats.pearsonr(w05_c["deviation_score"], w05_c[alignment[n]])
    r06, p06 = stats.pearsonr(w06_c["deviation_score"], w06_c[alignment[n]])
    r07, p07 = stats.pearsonr(w07_c["deviation_score"], w07_c[alignment[n]])

    print(f"correlation coefficient is {round(r03, 2)}, and p-value is {round(p03, 4)} for numerosity range 21-25")
    print(f"correlation coefficient is {round(r04, 2)}, and p-value is {round(p04, 4)} for numerosity range 31-35")
    print(f"correlation coefficient is {round(r05, 2)}, and p-value is {round(p05, 4)} for numerosity range 41-45")
    print(f"correlation coefficient is {round(r06, 2)}, and p-value is {round(p06, 4)} for numerosity range 49-53")
    print(f"correlation coefficient is {round(r07, 2)}, and p-value is {round(p07, 4)} for numerosity range 54-58")
    # %%plots
    sns.set(style = 'white', color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    fig, axes = plt.subplots(2, 3, figsize = (13, 6), sharex = False, sharey = True)

    sns.regplot(x = alignment[n], y = "deviation_score", data = w03_c, x_jitter = 0.5, ax = axes[0, 0])
    sns.regplot(x = alignment[n], y = "deviation_score", data = w04_c, x_jitter = 0.5, ax = axes[0, 1])
    sns.regplot(x = alignment[n], y = "deviation_score", data = w05_c, x_jitter = 0.5, ax = axes[0, 2])
    sns.regplot(x = alignment[n], y = "deviation_score", data = w06_c, x_jitter = 0.5, ax = axes[1, 0])
    sns.regplot(x = alignment[n], y = "deviation_score", data = w07_c, x_jitter = 0.5, ax = axes[1, 1])

    # set x, y limits
    axes[0, 0].set_ylim(-2, 6)
    axes[0, 1].set_ylim(-2, 6)
    axes[0, 2].set_ylim(-2, 6)
    axes[1, 0].set_ylim(-2, 6)
    axes[1, 1].set_ylim(-2, 6)

    # set x,y label
    axes[0, 0].set(xlabel = '', ylabel = '')
    axes[0, 1].set(xlabel = '', ylabel = '')
    axes[0, 2].set(xlabel = '', ylabel = '')
    axes[1, 0].set(xlabel = '', ylabel = '')
    axes[1, 1].set(xlabel = "alignment value", ylabel = '')

    axes[1, 1].xaxis.label.set_size(20)

    # peasorn r
    fig.text(0.28, 0.85, 'r = %s' % (round(r03, 2)), va = 'center', fontsize = 15)
    fig.text(0.56, 0.85, 'r = %s' % (round(r04, 2)), va = 'center', fontsize = 15)
    fig.text(0.83, 0.85, 'r = %s' % (round(r05, 2)), va = 'center', fontsize = 15)
    fig.text(0.28, 0.43, 'r = %s' % (round(r06, 2)), va = 'center', fontsize = 15)
    fig.text(0.56, 0.43, 'r = %s' % (round(r07, 2)), va = 'center', fontsize = 15)

    fig.text(0.15, 0.89, '(a) numerosity range: 21-25', fontsize = 14)
    fig.text(0.43, 0.89, '(b) numerosity range: 31-35', fontsize = 14)
    fig.text(0.7, 0.89, '(c) numerosity range: 41-45', fontsize = 14)
    fig.text(0.15, 0.47, '(d) numerosity range: 49-53', fontsize = 14)
    fig.text(0.43, 0.47, '(e) numerosity range: 54-58', fontsize = 14)

    # remoing the borders and ticks of the last subplot
    axes[1, 2].spines['top'].set_visible(False)
    axes[1, 2].spines['left'].set_visible(False)
    axes[1, 2].spines['right'].set_visible(False)
    axes[1, 2].spines['bottom'].set_visible(False)
    # removing the tick marks
    axes[1, 2].tick_params(bottom = False, left = False)

    # removing the x label
    axes[1, 2].xaxis.set_visible(False)
    plt.show()
    # %% debug and write to excel
    if is_debug:
        col_names_stimuli = list(stimuli_to_merge_ori.columns)
        col_names_data = list(data_to_merge)
        col_names_my_data = list(my_data)
    if write_to_excel:
        pt.to_excel("exp1_alig_%s.xlsx" % n)
