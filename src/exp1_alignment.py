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
    normalize_deviation, normalize_alignment_v, rename_norm_col, add_color_code_by_winsize, add_color_code_5levels, \
    calculate_residuals, add_legend
from src.commons.process_dataframe import change_col_value_type, keep_valid_columns, get_pivot_table, \
    get_sub_df_according2col_value, insert_new_col, insert_new_col_from_two_cols
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF, KEPT_COL_NAMES

is_debug = True
check_r = False
pivot_table = False
cal_pearsonr = True
save_fig = True
see_winsize_alignv = False
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
FILENAME_DATA = "cleanedTotalData_fullinfo_v2.xlsx"
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

# data for each winsize
w03 = get_sub_df_according2col_value(my_data, "winsize", 0.3)
w04 = get_sub_df_according2col_value(my_data, "winsize", 0.4)
w05 = get_sub_df_according2col_value(my_data, "winsize", 0.5)
w06 = get_sub_df_according2col_value(my_data, "winsize", 0.6)
w07 = get_sub_df_according2col_value(my_data, "winsize", 0.7)

# w03_c = w03_c["deviation_score"].groupby(
#         [w03_c["alig_v_angle12_step1"], w03_c["N_disk"], w03_c["list_index"]]).mean()
# # convert index to column
# w03_c = w03_c.reset_index(level = ["alig_v_angle12_step1", "list_index", "N_disk"])

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

if cal_pearsonr:
    r03, p03 = stats.pearsonr(w03["deviation_score"], w03[alignment[indx_align_n]])
    r04, p04 = stats.pearsonr(w04["deviation_score"], w04[alignment[indx_align_n]])
    r05, p05 = stats.pearsonr(w05["deviation_score"], w05[alignment[indx_align_n]])
    r06, p06 = stats.pearsonr(w06["deviation_score"], w06[alignment[indx_align_n]])
    r07, p07 = stats.pearsonr(w07["deviation_score"], w07[alignment[indx_align_n]])

    r03_1, p03_1 = stats.pearsonr(w03["N_disk"], w03[alignment[indx_align_n]])
    r04_1, p04_1 = stats.pearsonr(w04["N_disk"], w04[alignment[indx_align_n]])
    r05_1, p05_1 = stats.pearsonr(w05["N_disk"], w05[alignment[indx_align_n]])
    r06_1, p06_1 = stats.pearsonr(w06["N_disk"], w06[alignment[indx_align_n]])
    r07_1, p07_1 = stats.pearsonr(w07["N_disk"], w07[alignment[indx_align_n]])

# %% normalization
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

# separate for each numerosity
N_disk = "N_disk"
w03_a = get_sub_df_according2col_value(w03, N_disk, 21)
w03_b = get_sub_df_according2col_value(w03, N_disk, 22)
w03_c = get_sub_df_according2col_value(w03, N_disk, 23)
w03_d = get_sub_df_according2col_value(w03, N_disk, 24)
w03_e = get_sub_df_according2col_value(w03, N_disk, 25)

w04_a = get_sub_df_according2col_value(w04, N_disk, 31)
w04_b = get_sub_df_according2col_value(w04, N_disk, 32)
w04_c = get_sub_df_according2col_value(w04, N_disk, 33)
w04_d = get_sub_df_according2col_value(w04, N_disk, 34)
w04_e = get_sub_df_according2col_value(w04, N_disk, 35)

w05_a = get_sub_df_according2col_value(w05, N_disk, 41)
w05_b = get_sub_df_according2col_value(w05, N_disk, 42)
w05_c = get_sub_df_according2col_value(w05, N_disk, 43)
w05_d = get_sub_df_according2col_value(w05, N_disk, 44)
w05_e = get_sub_df_according2col_value(w05, N_disk, 45)

w06_a = get_sub_df_according2col_value(w06, N_disk, 49)
w06_b = get_sub_df_according2col_value(w06, N_disk, 50)
w06_c = get_sub_df_according2col_value(w06, N_disk, 51)
w06_d = get_sub_df_according2col_value(w06, N_disk, 52)
w06_e = get_sub_df_according2col_value(w06, N_disk, 53)

w07_a = get_sub_df_according2col_value(w07, N_disk, 54)
w07_b = get_sub_df_according2col_value(w07, N_disk, 55)
w07_c = get_sub_df_according2col_value(w07, N_disk, 56)
w07_d = get_sub_df_according2col_value(w07, N_disk, 57)
w07_e = get_sub_df_according2col_value(w07, N_disk, 58)

# calculate residuals
calculate_residuals(w03)
calculate_residuals(w04)
calculate_residuals(w05)
calculate_residuals(w06)
calculate_residuals(w07)

