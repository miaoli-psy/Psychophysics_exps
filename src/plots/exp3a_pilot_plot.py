# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-22 21:15
IDE: PyCharm
Introduction:
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def __get_label4plot(condi: str) -> str:
    if condi == "rc_pc":
        return "crowding reference and crowding probe"
    elif condi == "rc_pnc":
        return "crowding reference and no-crowding probe"
    elif condi == "rnc_pc":
        return "no-crowding reference and crowding probe"
    elif condi == "rnc_pnc":
        return "no-crowding reference and no-crowding probe"
    else:
        raise Exception(f"the condi {condi} does not exist.")


def __get_title4plot(row_number: int) -> str:
    if row_number == 12:
        return "all participants"
    elif row_number == 13:
        return "probe first group"
    elif row_number == 14:
        return "ref first group"
    elif row_number <= 5:
        return "pp%s probe first" % (row_number + 1)
    elif 6 <= row_number <= 11:
        return "pp%s ref first" % (row_number + 1)
    else:
        raise Exception(f"the select y values {row_number} was incorrect.")


def plot_seprate_condi(data, x, y, hue, style, ci = 68, err_style = "bars", dashes = False, alpha = 0.5,
                       palette = ["royalblue", "orangered"], markers = ["o", "o"], title = "", savefig = False):
    fig, ax = plt.subplots(figsize = (6, 4.5))
    ax = sns.lineplot(x = x,
                      y = y,
                      data = data,
                      hue = hue,
                      err_style = err_style,
                      palette = palette,
                      alpha = alpha,
                      style = style,
                      dashes = dashes,
                      markers = markers,
                      ci = ci)
    ax.set_ylim(0, 1)
    ax.axhline(0.5, ls = '--', color = "k", linewidth = 0.5)
    ax.set_title(title)
    plt.ylabel("proportion response probe more")
    plt.xlabel("probe numerosity")
    if savefig:
        plt.savefig("try.svg")
    plt.show()


def plot_allcondi_inone(data, x, y, hue, style, ci = 68, err_style = "bars", dashes = False, alpha = 0.5, markers = ["o", "o", 'o', 'o'], title = "", savefig = False):
    fig, ax = plt.subplots(figsize = (6, 4.5))
    ax = sns.lineplot(x = x,
                      y = y,
                      data = data,
                      hue = hue,
                      err_style = err_style,
                      alpha = alpha,
                      style = style,
                      dashes = dashes,
                      markers = markers,
                      ci = ci)
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.axhline(0.5, ls = '--', color = "k", linewidth = 0.5)
    plt.ylabel("proportion response probe more")
    plt.xlabel("probe numerosity")
    if savefig:
        plt.savefig("try.svg")
    plt.show()
