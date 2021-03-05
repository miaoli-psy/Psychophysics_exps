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
import exp1_radial_display2
from matplotlib.lines import Line2D
import pingouin as pg

from src.analysis.exp1_alignment_analysis import get_data_to_analysis, get_analysis_dataframe, \
    add_color_code_by_crowdingcons, \
    normalize_deviation, normalize_zerotoone, rename_norm_col, add_color_code_by_winsize, add_color_code_5levels, \
    calculate_residuals, add_legend
from src.commons.process_dataframe import change_col_value_type, keep_valid_columns, get_pivot_table, \
    get_sub_df_according2col_value, insert_new_col, insert_new_col_from_two_cols
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF, KEPT_COL_NAMES

is_debug = True
check_r = False
pivot_table = False
cal_pearsonr = True
save_fig = True
# TODO set parameters
separate_each_n = False  # True for 5 reg lines in each plot for 5 numerosities
crowdingcons = 2  # 0, 1, 2 for no-crowding, crowding and all data
indx_align_n = 6  # 0-11
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

# read stimuli info and data
PATH_DATA = "../data/exp1_rerun_data/"
FILENAME_DATA = "cleanedTotalData_fullinfo_v3.xlsx"
# stimuli dataframe read from exp1_raidal_display2.py
stimuli_to_merge_ori = exp1_radial_display2.stimuli_df
data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)

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
                  how = "left",
                  on = ["index_stimuliInfo", "N_disk", "crowdingcons", "winsize"])

# %% preprocess
my_data = keep_valid_columns(all_df, KEPT_COL_NAMES)
# add color coded for crowding and no-crowding displays
insert_new_col(my_data, "crowdingcons", 'colorcode', add_color_code_by_crowdingcons)
# color coded
insert_new_col_from_two_cols(my_data, "N_disk", "crowdingcons", "colorcode5levels", add_color_code_5levels)

# %% correlation
# crowding = 0, 1, 2 for no-crowding, crowding and all data
my_data = get_analysis_dataframe(my_data, crowding = crowdingcons)
winsize = [0.3, 0.4, 0.5, 0.6, 0.7]
my_data_list = [get_sub_df_according2col_value(my_data, "winsize", ws) for ws in winsize]

# data to calcualte partial corr
my_data_list2analysis = [
    get_data_to_analysis(data, "deviation_score", alignment[indx_align_n], "N_disk", "list_index", "colorcode",
                         "colorcode5levels") for data in my_data_list]

# partial corr between deviation score and alignment scores
method = "pearson"
partial_corr_list = [pg.partial_corr(data, x = "deviation_score", y = alignment[indx_align_n], covar = "N_disk",
                                     method = method) for data in my_data_list2analysis]

# see correlations
if cal_pearsonr:
    pearson_r = [stats.pearsonr(data["deviation_score"], data[alignment[indx_align_n]]) for data in
                 my_data_list2analysis]
    pearson_r2 = [stats.pearsonr(data["N_disk"], data[alignment[indx_align_n]]) for data in my_data_list2analysis]
    pearson_r3 = [stats.pearsonr(data["N_disk"], data["deviation_score"]) for data in my_data_list2analysis]
# %% normalization
norm_deviation_list = [normalize_deviation(data) for data in my_data_list2analysis]
norm_align_v_list = [normalize_zerotoone(data, to_normalize_col = alignment[indx_align_n]) for data in
                     my_data_list2analysis]

# rename normed cols
old_name_dev = "deviation_score"
new_name_dev = "deviation_score_norm"
old_name_alig = alignment[indx_align_n]
new_name_alig = alignment[indx_align_n] + "_norm"

renamed_norm_deviation_list = [rename_norm_col(norm_deviation, old_name_dev, new_name_dev) for norm_deviation in
                               norm_deviation_list]
renamed_norm_align_v_list = [rename_norm_col(norm_align_v, old_name_alig, new_name_alig) for norm_align_v in
                             norm_align_v_list]

# contact orig dataframe with new normalized dataframe
my_df_list = list()
for i in range(0, 5):
    data_df = pd.concat([my_data_list2analysis[i], renamed_norm_deviation_list[i], renamed_norm_align_v_list[i]],
                        axis = 1)
    my_df_list.append(data_df)

# separate for each numerosity
N_disk = "N_disk"
num_list = [21, 22, 23, 24, 25,
            31, 32, 33, 34, 35,
            41, 42, 43, 44, 45,
            49, 50, 51, 52, 53,
            54, 55, 56, 57, 58]

w03_list = [get_sub_df_according2col_value(my_df_list[0], N_disk, num) for num in num_list[0: 5]]
w04_list = [get_sub_df_according2col_value(my_df_list[1], N_disk, num) for num in num_list[5: 10]]
w05_list = [get_sub_df_according2col_value(my_df_list[2], N_disk, num) for num in num_list[10: 15]]
w06_list = [get_sub_df_according2col_value(my_df_list[3], N_disk, num) for num in num_list[15: 20]]
w07_list = [get_sub_df_according2col_value(my_df_list[4], N_disk, num) for num in num_list[20: 26]]

# calculate residuals
[calculate_residuals(data) for data in my_df_list]

