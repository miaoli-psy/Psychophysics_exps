# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-05 14:29
IDE: PyCharm
Introduction:
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from statannot import add_stat_annotation

PATH = "../../data/exp1_rerun_data/"
DATA_FILE2PLOT = "exp1_rerun_data2plot.xlsx"
save_plot = False

df_toplot = pd.read_excel(PATH + DATA_FILE2PLOT)
x = "winsize"
y = "deviation_score"
data = df_toplot
hue = "crowdingcons"

fig, ax = plt.subplots(figsize = (9, 7))
ax = sns.barplot(x = x,
                 y = y,
                 data = df_toplot,
                 hue = hue,
                 capsize = .05,
                 palette = ["royalblue", "orangered"],
                 alpha = 0.5,
                 ci = 68)

ax = sns.swarmplot(x = x,
                   y = y,
                   data = df_toplot,
                   hue = hue,
                   palette = ["royalblue", "orangered"],
                   dodge = True,
                   alpha = 0.65)

box_pairs = [((0.4, 0), (0.4, 1)),
             ((0.5, 0), (0.5, 1)),
             ((0.6, 0), (0.6, 1)),
             ((0.7, 0), (0.7, 1)),
             ((0.3, 0), (0.6, 1)),
             ((0.3, 0), (0.7, 1))]
text_annot_custom = ["*", "p = .067", "*", "*", "*", "*"]

# add asterisk and pairs
add_stat_annotation(ax, data = data, x = x, y = y, hue = hue, box_pairs = box_pairs,
                    text_annot_custom = text_annot_custom,
                    perform_stat_test = False,
                    pvalues = [0, 0, 0, 0, 0, 0],
                    loc = 'inside', verbose = 0)

# customize the plot
xlabel = "Numerosity"
ylabel = "Deviation Score"
ax.set_xlabel(xlabel, fontsize = 15, labelpad = 12)
ax.set_ylabel(ylabel, fontsize = 15)
ax.set_ylim([-15, 25])
ax.set_xticklabels(["21-25", "31-35", "41-45", "49-53", "54-58"])
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
# customize legend
handles, labels = ax.get_legend_handles_labels()
labels = ["no-crowding", "crowding"]
ax.legend(handles[2:], labels, loc = "lower center", ncol = 2, fontsize = 12)
# hide borders
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# add liney = 0
ax.axhline(y = 0, color = "k", linewidth = 0.5)
plt.show()
if save_plot:
    fig.savefig("exp1_results_plot.svg")