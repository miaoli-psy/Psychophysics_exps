import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from src.analysis.exp1_local_density_analysis import get_result_dict_loc_density, interplote_result_dict_start, \
    dict_pix_to_deg, get_data_to_fit_list, get_data_to_fit_list_no_normolized, get_avrg_dict, \
    get_avrg_result_dict_loc_density, get_avrg_data_to_fit, interplote_avrg_result_dict_start, avrg_dict_pix_to_deg
from src.commons.process_dataframe import keep_valid_columns, process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list

if __name__ == '__main__':
    plot_each_display = True
    normolization = False
    plot_average_display = False
    PATH = "../displays/"
    FILE = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILE)
    COL = ["displayN",
           "positions",
           "occupancyArea",
           "density_itemsperdeg2",
           "winsize",
           "crowdingcons",
           "list_index",
           "N_disk"]
    # process positions
    process_col(stimuli_df, "positions", str_to_list)
    # keep useful cols
    stimuli_df = keep_valid_columns(stimuli_df, COL)

    # crowding and no-crowding df
    stimuli_df_c = stimuli_df[(stimuli_df['crowdingcons'] == 1)]
    stimuli_df_nc = stimuli_df[(stimuli_df['crowdingcons'] == 0)]

    # positions into dictionary, key is numerosity
    crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_c.groupby('N_disk')}
    no_crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_nc.groupby('N_disk')}

    # get local density distribution
    result_dict_c = get_result_dict_loc_density(crowding_dic)
    result_dict_nc = get_result_dict_loc_density(no_crowding_dic)

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

    # %% plot each display
    numerosity_list = [21, 22, 23, 24, 25,
                       31, 32, 33, 34, 35,
                       41, 42, 43, 44, 45,
                       49, 50, 51, 52, 53,
                       54, 55, 56, 57, 58]
    if normolization:
        datac_to_fit = get_data_to_fit_list(result_dict_c_list)
        datanc_to_fit = get_data_to_fit_list(result_dict_nc_list)
    else:
        datac_to_fit = get_data_to_fit_list_no_normolized(result_dict_c_list)
        datanc_to_fit = get_data_to_fit_list_no_normolized(result_dict_nc_list)

    starting_n = 15

    if plot_each_display:
        figc, cxs = plt.subplots(5, 5, figsize = (30, 20), sharex = True, sharey = True)
        cxs = cxs.ravel()
        datac_to_fit1 = []
        for i in datac_to_fit:
            for display in i.values():
                display_new = []
                for j in display:
                    display_new.append(j[starting_n:])
                datac_to_fit1.append(display_new)

        datanc_to_fit1 = []
        for i in datanc_to_fit:
            for display in i.values():
                display_new = []
                for j in display:
                    display_new.append(j[starting_n:])
                datanc_to_fit1.append(display_new)

        for index, cx in enumerate(cxs):
            for i in range(0, 5):
                cx.plot(datac_to_fit1[index][i][:, 0], datac_to_fit1[index][i][:, 1], "r--",  alpha = 0.5)
                cx.plot(datanc_to_fit1[index][i][:, 0], datanc_to_fit1[index][i][:, 1], "b--", alpha = 0.5)
            cx.title.set_text("numerosity %s" % numerosity_list[index])
        plt.ylim([0, 1])
        plt.show()
        figc.savefig("try.svg")

    # %% plot average
    numerosity_list = [21, 22, 23, 24, 25,
                       31, 32, 33, 34, 35,
                       41, 42, 43, 44, 45,
                       49, 50, 51, 52, 53,
                       54, 55, 56, 57, 58]

    if plot_average_display:

        deg = 2 # 最高项系数the highest order
        if deg >= 2:
            label_c = "polynomial fit radial"
            label_nc = "polynomial fit tangential"
        elif deg == 1:
            label_c = "linear fit radial"
            label_nc = "linear fit tangential"

        avrg_crowding_dic = get_avrg_dict(crowding_dic)
        avrg_no_crowding_dic = get_avrg_dict(no_crowding_dic)

        # get local density distribution
        avrg_res_dict_c = get_avrg_result_dict_loc_density(avrg_crowding_dic)
        avrg_res_dict_nc = get_avrg_result_dict_loc_density(avrg_no_crowding_dic)

        # local density values start from 100 pix
        avrg_res_dict_c = interplote_avrg_result_dict_start(avrg_res_dict_c)
        avrg_res_dict_nc = interplote_avrg_result_dict_start(avrg_res_dict_nc)
        # pix to deg
        avrg_result_dict_c = avrg_dict_pix_to_deg(avrg_res_dict_c, 1)
        avrg_result_dict_nc = avrg_dict_pix_to_deg(avrg_res_dict_nc, 1)
        # data to fit
        avrg_dict_c_to_fit = get_avrg_data_to_fit(avrg_result_dict_c)
        avrg_dict_nc_to_fit = get_avrg_data_to_fit(avrg_result_dict_nc)


        # plot all
        start_n = 0
        x_avrg_c_list = [avrg_dict_c_to_fit[n][start_n:, 0] for n in numerosity_list]
        y_avrg_c_list = [avrg_dict_c_to_fit[n][start_n:, 1] for n in numerosity_list]
        x_avrg_nc_list = [avrg_dict_nc_to_fit[n][start_n:, 0] for n in numerosity_list]
        y_avrg_nc_list = [avrg_dict_nc_to_fit[n][start_n:, 1] for n in numerosity_list]

        polyfit_crowding_avrg_list = [np.poly1d(np.polyfit(x = x_avrg_c, y = y_avrg_c, deg = deg)) for
                                      x_avrg_c, y_avrg_c in zip(x_avrg_c_list, y_avrg_c_list)]
        polyfit_no_crowding_avrg_list = [np.poly1d(np.polyfit(x = x_avrg_nc, y = y_avrg_nc, deg = deg)) for
                                         x_avrg_nc, y_avrg_nc in zip(x_avrg_nc_list, y_avrg_nc_list)]

        figb, bxs = plt.subplots(5, 5, figsize = (25, 15), sharex = True, sharey = True)
        bxs = bxs.ravel()
        for index, bx in enumerate(bxs):
            bx.plot(x_avrg_c_list[index], y_avrg_c_list[index], "ro", size = 2, alpha = 0.5)
            bx.plot(x_avrg_nc_list[index], y_avrg_nc_list[index], "bo", size = 2,alpha = 0.5)
            bx.plot(x_avrg_c_list[index], polyfit_crowding_avrg_list[index](x_avrg_c_list[index]), "r-")
            bx.plot(x_avrg_nc_list[index], polyfit_no_crowding_avrg_list[index](x_avrg_nc_list[index]), "b-")
            bx.title.set_text("numerosity %s" % numerosity_list[index])
        # plt.ylim([0, 1])
        # plt.xlim([3.8, 16])
        plt.show()
