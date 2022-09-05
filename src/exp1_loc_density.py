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


from src.analysis.exp1_local_density_analysis import dict_pix_to_deg, get_result_dict, interplote_result_dict_start, \
    get_fitted_res_cdf_poisson, get_sample_plot_x_y, normolizedLD, get_data2fit, get_data_to_fit_list, \
    get_fitted_power_list, get_data_to_ttest, get_avrg_dict, get_avrg_result_dict, interplote_avrg_result_dict_start, \
    avrg_dict_pix_to_deg, get_avrg_data_to_fit, get_data_to_fit_list_no_normolized
from src.commons.fitfuncs import fit_poisson_cdf
from src.commons.process_dataframe import process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list


def get_diff_x_y(n: int, to_fit_dict_c: dict, to_fit_dict_nc: dict, fit_poly = True):
    # ori x values
    c_x_list = to_fit_dict_c[n][:, 0].tolist()
    nc_x_list = to_fit_dict_nc[n][:, 0].tolist()
    # ori y values
    c_y_list = to_fit_dict_c[n][:, 1].tolist()
    nc_y_list = to_fit_dict_nc[n][:, 1].tolist()
    if fit_poly:
        polyfit_crowding_avrg = np.poly1d(np.polyfit(x = c_x_list, y = c_y_list, deg = 2))
        c_y_list = polyfit_crowding_avrg(c_x_list).tolist()
        polyfit_no_crowding_avrg = np.poly1d(np.polyfit(x = nc_x_list, y = nc_y_list, deg = 2))
        nc_y_list = polyfit_no_crowding_avrg(nc_x_list).tolist()

    # x 的第一个值是一样的
    assert (c_x_list[0] == nc_x_list[0])
    # pair x, y
    c_xy_dict = dict(zip(c_x_list, c_y_list))
    nc_xy_dict = dict(zip(nc_x_list, nc_y_list))

    # new_y=nc_y_list-c_y_list
    # key: union x, value: new y
    diff_x_y_dict = dict()
    x_intersection = list(set(c_x_list) & set(nc_x_list))
    x_c_unique = set(c_x_list) - set(nc_x_list)
    x_nc_unique = set(nc_x_list) - set(c_x_list)

    for x in x_intersection:
        diff_x_y_dict[x] = nc_xy_dict[x] - c_xy_dict[x]

    # for x in x_c_unique:
    #     # find previous x of nc_x_list
    #     curr_nc_x = __find_previous_x(x, nc_x_list)
    #     diff_x_y_dict[x] = nc_xy_dict[curr_nc_x] - c_xy_dict[x]
    #
    # for x in x_nc_unique:
    #     # find previous x of c_x_list
    #     curr_c_x = __find_previous_x(x, c_x_list)
    #     diff_x_y_dict[x] = nc_xy_dict[x] - c_xy_dict[curr_c_x]

    res_x = sorted(list(diff_x_y_dict.keys()))
    res_y = list()
    for x in res_x:
        res_y.append(diff_x_y_dict[x])

    assert (res_y[0] == nc_y_list[0] - c_y_list[0])

    return res_x, res_y


def __find_previous_x(target_x: float, x_list: list) -> float:
    # 对从小到大的x_list找到第一个比target_x大的数，再往前找一步
    for curr_index, curr_x in enumerate(x_list):
        if curr_x > target_x:
            return x_list[curr_index - 1]
    # edge case: target_x > x_list[-1]
    if target_x > x_list[-1]:
        return x_list[-1]


assert (__find_previous_x(2.3, [1, 2.1, 3, 5]) == 2.1)