# %% combined r
# combine all normalized data
my_data_new = pd.concat([w03, w04, w05, w06, w07], axis = 0, sort = True)
# add colorcode by winsize
insert_new_col(my_data_new, "N_disk", 'colorcode_ws', add_color_code_by_winsize)
# single correlation combining all numerosity ranges
r, p = stats.pearsonr(my_data_new["deviation_score_norm"], my_data_new[alignment[indx_align_n] + "_norm"])
r2, p2 = stats.pearsonr(my_data_new["N_disk"], my_data_new[alignment[indx_align_n] + "_norm"])

partial_corr_all = pg.partial_corr(my_data_new, x = "deviation_score", y = alignment[indx_align_n],
                                   covar = "N_disk",
                                   method = method)
print(
        f"partial_r = {round(partial_corr_all.at['pearson', 'r'], 4)} between deviation score and align v, p = {round(partial_corr_all.at['pearson', 'p-val'], 4)}")
partial_corr = pd.concat(
        [partial_corr_03, partial_corr_04, partial_corr_05, partial_corr_06, partial_corr_07, partial_corr_all],
        axis = 0)
# partial_corr.to_excel("partial_corr%s"%(indx_align_n))
# %%plot
if see_winsize_alignv:
    # some parameters of the plot
    x_all = alignment[indx_align_n] + "_norm"
    y_all = "deviation_score_norm"
    markersize = 8
    line_color = "w"
    marker = "o"
    colors = ["cornflowerblue", "orange", "limegreen", "red", "mediumpurple"]
    labels = ['21-25', '31-35', '41-45', '49-53', '54-58']
    # plot starts her
    fig1, ax1 = plt.subplots()
    sns.regplot(x = x_all, y = y_all, data = my_data_new, x_jitter = 0.001,
                scatter_kws = {"facecolors": my_data_new["colorcode_ws"]}, color = "gray")

    # add legend for each winsize
    circle_legend = [
        Line2D([0], [0], marker = marker, color = line_color, label = labels[0], markerfacecolor = colors[0],
               markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, label = labels[1], markerfacecolor = colors[1],
               markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, label = labels[2], markerfacecolor = colors[2],
               markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, label = labels[3], markerfacecolor = colors[3],
               markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, label = labels[4], markerfacecolor = colors[4],
               markersize = markersize)]
    plt.legend(handles = circle_legend, bbox_to_anchor = (1.12, 1.05))
    # write r and p
    fig1.text(0.85, 0.65, "r = %s" % (round(r, 2)), va = "center", fontsize = 15)
    fig1.text(0.85, 0.60, "p = %s" % (round(p, 4)), va = "center", fontsize = 15)
    plt.show()
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
x_label = "Residuals of liner regression predicting normalized deviation score from numerosity"
y_label = "Residuals of liner regression predicting"
y_label2 = "normalized alignment value from numerosity"
# plot starts here
fig, axes = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
if not separate_each_n:
    sns.regplot(x = x, y = y, data = w03, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03['colorcode5levels']}, color = color, ci = ci)
    sns.regplot(x = x, y = y, data = w04, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04['colorcode5levels']}, color = color, ci = ci)
    sns.regplot(x = x, y = y, data = w05, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05['colorcode5levels']}, color = color, ci = ci)
    sns.regplot(x = x, y = y, data = w06, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06['colorcode5levels']}, color = color, ci = ci)
    sns.regplot(x = x, y = y, data = w07, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07['colorcode5levels']}, color = color, ci = ci)
    sns.regplot(x = x, y = y, data = my_data_new, x_jitter = jitter, ax = axes[1, 2],
                scatter_kws = {'facecolors': my_data_new['colorcode']}, color = color, ci = ci)

