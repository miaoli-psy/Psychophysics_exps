# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 23:18
IDE: PyCharm
Introduction:
"""
from src.constants.exp3a_pilot_constants import SUB_DF_COLS2CHECK
from src.plots.exp3a_pilot_plot import plot_seprate_condi, plot_allcondi_inone

from src.commons.process_dataframe import get_sub_df_according2col_value
from src.analysis.exp3a_pilot_analysis import get_output_results, get_output_results_sep_condi

import pandas as pd

if __name__ == "__main__":
    is_debug = True
    see_4condi_in_all = False
    save_plots = True

    PATH = "../data/exp3_data/exp3_pilot_data/"
    DATAFILE = "exp3a_preprocessed.xlsx"
    mydata = pd.read_excel(PATH + DATAFILE)

    # exclude subject TODO
    exclude = False
    exclude_n = 8

    # exp conditions in separate df for plots
    refc = get_sub_df_according2col_value(mydata, "refCrowding", 1)
    refnc = get_sub_df_according2col_value(mydata, "refCrowding", 0)
    probec = get_sub_df_according2col_value(mydata, "probeCrowding", 1)
    probenc = get_sub_df_according2col_value(mydata, "probeCrowding", 0)
    # below are four exp conditions
    refcprobec = get_sub_df_according2col_value(refc, "probeCrowding", 1)
    refcprobenc = get_sub_df_according2col_value(refc, "probeCrowding", 0)
    refncprobec = get_sub_df_according2col_value(refnc, "probeCrowding", 1)
    refncprobenc = get_sub_df_according2col_value(refnc, "probeCrowding", 0)

    # %% plots - see all together
    # all data
    x = "probeN"
    y = "is_resp_probe_more"
    hue = "ref_probe_condi"
    if see_4condi_in_all:
        alldata = get_output_results(mydata)
        plot_allcondi_inone(alldata, x = x, y = y, hue = hue, style = hue)
        # ref first group
        ref_first = get_sub_df_according2col_value(mydata, "ref_first", 1)
        plot_allcondi_inone(ref_first, x = x, y = y, hue = hue, style = hue, title = "ref first group")

        # probe first group
        probe_first = get_sub_df_according2col_value(mydata, "ref_first", 0)
        plot_allcondi_inone(ref_first, x = x, y = y, hue = hue, style = hue, title = "probe first group")

        # see each pp
        pp = list(range(1, 13))
        results_all_pp = [get_sub_df_according2col_value(mydata, "participantN", p) for p in pp]

        for i, pp_result in enumerate(results_all_pp):
            plot_allcondi_inone(pp_result, x = "probeN", y = "is_resp_probe_more", hue = "ref_probe_condi",
                                style = "ref_probe_condi", title = "participant%s" % (i+1))

    # %% plot separate condition
    hue = "refCrowding"
    # plot 2 probe conditions
    probec = get_output_results_sep_condi(probec)
    probenc = get_output_results_sep_condi(probenc)
    if exclude:
        probec = probec[probec["participantN"] != exclude_n]
        probenc = probenc[probenc["participantN"] != exclude_n]
    plot_seprate_condi(probec, x = x, y = y, hue = hue, style = hue, savefig = save_plots, title = "probec")
    plot_seprate_condi(probenc, x = x, y = y, hue = hue, style = hue, savefig = save_plots, title = "probenc")

    if is_debug:
        col_names = list(mydata.columns)