if __name__ == '__main__':
    save_plot = False
    fit_poisson = False
    fit_polynomial = False
    plot_each_display = True
    plot_average_display = False
    plot_loc_density_diff = False
    normolization = False
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
    if normolization:
        datac_to_fit = get_data_to_fit_list(result_dict_c_list)
        datanc_to_fit = get_data_to_fit_list(result_dict_nc_list)
    else:
        datac_to_fit = get_data_to_fit_list_no_normolized(result_dict_c_list)
        datanc_to_fit = get_data_to_fit_list_no_normolized(result_dict_nc_list)

    # 最高项系数the highest order
    deg = 2

    if deg == 2:
        label_c = "polynomial fit radial"
        label_nc = "polynomial fit tangential"
    elif deg == 1:
        label_c = "linear fit radial"
        label_nc = "linear fit tangential"

    fitted_c = get_fitted_power_list(datac_to_fit, deg = deg)
    fitted_nc = get_fitted_power_list(datanc_to_fit, deg = deg)

    # data for ttest
    datac_ttest = get_data_to_ttest(fitted_c)
    datanc_ttest = get_data_to_ttest(fitted_nc)
    # covert to dataframe
    dfc = pd.DataFrame(datac_ttest).T
    dfnc = pd.DataFrame(datanc_ttest).T
    dfc.to_excel("c.xlsx")
    dfnc.to_excel("nc.xlsx")

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
        N = 55
        res_c = result_dict_c_list[4][N][0]
        res_nc = result_dict_nc_list[4][N][1]
        x_crowding = [t[0] for t in res_c]
        y_crowding = [t[1] for t in res_c]
        x_ncrowding = [t[0] for t in res_nc]
        y_ncrowding = [t[1] for t in res_nc]
        norm_y_crowding = normolizedLD(y_crowding)
        norm_y_ncrowding = normolizedLD(y_ncrowding)

        np_arr_crowding = np.array([x_crowding, norm_y_crowding]).transpose()
        np_arr_ncrowding = np.array([x_ncrowding, norm_y_ncrowding]).transpose()
        # fit here
        polyfit_crowding = np.poly1d(np.polyfit(x = np_arr_crowding[:, 0], y = norm_y_crowding, deg = deg))
        polyfit_ncrowding = np.poly1d(np.polyfit(x = np_arr_ncrowding[:, 0], y = norm_y_ncrowding, deg = deg))

        fig1, ax1 = plt.subplots()
        ax1.plot(np_arr_crowding[:, 0], np_arr_crowding[:, 1], 'ro', alpha = 0.5, label = "radial display")
        ax1.plot(np_arr_ncrowding[:, 0], np_arr_ncrowding[:, 1], 'bo', alpha = 0.5, label = "tangential display")
        ax1.plot(np_arr_crowding[:, 0], polyfit_crowding(np_arr_crowding[:, 0]), 'r--', label = label_c)
        ax1.plot(np_arr_ncrowding[:, 0], polyfit_ncrowding(np_arr_ncrowding[:, 0]), 'b--', label = label_nc)
        plt.legend(loc = 'best')
        ax1.set_xlabel("Eccentricity", fontsize = 15)
        ax1.set_ylabel("Normalized Local Density", fontsize = 15)
        ax1.set_title("Sample displays(numerosity 55): tangential vs. radial", fontsize = 12)
        plt.show()
        fig1.savefig("try1.svg")

    # %% fit possion cdf here
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
        ax.plot(to_plot_array[:, 0], to_plot_array[:, 1], 'bo', label = "data", alpha = 0.5)
        # ax.plot(to_plot_array2[:, 0], to_plot_array2[:, 1], 'ro', label = "crowding display", alpha = 0.5)
        # get fitted y
        opty = fit_poisson_cdf(to_plot_array)
        opty2 = fit_poisson_cdf(to_plot_array2)
        # plot fitted data
        # ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty), 'b--',
        #         label = 'CDF Poisson fit')
        # ax.plot(to_plot_array[:, 0], poisson.cdf(to_plot_array[:, 0], opty2), 'r--', label = 'CDF Poisson fit crowding')
        # customize the plot
        plt.legend(loc = 'best')
        # ax.set_xlabel("Eccentricity", fontsize = 15)
        # ax.set_ylabel("Local density", fontsize = 15)
        # ax.set_title("Sample displays(numerosity 55): no crowding vs. crowding", fontsize = 12)

        plt.show()
    # %% plot each display
    numerosity_list = [21, 22, 23, 24, 25,
                       31, 32, 33, 34, 35,
                       41, 42, 43, 44, 45,
                       49, 50, 51, 52, 53,
                       54, 55, 56, 57, 58]
    if plot_each_display:
        figc, cxs = plt.subplots(5, 5, figsize = (30, 20), sharex = True, sharey = True)
        cxs = cxs.ravel()
        datac_to_fit1 = []
        for i in datac_to_fit:
            for display in i.values():
                datac_to_fit1.append(display)
        datanc_to_fit1 = []
        for i in datanc_to_fit:
            for display in i.values():
                datanc_to_fit1.append(display)
        for index, cx in enumerate(cxs):
            for i in range(0, 5):
                cx.plot(datac_to_fit1[index][i][:, 0], datac_to_fit1[index][i][:, 1], "r--", alpha = 0.5)
                cx.plot(datanc_to_fit1[index][i][:, 0], datanc_to_fit1[index][i][:, 1], "b--", alpha = 0.5)
            cx.title.set_text("numerosity %s" % numerosity_list[index])
        plt.show()
        # figc.savefig("try.svg")

    # %% averaged local density for each numerosity
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
    numerosity = 21
    x_avrg_c = avrg_dict_c_to_fit[numerosity][:, 0]
    x_avrg_nc = avrg_dict_nc_to_fit[numerosity][:, 0]
    y_avrg_c = avrg_dict_c_to_fit[numerosity][:, 1]
    y_avrg_nc = avrg_dict_nc_to_fit[numerosity][:, 1]

    # fit here
    polyfit_crowding_avrg = np.poly1d(np.polyfit(x = x_avrg_c, y = y_avrg_c, deg = deg))
    polyfit_ncrowding_avrg = np.poly1d(np.polyfit(x = x_avrg_nc, y = y_avrg_nc, deg = deg))

    fig2, ax2 = plt.subplots()
    ax2.plot(x_avrg_c, y_avrg_c, 'ro', alpha = 0.1, label = "radial displays")
    ax2.plot(x_avrg_nc, y_avrg_nc, 'bo', alpha = 0.1, label = "tangential displays")
    ax2.plot(x_avrg_c, polyfit_crowding_avrg(x_avrg_c), 'r--', label = label_c)
    ax2.plot(x_avrg_nc, polyfit_ncrowding_avrg(x_avrg_nc), 'b--', label = label_nc)
    plt.legend(loc = 'best')
    ax2.set_xlabel("Eccentricity", fontsize = 15)
    ax2.set_ylabel("Local density", fontsize = 15)
    ax2.set_title("Average displays(numerosity %s): tangential vs. radial" % numerosity, fontsize = 12)
    plt.show()

    if plot_average_display:
        # plot all
        x_avrg_c_list = [avrg_dict_c_to_fit[n][:, 0] for n in numerosity_list]
        y_avrg_c_list = [avrg_dict_c_to_fit[n][:, 1] for n in numerosity_list]
        x_avrg_nc_list = [avrg_dict_nc_to_fit[n][:, 0] for n in numerosity_list]
        y_avrg_nc_list = [avrg_dict_nc_to_fit[n][:, 1] for n in numerosity_list]

        polyfit_crowding_avrg_list = [np.poly1d(np.polyfit(x = x_avrg_c, y = y_avrg_c, deg = deg)) for
                                      x_avrg_c, y_avrg_c in zip(x_avrg_c_list, y_avrg_c_list)]
        polyfit_no_crowding_avrg_list = [np.poly1d(np.polyfit(x = x_avrg_nc, y = y_avrg_nc, deg = deg)) for
                                         x_avrg_nc, y_avrg_nc in zip(x_avrg_nc_list, y_avrg_nc_list)]

        figb, bxs = plt.subplots(5, 5, figsize = (25, 15), sharex = True, sharey = True)
        bxs = bxs.ravel()
        for index, bx in enumerate(bxs):
            bx.plot(x_avrg_c_list[index], y_avrg_c_list[index], "r--", alpha = 0.5)
            bx.plot(x_avrg_nc_list[index], y_avrg_nc_list[index], "--", alpha = 0.5)
            bx.plot(x_avrg_c_list[index], polyfit_crowding_avrg_list[index](x_avrg_c_list[index]), "r-")
            bx.plot(x_avrg_nc_list[index], polyfit_no_crowding_avrg_list[index](x_avrg_nc_list[index]), "b-")
            bx.title.set_text("numerosity %s" % numerosity_list[index])
        plt.show()
    # %% plot local density differences
    if plot_loc_density_diff:
        to_plot_diff_array_list = list()
        for n in numerosity_list:
            x_list_diff, y_list_diff = get_diff_x_y(n, to_fit_dict_c = avrg_dict_c_to_fit,
                                                    to_fit_dict_nc = avrg_dict_nc_to_fit,
                                                    fit_poly = False)

            to_plot_diff_array_list.append(np.array([x_list_diff, y_list_diff]).T)

        figd, dxs = plt.subplots(5, 5, figsize = (40, 30), sharex = True, sharey = True)
        dxs = dxs.ravel()
        for i, to_plot_diff_array in enumerate(to_plot_diff_array_list):
            dxs[i].plot(to_plot_diff_array[:, 0], to_plot_diff_array[:, 1])
            dxs[i].axhline(y = 0)
        for dx in dxs:
            dx.set_ylim(-0.5, 0.5)
        plt.show()
        figd.savefig("diff_nofitting.svg")

    # plot different curves: 5 in a subplot
        plot_dict = {0: [0, 1, 2, 3, 4],
                     1: [5, 6, 7, 8, 9],
                     2: [10, 11, 12, 13, 14],
                     3: [15, 16, 17, 18, 19],
                     4: [20, 21, 22, 23, 24]}

        fige, exs = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
        exs = exs.ravel()

        for index, ex in enumerate(exs):
            if index < 5:
                for i in range(0, 5):
                    ex.plot(to_plot_diff_array_list[plot_dict[index][i]][:, 0],
                            to_plot_diff_array_list[plot_dict[index][i]][:, 1],
                            label = "%s" %i, alpha = 0.5)
                    ex.legend()
            ex.set_ylim(-0.5, 0.5)
            ex.axhline(y = 0, color = "gray", linestyle = "--")
        plt.show()
        fige.savefig("try.svg")

    if save_plot:
        fig.savefig("sampleplot.svg")
        figc.savefig("eachdisplay.svg")
        figb.savefig("avrgdisplay.svg")