# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-05 19:14
IDE: PyCharm
Introduction:
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from scipy.stats import poisson

from src.analysis.exp1_local_density_analysis import dict_pix_to_deg, get_result_dict, interplote_result_dict_start, \
    get_fitted_res, get_sample_plot_x_y
from src.commons.fitfuncs import get_lambda
from src.commons.process_dataframe import process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list


if __name__ == '__main__':
    save_plot = False
    PATH = "../displays/"
    FILE = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILE)

    # process positions
    process_col(stimuli_df, "positions", str_to_list)
    # crowding and no-crowding df
    stimuli_df_c = stimuli_df[(stimuli_df['crowdingcons'] == 1)]
    stimuli_df_nc = stimuli_df[(stimuli_df['crowdingcons'] == 0)]
    # positions into dictionary, key is numerosity
    crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_c.groupby('N_disk')}
    no_crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_nc.groupby('N_disk')}
    # get local density distribution
    result_dict_c = get_result_dict(crowding_dic)
    result_dict_nc = get_result_dict(no_crowding_dic)
    # make sure the local density values start from (100,..)
    result_dict_c = interplote_result_dict_start(result_dict_c)
    result_dict_nc = interplote_result_dict_start(result_dict_nc)
    # covert pixel to deg
    result_dict_c = dict_pix_to_deg(result_dict_c, 1)
    result_dict_nc = dict_pix_to_deg(result_dict_nc, 1)
    # possible keys
    k_c_03 = [21, 22, 23, 24, 25]
    k_c_04 = [31, 32, 33, 34, 35]
    k_c_05 = [41, 42, 43, 44, 45]
    k_c_06 = [49, 50, 51, 52, 53]
    k_c_07 = [54, 55, 56, 57, 58]
    # data to fit
    res_dict_c_03 = get_sub_dict(result_dict_c, k_c_03)
    res_dict_c_04 = get_sub_dict(result_dict_c, k_c_04)
    res_dict_c_05 = get_sub_dict(result_dict_c, k_c_05)
    res_dict_c_06 = get_sub_dict(result_dict_c, k_c_06)
    res_dict_c_07 = get_sub_dict(result_dict_c, k_c_07)

    res_dict_nc_03 = get_sub_dict(result_dict_nc, k_c_03)
    res_dict_nc_04 = get_sub_dict(result_dict_nc, k_c_04)
    res_dict_nc_05 = get_sub_dict(result_dict_nc, k_c_05)
    res_dict_nc_06 = get_sub_dict(result_dict_nc, k_c_06)
    res_dict_nc_07 = get_sub_dict(result_dict_nc, k_c_07)
    # fit here
    fitted_c_03 = get_fitted_res(res_dict_c_03)
    fitted_c_04 = get_fitted_res(res_dict_c_04)
    fitted_c_05 = get_fitted_res(res_dict_c_05)
    fitted_c_06 = get_fitted_res(res_dict_c_06)
    fitted_c_07 = get_fitted_res(res_dict_c_07)

    fitted_nc_03 = get_fitted_res(res_dict_nc_03)
    fitted_nc_04 = get_fitted_res(res_dict_nc_04)
    fitted_nc_05 = get_fitted_res(res_dict_nc_05)
    fitted_nc_06 = get_fitted_res(res_dict_nc_06)
    fitted_nc_07 = get_fitted_res(res_dict_nc_07)

    # collect all fitted lambda here
    fitted_lambda = np.column_stack([fitted_c_03,
                                     fitted_c_04,
                                     fitted_c_05,
                                     fitted_c_06,
                                     fitted_c_07,
                                     fitted_nc_03,
                                     fitted_nc_04,
                                     fitted_nc_05,
                                     fitted_nc_06,
                                     fitted_nc_07])

    # independent t test
    # index 0, 5 -> crowding vs. no-crowding in winsize 03
    # index 1, 6 -> winsize 04
    # index 2, 7 -> winsize 05
    # index 3, 8 -> winsize 06
    # index 4, 9 -> winsize 07
    t, p = stats.ttest_ind(fitted_lambda[:, 0], fitted_lambda[:, 5])

    # a sample fit
    # no-crowding data
    to_plot_array = get_sample_plot_x_y(res_dict_nc_07, key = 55, list_index = 0)
    # crowding data
    to_plot_array2 = get_sample_plot_x_y(res_dict_c_07, key = 55, list_index = 0)
    # plot starts here
    fig, ax = plt.subplots()
    # plot original data
    ax.plot(to_plot_array[:, 0], to_plot_array[:, 1], 'bo', label = "no-crowding display", alpha = 0.5)
    ax.plot(to_plot_array2[:, 0], to_plot_array2[:, 1], 'ro', label = "crowding display", alpha = 0.5)
    # get fitted y
    opty = get_lambda(to_plot_array)
    opty2 = get_lambda(to_plot_array2)
    # plot fitted data
    ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty), 'b+', label = 'CDF Poisson fit no-crowding')
    ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty2), 'r+', label = 'CDF Poisson fit crowding')
    # customize the plot
    plt.legend(loc = 'best')
    ax.set_xlabel("Eccentricity", fontsize = 15)
    ax.set_ylabel("Local density", fontsize = 15)
    ax.set_title("Sample displays(numerosity 55): no crowding vs. crowding", fontsize = 12)
    plt.show()
    if save_plot:
        fig.savefig("sampleplot.svg")