else:
    # range 21-25
    sns.regplot(x = x, y = y, data = w03_a, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03_a['']}, color = color_reg_line[0], ci = None)
    sns.regplot(x = x, y = y, data = w03_b, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03_b['colorcode5levels']}, color = color_reg_line[1], ci = None)
    sns.regplot(x = x, y = y, data = w03_c, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03_c['colorcode5levels']}, color = color_reg_line[2], ci = None)
    sns.regplot(x = x, y = y, data = w03_d, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03_d['colorcode5levels']}, color = color_reg_line[3], ci = None)
    sns.regplot(x = x, y = y, data = w03_e, x_jitter = jitter, ax = axes[0, 0],
                scatter_kws = {'facecolors': w03_e['colorcode5levels']}, color = color_reg_line[4], ci = None)
    # range 31-35
    sns.regplot(x = x, y = y, data = w04_a, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04_a['colorcode5levels']}, color = color_reg_line[0], ci = None)
    sns.regplot(x = x, y = y, data = w04_b, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04_b['colorcode5levels']}, color = color_reg_line[1], ci = None)
    sns.regplot(x = x, y = y, data = w04_c, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04_c['colorcode5levels']}, color = color_reg_line[2], ci = None)
    sns.regplot(x = x, y = y, data = w04_d, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04_d['colorcode5levels']}, color = color_reg_line[3], ci = None)
    sns.regplot(x = x, y = y, data = w04_e, x_jitter = jitter, ax = axes[0, 1],
                scatter_kws = {'facecolors': w04_e['colorcode5levels']}, color = color_reg_line[4], ci = None)
    # range 41-45
    sns.regplot(x = x, y = y, data = w05_a, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05_a['colorcode5levels']}, color = color_reg_line[0], ci = None)
    sns.regplot(x = x, y = y, data = w05_b, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05_b['colorcode5levels']}, color = color_reg_line[1], ci = None)
    sns.regplot(x = x, y = y, data = w05_c, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05_c['colorcode5levels']}, color = color_reg_line[2], ci = None)
    sns.regplot(x = x, y = y, data = w05_d, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05_d['colorcode5levels']}, color = color_reg_line[3], ci = None)
    sns.regplot(x = x, y = y, data = w05_e, x_jitter = jitter, ax = axes[0, 2],
                scatter_kws = {'facecolors': w05_e['colorcode5levels']}, color = color_reg_line[4], ci = None)
    # range 49-53
    sns.regplot(x = x, y = y, data = w06_a, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06_a['colorcode5levels']}, color = color_reg_line[0], ci = None)
    sns.regplot(x = x, y = y, data = w06_b, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06_b['colorcode5levels']}, color = color_reg_line[1], ci = None)
    sns.regplot(x = x, y = y, data = w06_c, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06_c['colorcode5levels']}, color = color_reg_line[2], ci = None)
    sns.regplot(x = x, y = y, data = w06_d, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06_d['colorcode5levels']}, color = color_reg_line[3], ci = None)
    sns.regplot(x = x, y = y, data = w06_e, x_jitter = jitter, ax = axes[1, 0],
                scatter_kws = {'facecolors': w06_e['colorcode5levels']}, color = color_reg_line[4], ci = None)
    # range 54-58
    sns.regplot(x = x, y = y, data = w07_a, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07_a['colorcode5levels']}, color = color_reg_line[0], ci = None)
    sns.regplot(x = x, y = y, data = w07_b, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07_b['colorcode5levels']}, color = color_reg_line[1], ci = None)
    sns.regplot(x = x, y = y, data = w07_c, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07_c['colorcode5levels']}, color = color_reg_line[2], ci = None)
    sns.regplot(x = x, y = y, data = w07_d, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07_d['colorcode5levels']}, color = color_reg_line[3], ci = None)
    sns.regplot(x = x, y = y, data = w07_e, x_jitter = jitter, ax = axes[1, 1],
                scatter_kws = {'facecolors': w07_e['colorcode5levels']}, color = color_reg_line[4], ci = None)
# set x, y limits
# axes[0, 0].set_ylim(-1.1, 1.1)
# axes[0, 1].set_ylim(-1.1, 1.1)
# axes[0, 2].set_ylim(-1.1, 1.1)
# axes[1, 0].set_ylim(-1.1, 1.1)
# axes[1, 1].set_ylim(-1.1, 1.1)
# axes[1, 2].set_ylim(-1.1, 1.1)
#
axes[0, 0].set_xlim(-0.5, 1)
axes[0, 1].set_xlim(-0.5, 1)
axes[0, 2].set_xlim(-0.5, 1)
axes[1, 0].set_xlim(-0.5, 1)
axes[1, 1].set_xlim(-0.5, 1)
axes[1, 2].set_xlim(-0.5, 1)

# set x,y label
axes[0, 0].set(xlabel = "", ylabel = "")
axes[0, 1].set(xlabel = "", ylabel = "")
axes[0, 2].set(xlabel = "", ylabel = "")
axes[1, 0].set(xlabel = "", ylabel = "")
axes[1, 2].set(xlabel = "", ylabel = "")
# axes[1, 1].set(xlabel = "Normalized Alignment Value: %s" % (alignment[indx_align_n]), ylabel = "")
axes[1, 1].set(xlabel = x_label, ylabel = "")
axes[1, 1].xaxis.label.set_size(20)

