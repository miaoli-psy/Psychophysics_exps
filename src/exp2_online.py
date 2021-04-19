# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-04-19 10:54
IDE: PyCharm
Introduction: exp2(online) results plot: 1. deviation socre as a funtion of clustering, seprate winsize.
2. deviation score as a fucntion of winsize, across all clustering levels.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.commons.process_dataframe import get_col_names, get_sub_df_according2col_value


def plot_with_clustering(data2plot_sep_ws, x, y, hue, capsize, errwidth, palette, alpha, ci, savefig = True):
    sns.set(style = "white", color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    fig, axes = plt.subplots(1, 2, figsize = (13, 6), sharex = False, sharey = True)
    axes = axes.ravel()
    for i, ax in enumerate(axes):
        sns.barplot(x = x, y = y, data = data2plot_sep_ws[i], ax = ax, hue = hue, capsize = capsize,
                    errwidth = errwidth, palette = palette, alpha = alpha, ci = ci)
        sns.swarmplot(x = x, y = y, data = data2plot_sep_ws[i], ax = ax, hue = hue, palette = palette, dodge = True,
                      alpha = alpha)
        if i == 0:
            handles, labels = ax.get_legend_handles_labels()
            labels = ["tangential", "radial", "others"]
            ax.legend(handles[3:], labels, loc = "lower center", ncol = 2, fontsize = 12)
        elif i == 1:
            ax.legend([], [], frameon = False)

        # add y = 0
        ax.axhline(y = 0, color = "k", linewidth = 0.5)

        # hide borders
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    plt.show()
    if savefig:
        fig.savefig("exp2_res.svg", bbox_inches = 'tight')


def plot_no_clustering(data2plot, x, y, hue, capsize, palette, errwidth, alpha, savefig = True):
    sns.set(style = "white", color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    fig, ax = plt.subplots(figsize = (6, 4.5), sharex = False, sharey = True)
    sns.barplot(x = x, y = y, data = data2plot, hue = hue, capsize = capsize, palette = palette, alpha = alpha,
                ci = 68, ax = ax, errwidth = errwidth)
    sns.swarmplot(x = x, y = y, data = data2plot, hue = hue, palette = palette, dodge = True, alpha = 0.65, ax = ax)
    # reset bar width
    for i, patch in enumerate(ax.patches):
        curr_width = patch.get_width()
        new_width = curr_width / 2
        patch.set_width(new_width)
        diff = curr_width - curr_width / 2
        patch.set_x(patch.get_x() + diff / 2)
    # set legend
    handles, labels = ax.get_legend_handles_labels()
    labels = ["tangential", "radial", "others"]
    ax.legend(handles[3:], labels, loc = "lower center", ncol = 2, fontsize = 12)

    # add y = 0
    ax.axhline(y = 0, color = "k", linewidth = 0.5)

    # hide borders
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    if savefig:
        fig.savefig("exp2_noclustering.svg", bbox_inches = 'tight')
    plt.show()


if __name__ == '__main__':
    debug = True
    save_fig = False
    see_clustering_level = True

    # read data
    PATH = "../data/exp2_data_online/"
    DATA = "exp2_online_preprocessed.xlsx"
    data = pd.read_excel(PATH + DATA)

    # data to plot: different clustering levels
    if see_clustering_level:
        data2plot = data["deviation"].groupby(
                [data["crowding"], data["winsize"], data["clustering"], data["participantID"]]).mean()
        data2plot = data2plot.reset_index(level = ["crowding", "winsize", "clustering", "participantID"])

        # data sep winsize
        data_sep_ws = [get_sub_df_according2col_value(data2plot, "winsize", winsize) for winsize in [0.4, 0.6]]

        # some parameters
        x = "clustering"
        y = "deviation"
        hue = "crowding"
        errwidth = 2
        capsize = 0.05
        alpha = 0.5
        palette = ["royalblue", "orangered", "grey"]
        ci = 68
        # plot starts here
        plot_with_clustering(data2plot_sep_ws = data_sep_ws,
                             x = x,
                             y = y,
                             hue = hue,
                             capsize = capsize,
                             errwidth = errwidth,
                             palette = palette,
                             alpha = alpha,
                             ci = ci,
                             savefig = save_fig)

    # no-clustering level
    data2plot = data["deviation"].groupby(
            [data["crowding"], data["winsize"], data["participantID"]]).mean()
    data2plot = data2plot.reset_index(level = ["crowding", "winsize", "participantID"])

    # some parameters
    x = "winsize"
    y = "deviation"
    hue = "crowding"
    errwidth = 2
    capsize = 0.05
    alpha = 0.5
    palette = ["royalblue", "orangered", "grey"]
    ci = 68
    # plot starts here
    plot_no_clustering(data2plot = data2plot,
                       x = x,
                       y = y,
                       hue = hue,
                       capsize = capsize,
                       palette = palette,
                       alpha = alpha,
                       errwidth = errwidth,
                       savefig = save_fig)
    if debug:
        col_names = get_col_names(data)
