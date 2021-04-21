# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-19 23:18
IDE: PyCharm
Introduction:
"""
from src.constants.exp3a_pilot_constants import SUB_DF_COLS2CHECK
from src.plots.exp3a_pilot_plot import drawplot

from src.commons.process_dataframe import get_sub_df_according2col_value
from src.analysis.exp3a_pilot_analysis import get_output_results, get_piovt_table

import pandas as pd

if __name__ == "__main__":
    is_debug = True
    write_to_excel = False
    save_plots = False

    PATH = "../data/exp3_data/exp3_pilot_data/"
    DATAFILE = "exp3a_preprocessed.xlsx"
    mydata = pd.read_excel(PATH + DATAFILE)

    # exp conditions in separate df for plots
    refc = get_sub_df_according2col_value(mydata, "refCrowding", 1)
    refnc = get_sub_df_according2col_value(mydata, "refCrowding", 0)
    # below are four exp conditions
    refcprobec = get_sub_df_according2col_value(refc, "probeCrowding", 1)
    refcprobenc = get_sub_df_according2col_value(refc, "probeCrowding", 0)
    refncprobec = get_sub_df_according2col_value(refnc, "probeCrowding", 1)
    refncprobenc = get_sub_df_according2col_value(refnc, "probeCrowding", 0)

    # %% output dataframe
    # pivot table
    pt = get_piovt_table(mydata)
    # groupby()
    results_df = get_output_results(mydata)
    # add means of result_df
    results_df.loc["mean_across_all_participants"] = results_df.mean()
    # add means across participants by different group (ref first or not)
    results_df.loc["mean_of_probe_first_participants"] = results_df.iloc[0:5].mean()
    results_df.loc["mean_of_ref_first_participants"] = results_df.iloc[6:11].mean()

    # %% plots
    x_values = [34, 36, 38, 40, 42, 44, 46]
    condi_list = ["rc_pc", "rc_pnc", "rnc_pc", "rnc_pnc"]
    # row number: possible 0-14; 0-11 (12 participants) 12 all participants, 13 probe first group, 14 ref first
    # group
    for row in range(15):
        drawplot(results_df, x_values, condi_list, row_number = row, savefig = save_plots)


    if is_debug:
        col_names = list(mydata.columns)
        df2check = mydata[SUB_DF_COLS2CHECK]

    if write_to_excel:
        mydata.to_excel("preprocess_exp3a_pilot.xlsx")
        pt.to_excel("pivot_table_exp3a_pilot.xlsx")