# %% combined r
# combine all normalized data
my_data_new = pd.concat(my_df_list, axis = 0, sort = True)
# add colorcode by winsize
insert_new_col(my_data_new, "N_disk", 'colorcode_ws', add_color_code_by_winsize)
# single correlation combining all numerosity ranges
r, p = stats.pearsonr(my_data_new["deviation_score_norm"], my_data_new[alignment[indx_align_n] + "_norm"])
r2, p2 = stats.pearsonr(my_data_new["N_disk"], my_data_new[alignment[indx_align_n] + "_norm"])

partial_corr_all = pg.partial_corr(my_data_new, x = "deviation_score", y = alignment[indx_align_n],
                                   covar = "N_disk",
                                   method = method)
partial_corr_list.append(partial_corr_all)
partial_corr = pd.concat(partial_corr_list, axis = 0)
# %%plots-separate winsize correlation between alignment value and deviation score
# ini plot
sns.set(style = "white", color_codes = True)
sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
# some parameters
# x = alignment[indx_align_n] + "_norm"
x = "rX"
# y = "deviation_score_norm"
y = "rY"
jitter = 0.001
ci = None
color = "gray"
color_reg_line = ["#d9d9d9", "#bfbfbf", "#a6a6a6", "#8c8c8c", "#737373"]
x_label = "Residuals of liner regression predicting normalized alignment value from numerosity"
y_label = "Residuals of liner regression predicting"
y_label2 = "normalized deviation score from numerosity"
colors_c = ["#ffd6cc", "#ffad99", "#ff8566", "#ff5c33", "#ff3300"]
colors_nc = ["#ccccff", "#9999ff", "#6666ff", "#3333ff", "#0000ff"]
labels03 = ['21', '22', '23', '23', '25']
# plot starts here
fig, axes = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
axes = axes.ravel()
if not separate_each_n:
    for i, ax in enumerate(axes):
        if i < 5:
            sns.regplot(x = x, y = y, data = my_df_list[i], x_jitter = jitter, ax = ax,
                        scatter_kws = {'facecolors': my_df_list[i]['colorcode5levels']}, color = color, ci = ci)
        else:
            sns.regplot(x = x, y = y, data = my_data_new, x_jitter = jitter, ax = ax,
                        scatter_kws = {'facecolors': my_data_new['colorcode']}, color = color, ci = ci)
        # sex xlim
        ax.set_xlim(-0.5, 1)

        # set x,y label
        if i == 4:
            ax.set(xlabel = x_label, ylabel = "")
            ax.xaxis.label.set_size(20)
        else:
            ax.set(xlabel = "", ylabel = "")

        # legend
        if i == 0:
            circle_legend = add_legend(colors_c, colors_nc)
            ax.legend(handles = circle_legend, labelspacing = 0.01, ncol = 2, columnspacing = 0.01, borderpad = None,
                      frameon = False, bbox_to_anchor = (0.6, 0., 0.5, 0.5))
    # some text
    fig.text(0.16, 0.89, "(a) numerosity range: 21-25", fontsize = 14)
    fig.text(0.44, 0.89, "(b) numerosity range: 31-35", fontsize = 14)
    fig.text(0.71, 0.89, "(c) numerosity range: 41-45", fontsize = 14)
    fig.text(0.16, 0.47, "(d) numerosity range: 49-53", fontsize = 14)
    fig.text(0.44, 0.47, "(e) numerosity range: 54-58", fontsize = 14)
    fig.text(0.71, 0.47, "(f) all numerosities", fontsize = 14)
    fig.text(0.06, 0.5, y_label, va = 'center', rotation = 'vertical', fontsize = 20)
    fig.text(0.08, 0.5, y_label2, va = 'center', rotation = 'vertical', fontsize = 20)

    plt.show()
# %%plots-separate winsize - correlation between alignment value and numerosity
# ini plot
sns.set(style = "white", color_codes = True)
sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
# some parameters
x = "N_disk"
y = alignment[indx_align_n] + "_norm"
jitter = 0.001
color = "gray"
# plot starts here
figa, axes = plt.subplots(2, 3, figsize = (13, 6), sharex = False, sharey = True)
axes = axes.ravel()
for i, ax in enumerate(axes):
    if i < 5:
        sns.regplot(x = x, y = y, data = my_df_list[i], x_jitter = jitter, ax = ax,
                    scatter_kws = {'facecolors': my_df_list[i]['colorcode']}, color = color)

    # set x, y limits
    ax.set_ylim(-0.1, 1.1)

    # set x,y label
    if i == 4:
        ax.set(xlabel = "numerosity", ylabel = "")
        ax.xaxis.label.set_size(20)
    else:
        ax.set(xlabel = "", ylabel = "")

fig.text(0.07, 0.5, "alignment value: %s" % (alignment[indx_align_n]), va = 'center', rotation = 'vertical',
         fontsize = 20)
plt.show()
# %% debug and write to excel
if is_debug:
    col_names_stimuli = list(stimuli_to_merge_ori.columns)
    col_names_data = list(data_to_merge)
    col_names_my_data = list(my_data)
if save_fig:
    fig.savefig("try.svg")