if not separate_each_n:
    # peasorn r
    fig.text(0.28, 0.85, "r = %s" % (round(partial_corr_03.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    fig.text(0.56, 0.85, "r = %s" % (round(partial_corr_04.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    fig.text(0.83, 0.85, "r = %s" % (round(partial_corr_05.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    fig.text(0.28, 0.43, "r = %s" % (round(partial_corr_06.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    fig.text(0.56, 0.43, "r = %s" % (round(partial_corr_07.at['pearson', 'r'], 2)), va = "center", fontsize = 15)
    fig.text(0.83, 0.43, "r = %s" % (round(partial_corr_all.at['pearson', 'r'], 2)), va = "center", fontsize = 15)

    # p-val
    fig.text(0.28, 0.81, "p = %s" % (round(partial_corr_03.at['pearson', 'p-val'], 2)), va = "center", fontsize = 15)
    fig.text(0.56, 0.81, "p = %s" % (round(partial_corr_04.at['pearson', 'p-val'], 2)), va = "center", fontsize = 15)
    fig.text(0.83, 0.81, "p = %s" % (round(partial_corr_05.at['pearson', 'p-val'], 2)), va = "center", fontsize = 15)
    # fig.text(0.28, 0.33, "p = %s" % (round(partial_corr_06.at['pearson', 'p-val'], 2)), va = "center", fontsize = 15)
    fig.text(0.28, 0.39, "p < .005", va = "center", fontsize = 15)
    # fig.text(0.56, 0.33, "p = %s" % (round(partial_corr_07.at['pearson', 'p-val'], 2)), va = "center", fontsize = 15)
    fig.text(0.56, 0.39, "p < .005", va = "center", fontsize = 15)
    # fig.text(0.83, 0.33, "p = %s" % (round(partial_corr_all.at['pearson', 'p-val'], 4)), va = "center", fontsize = 15)
    fig.text(0.83, 0.39, "p < .0001", va = "center", fontsize = 15)

fig.text(0.16, 0.89, "(a) numerosity range: 21-25", fontsize = 14)
fig.text(0.44, 0.89, "(b) numerosity range: 31-35", fontsize = 14)
fig.text(0.71, 0.89, "(c) numerosity range: 41-45", fontsize = 14)
fig.text(0.16, 0.47, "(d) numerosity range: 49-53", fontsize = 14)
fig.text(0.44, 0.47, "(e) numerosity range: 54-58", fontsize = 14)
fig.text(0.71, 0.47, "(f) all numerosities)", fontsize = 12)

# fig.text(0.08, 0.5, 'Normalized Deviation Score', va = 'center', rotation = 'vertical', fontsize = 20)
fig.text(0.06, 0.5, y_label, va = 'center', rotation = 'vertical', fontsize = 20)
fig.text(0.08, 0.5, y_label2, va = 'center', rotation = 'vertical', fontsize = 20)
colors_c = ["#ffd6cc", "#ffad99", "#ff8566", "#ff5c33", "#ff3300"]
colors_nc = ["#ccccff", "#9999ff", "#6666ff", "#3333ff", "#0000ff"]
labels03 = ['21', '22', '23', '23', '25']
circle_legend = add_legend(colors_c, colors_nc)
axes[0, 0].legend(handles = circle_legend, labelspacing = 0.01,
            ncol = 2, columnspacing = 0.01, borderpad = None,
            frameon = False, bbox_to_anchor = (0.6, 0., 0.5, 0.5))

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
sns.regplot(x = x, y = y, data = w03, x_jitter = jitter, ax = axes[0, 0],
            scatter_kws = {'facecolors': w03['colorcode']}, color = color)
sns.regplot(x = x, y = y, data = w04, x_jitter = jitter, ax = axes[0, 1],
            scatter_kws = {'facecolors': w04['colorcode']}, color = color)
sns.regplot(x = x, y = y, data = w05, x_jitter = jitter, ax = axes[0, 2],
            scatter_kws = {'facecolors': w05['colorcode']}, color = color)
sns.regplot(x = x, y = y, data = w06, x_jitter = jitter, ax = axes[1, 0],
            scatter_kws = {'facecolors': w06['colorcode']}, color = color)
sns.regplot(x = x, y = y, data = w07, x_jitter = jitter, ax = axes[1, 1],
            scatter_kws = {'facecolors': w07['colorcode']}, color = color)

# set x, y limits
axes[0, 0].set_ylim(-0.1, 1.1)
axes[0, 1].set_ylim(-0.1, 1.1)
axes[0, 2].set_ylim(-0.1, 1.1)
axes[1, 0].set_ylim(-0.1, 1.1)
axes[1, 1].set_ylim(-0.1, 1.1)

# set x,y label
axes[0, 0].set(xlabel = "", ylabel = "")
axes[0, 1].set(xlabel = "", ylabel = "")
axes[0, 2].set(xlabel = "", ylabel = "")
axes[1, 0].set(xlabel = "", ylabel = "")
axes[1, 1].set(xlabel = "numerosity", ylabel = "")

axes[1, 1].xaxis.label.set_size(20)

fig.text(0.07, 0.5, "alignment value: %s" % (alignment[indx_align_n]), va = 'center', rotation = 'vertical',
         fontsize = 20)

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
# %% debug and write to excel
if is_debug:
    col_names_stimuli = list(stimuli_to_merge_ori.columns)
    col_names_data = list(data_to_merge)
    col_names_my_data = list(my_data)
if save_fig:
    fig.savefig("try.svg")