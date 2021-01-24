# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-14 20:21
IDE: PyCharm
Introduction:
"""
import pandas as pd
from collections import Counter
import statistics
import seaborn as sns
import matplotlib.pyplot as plt

from src.analysis.exp1_raidal_displays_analysis2 import get_angle_range, count_ndisc_in_range, get_avrg_alignment_v, \
    counter2list, \
    cal_alignment_value, get_angle_range_no_overlap, get_beam_n, get_one_beam_n_from_list
from src.commons.process_dataframe import get_col_names, get_sub_df_according2col_value
from src.commons.process_str import str_to_list
from src.point.polar_point import get_polar_coordinates

is_debug = True
indi_display = True
write_to_excel = True

# read stimuli display
PATH = "../displays/"
FILENAME = "update_stim_info_full.xlsx"
stimuli_df = pd.read_excel(PATH + FILENAME)
# TODO count 3 or more/ 4 or more
count_edge = 3
# TODO see number of beam regions
beam_region_info = True
# get and insert new col "n_beams" into stimuli dataframe
# number of beams that contains 1, 2, 3, 4, 5, 6 disc
# stimuli_df["align_v_size12"] = stimuli_df["positions_list"].apply(get_avrg_alignment_v, args = (12, count_edge))
base_col_name = "align_v_size"
for i in range(1, 13):
    stimuli_df[base_col_name + str(i)] = stimuli_df["positions_list"].apply(get_avrg_alignment_v, args = (i, count_edge))

stimuli_df["beam_n"] = stimuli_df["positions_list"].apply(get_beam_n, args = (6,))

if beam_region_info:
    # put those 6 values in separate columns
    for i in range(0, 6):
        stimuli_df["n_beam%s" % (i + 1)] = stimuli_df["beam_n"].apply(get_one_beam_n_from_list, args = (i,))
    # get sub df that contained needed columns
    n_beams_to_plot1 = stimuli_df[["n_beam1", "crowdingcons", "winsize"]]
    n_beams_to_plot2 = stimuli_df[["n_beam2", "crowdingcons", "winsize"]]
    n_beams_to_plot3 = stimuli_df[["n_beam3", "crowdingcons", "winsize"]]
    n_beams_to_plot4 = stimuli_df[["n_beam4", "crowdingcons", "winsize"]]
    n_beams_to_plot5 = stimuli_df[["n_beam5", "crowdingcons", "winsize"]]
    n_beams_to_plot6 = stimuli_df[["n_beam6", "crowdingcons", "winsize"]]
    # rename to "n_beam", be ready to contact
    n_beams_to_plot1 = n_beams_to_plot1.rename(columns = {"n_beam1": "n_beam"})
    n_beams_to_plot2 = n_beams_to_plot2.rename(columns = {"n_beam2": "n_beam"})
    n_beams_to_plot3 = n_beams_to_plot3.rename(columns = {"n_beam3": "n_beam"})
    n_beams_to_plot4 = n_beams_to_plot4.rename(columns = {"n_beam4": "n_beam"})
    n_beams_to_plot5 = n_beams_to_plot5.rename(columns = {"n_beam5": "n_beam"})
    n_beams_to_plot6 = n_beams_to_plot6.rename(columns = {"n_beam6": "n_beam"})
    # set second column - will be x-axis in the plot
    nl1 = [1 for i in range(0, 250)]
    nl2 = [2 for i in range(0, 250)]
    nl3 = [3 for i in range(0, 250)]
    nl4 = [4 for i in range(0, 250)]
    nl5 = [5 for i in range(0, 250)]
    nl6 = [6 for i in range(0, 250)]
    n_beams_to_plot1["N_disc_in_beam"] = nl1
    n_beams_to_plot2["N_disc_in_beam"] = nl2
    n_beams_to_plot3["N_disc_in_beam"] = nl3
    n_beams_to_plot4["N_disc_in_beam"] = nl4
    n_beams_to_plot5["N_disc_in_beam"] = nl5
    n_beams_to_plot6["N_disc_in_beam"] = nl6
    # get the dataframe, to be plot
    n_beams_to_plot = pd.concat(
            [n_beams_to_plot1, n_beams_to_plot2, n_beams_to_plot3, n_beams_to_plot4, n_beams_to_plot5,
             n_beams_to_plot6],
            axis = 0, sort = True)
    # separate for each numerosity range
    n_beams_to_plot_w03 = get_sub_df_according2col_value(n_beams_to_plot, "winsize", 0.3)
    n_beams_to_plot_w04 = get_sub_df_according2col_value(n_beams_to_plot, "winsize", 0.4)
    n_beams_to_plot_w05 = get_sub_df_according2col_value(n_beams_to_plot, "winsize", 0.5)
    n_beams_to_plot_w06 = get_sub_df_according2col_value(n_beams_to_plot, "winsize", 0.6)
    n_beams_to_plot_w07 = get_sub_df_according2col_value(n_beams_to_plot, "winsize", 0.7)
    # plots starts here
    fig, axes = plt.subplots(2, 3, figsize = (13, 6), sharex = True, sharey = True)
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot_w03, ax = axes[0, 0], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot_w04, ax = axes[0, 1], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot_w05, ax = axes[0, 2], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot_w06, ax = axes[1, 0], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot_w07, ax = axes[1, 1], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    sns.boxplot(x = "N_disc_in_beam", y = "n_beam", data = n_beams_to_plot, ax = axes[1, 2], hue = "crowdingcons",
                palette = ["royalblue", "orangered"])
    # set x,y label
    axes[0, 0].set(xlabel = "", ylabel = "")
    axes[0, 1].set(xlabel = "", ylabel = "")
    axes[0, 2].set(xlabel = "", ylabel = "")
    axes[1, 0].set(xlabel = "", ylabel = "")
    axes[1, 1].set(xlabel = "Number of discs in one beam region", ylabel = "")
    axes[1, 1].xaxis.label.set_size(15)
    axes[1, 2].set(xlabel = "", ylabel = "")
    # some text
    fig.text(0.15, 0.89, "(a) numerosity range: 21-25", fontsize = 15)
    fig.text(0.43, 0.89, "(b) numerosity range: 31-35", fontsize = 15)
    fig.text(0.70, 0.89, "(c) numerosity range: 41-45", fontsize = 15)
    fig.text(0.15, 0.47, "(d) numerosity range: 49-53", fontsize = 15)
    fig.text(0.43, 0.47, "(e) numerosity range: 54-58", fontsize = 15)
    fig.text(0.70, 0.47, "(e) all numerosities", fontsize = 15)
    fig.text(0.08, 0.5, 'Number of beam regions', va = 'center', rotation = 'vertical', fontsize = 15)
    # keep only one legend
    handles, labels = axes[0, 1].get_legend_handles_labels()
    labels = ["no-crowding", "crowding"]
    axes[0, 1].legend(handles[:], labels, loc = "best")
    axes[0, 0].get_legend().remove()
    axes[0, 2].get_legend().remove()
    axes[1, 0].get_legend().remove()
    axes[1, 1].get_legend().remove()
    axes[1, 2].get_legend().remove()
    plt.show()

# individual display alignment value
if indi_display:
    display_n = 248  # 0-249
    posis_str = stimuli_df.positions_list[display_n]
    posis = str_to_list(posis_str)
    # get polar positions for a single display
    polar_posis = get_polar_coordinates(posis)

    # some parameters, started and ended where
    ini_start_angle = polar_posis[0][0]
    angle_size = 12
    ini_end_angle = ini_start_angle + angle_size
    # get the ranges
    my_range_overlap = get_angle_range(polar_posis, ini_start_angle = ini_start_angle, ini_end_angle = ini_end_angle)
    align_v_list = list()
    n_beamlist = list()
    for i in range(0, len(my_range_overlap)):
        # get different ranges starting from each disc
        my_range = get_angle_range_no_overlap(my_range_overlap, start_n = i)
        # get number of discs in each range
        ndisc_list = list()
        for beam in my_range:
            ndisc = count_ndisc_in_range(polar_posis, beam[0], beam[1])
            ndisc_list.append(ndisc)
        # get number of beams that contains 1, 2, 3, 4, 5, 6 discs
        count_beams = Counter(ndisc_list)
        n_beams = counter2list(count_beams)
        n_beamlist.append(n_beams)
        align_v = cal_alignment_value(n_beams, count_edge = count_edge)
        align_v_list.append(align_v)
        # mean
        alignment_v = statistics.mean(align_v_list)
if is_debug:
    col_names = get_col_names(stimuli_df)

if write_to_excel:
    stimuli_df.to_excel("try.xlsx")