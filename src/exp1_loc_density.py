# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-05 19:14
IDE: PyCharm
Introduction:
"""
import copy

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from scipy.stats import poisson

from src.analysis.exp1_local_density_analysis import dict_pix_to_deg, get_result_dict, interplote_result_dict_start, \
    get_fitted_res_cdf_poisson, get_sample_plot_x_y, normolizedLD, get_data2fit, get_data_to_fit_list, \
    get_fitted_power_list, get_data_to_ttest, get_avrg_dict, get_avrg_result_dict, interplote_avrg_result_dict_start, \
    avrg_dict_pix_to_deg, get_avrg_data_to_fit
from src.commons.fitfuncs import fit_poisson_cdf
from src.commons.process_dataframe import process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list


if __name__ == '__main__':
    save_plot = False
    fit_poisson = False
    fit_polynomial = True
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
    k_03 = [21, 22, 23, 24, 25]
    k_04 = [31, 32, 33, 34, 35]
    k_05 = [41, 42, 43, 44, 45]
    k_06 = [49, 50, 51, 52, 53]
    k_07 = [54, 55, 56, 57, 58]
    k_list = [k_03, k_04, k_05, k_06, k_07]
    # data to fit
    result_dict_c_list = [get_sub_dict(result_dict_c, k) for k in k_list]
    result_dict_nc_list = [get_sub_dict(result_dict_nc, k) for k in k_list]
    # %% fit polynomial
    datac_to_fit = get_data_to_fit_list(result_dict_c_list)
    datanc_to_fit = get_data_to_fit_list(result_dict_nc_list)

    # 最高项系数
    deg = 2
    fitted_c = get_fitted_power_list(datac_to_fit, deg = deg)
    fitted_nc = get_fitted_power_list(datanc_to_fit, deg = deg)

    # data for ttest
    datac_ttest = get_data_to_ttest(fitted_c)
    datanc_ttest = get_data_to_ttest(fitted_nc)

    # ttest here
    ts, ps = list(), list()
    for win_index in range(0, 5):
        t, p = stats.ttest_rel(datac_ttest[win_index], datanc_ttest[win_index])
        ts.append(t)
        ps.append(p)
    print(f"t = %s" % ts)
    print(f"p = %s" % ps)

    if fit_polynomial:
        # sample crowding and no-crowding display
        res_c = result_dict_c_list[4][55][0]
        res_nc = result_dict_nc_list[4][55][1]
        x_crowding = [t[0] for t in res_c]
        y_crowding = [t[1] for t in res_c]
        x_ncrowding = [t[0] for t in res_nc]
        y_ncrowding = [t[1] for t in res_nc]
        norm_y_crowding = normolizedLD(y_crowding)
        norm_y_ncrowding = normolizedLD(y_ncrowding)

        np_arr_crowding = np.array([x_crowding, norm_y_crowding]).transpose()
        np_arr_ncrowding = np.array([x_ncrowding, norm_y_ncrowding]).transpose()
        # fit here
        polyfit_crowding = np.poly1d(np.polyfit(x= np_arr_crowding[:, 0], y = norm_y_crowding, deg = deg))
        polyfit_ncrowding = np.poly1d(np.polyfit(x= np_arr_ncrowding[:, 0], y = norm_y_ncrowding, deg = deg))

        fig1, ax1 = plt.subplots()
        if deg == 2:
            label_c = "polynomial fit crowding"
            label_nc = "polynomial fit no-crowding"
        elif deg == 1:
            label_c = "linear fit crowding"
            label_nc = "linear fit no-crowding"
        ax1.plot(np_arr_crowding[:, 0], np_arr_crowding[:, 1], 'ro', alpha = 0.5, label = "crowding display")
        ax1.plot(np_arr_ncrowding[:, 0], np_arr_ncrowding[:, 1], 'bo', alpha = 0.5, label = "no-crowding display")
        ax1.plot(np_arr_crowding[:, 0], polyfit_crowding(np_arr_crowding[:, 0]), 'r--', label = label_c)
        ax1.plot(np_arr_ncrowding[:, 0], polyfit_ncrowding(np_arr_ncrowding[:, 0]), 'b--', label = label_nc)
        plt.legend(loc = 'best')
        ax1.set_xlabel("Eccentricity", fontsize = 15)
        ax1.set_ylabel("Local density", fontsize = 15)
        ax1.set_title("Sample displays(numerosity 55): no crowding vs. crowding", fontsize = 12)
        plt.show()

    #%% fit possion cdf here
    if fit_poisson:
        fitted_c_list = [get_fitted_res_cdf_poisson(sub_dict) for sub_dict in result_dict_c_list]
        fitted_nc_list = [get_fitted_res_cdf_poisson(sub_dict) for sub_dict in result_dict_nc_list]
        # collect all fitted lambda here
        fitted_lambda_c = np.column_stack(fitted_c_list)
        fitted_lambda_nc = np.column_stack(fitted_nc_list)

        # independent t test
        # index 0, 0 -> crowding vs. no-crowding in winsize 03
        # index 1, 1 -> winsize 04
        # index 2, 2 -> winsize 05
        # index 3, 3 -> winsize 06
        # index 4, 4 -> winsize 07
        t, p = stats.ttest_ind(fitted_lambda_c[:, 4], fitted_lambda_nc[:, 4])

        # %% plot
        # a sample fit
        # no-crowding data
        to_plot_array = get_sample_plot_x_y(result_dict_c_list[4], key = 55, list_index = 0)
        # crowding data
        to_plot_array2 = get_sample_plot_x_y(result_dict_nc_list[4], key = 55, list_index = 0)
        # plot starts here
        fig, ax = plt.subplots()
        # plot original data
        ax.plot(to_plot_array[:, 0], to_plot_array[:, 1], 'bo', label = "no-crowding display", alpha = 0.5)
        ax.plot(to_plot_array2[:, 0], to_plot_array2[:, 1], 'ro', label = "crowding display", alpha = 0.5)
        # get fitted y
        opty = fit_poisson_cdf(to_plot_array)
        opty2 = fit_poisson_cdf(to_plot_array2)
        # plot fitted data
        ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty), 'b--', label = 'CDF Poisson fit no-crowding')
        ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty2), 'r--', label = 'CDF Poisson fit crowding')
        # customize the plot
        plt.legend(loc = 'best')
        ax.set_xlabel("Eccentricity", fontsize = 15)
        ax.set_ylabel("Local density", fontsize = 15)
        ax.set_title("Sample displays(numerosity 55): no crowding vs. crowding", fontsize = 12)

        plt.show()

    #%% averaged local density for each numerosity
    avrg_crowding_dic = get_avrg_dict(crowding_dic)
    avrg_no_crowding_dic = get_avrg_dict(no_crowding_dic)
    # get local density distribution
    avrg_res_dict_c = get_avrg_result_dict(avrg_crowding_dic)
    avrg_res_dict_nc = get_avrg_result_dict(avrg_no_crowding_dic)

    # local density values start from 100 pix
    avrg_res_dict_c = interplote_avrg_result_dict_start(avrg_res_dict_c)
    avrg_res_dict_nc = interplote_avrg_result_dict_start(avrg_res_dict_nc)
    # pix to deg
    avrg_result_dict_c = avrg_dict_pix_to_deg(avrg_res_dict_c, 1)
    avrg_result_dict_nc = avrg_dict_pix_to_deg(avrg_res_dict_nc, 1)
    # data to fit
    avrg_dict_c_to_fit = get_avrg_data_to_fit(avrg_result_dict_c)
    avrg_dict_nc_to_fit = get_avrg_data_to_fit(avrg_result_dict_nc)

    # fit one average data to polynomial
    numerosity = 32
    x_avrg_c = avrg_dict_c_to_fit[numerosity][:, 0]
    x_avrg_nc = avrg_dict_nc_to_fit[numerosity][:, 0]
    y_avrg_c = avrg_dict_c_to_fit[numerosity][:, 1]
    y_avrg_nc = avrg_dict_nc_to_fit[numerosity][:, 1]

    #fit here
    polyfit_crowding_avrg = np.poly1d(np.polyfit(x = x_avrg_c, y = y_avrg_c, deg = deg))
    polyfit_ncrowding_avrg = np.poly1d(np.polyfit(x = x_avrg_nc, y = y_avrg_nc, deg = deg))

    fig2, ax2 = plt.subplots()
    ax2.plot(x_avrg_c, y_avrg_c, 'ro', alpha = 0.1, label = "crowding displays")
    ax2.plot(x_avrg_nc, y_avrg_nc, 'bo', alpha = 0.1, label = "no-crowding displays")
    ax2.plot(x_avrg_c, polyfit_crowding_avrg(x_avrg_c), 'r--', label = label_c)
    ax2.plot(x_avrg_nc, polyfit_ncrowding_avrg(x_avrg_nc), 'b--', label = label_nc)
    plt.legend(loc = 'best')
    ax2.set_xlabel("Eccentricity", fontsize = 15)
    ax2.set_ylabel("Local density", fontsize = 15)
    ax2.set_title("Average displays(numerosity %s): no crowding vs. crowding" %numerosity, fontsize = 12)
    plt.show()

    if save_plot:
        fig.savefig("sampleplot.svg")
