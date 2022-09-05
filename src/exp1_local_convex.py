import pandas as pd
import matplotlib.pyplot as plt

from src.analysis.exp1_local_density_analysis import get_result_dict_loc_density, interplote_result_dict_start, \
    dict_pix_to_deg, get_data_to_fit_list, get_data_to_fit_list_no_normolized, get_result_dict_loc_convex_hull
from src.commons.process_dataframe import keep_valid_columns, process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list

if __name__ == '__main__':
    plot_each_display = True
    normolization = False
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

    # get local convexhull distribution
    result_dict_c = get_result_dict_loc_convex_hull(crowding_dic)
    result_dict_nc = get_result_dict_loc_convex_hull(no_crowding_dic)

    # make sure the x-axis start with 100 pix
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

    if plot_each_display:
        figc, cxs = plt.subplots(5, 5, figsize = (30, 20), sharex = True, sharey = True)
        cxs = cxs.ravel()
        datac_to_fit1 = []
        for i in datac_to_fit:
            for display in i.values():
                display_new = []
                for j in display:
                    display_new.append(j[7:])
                datac_to_fit1.append(display_new)

        datanc_to_fit1 = []
        for i in datanc_to_fit:
            for display in i.values():
                display_new = []
                for j in display:
                    display_new.append(j[7:])
                datanc_to_fit1.append(display_new)

        for index, cx in enumerate(cxs):
            for i in range(0, 5):
                cx.plot(datac_to_fit1[index][i][:, 0], datac_to_fit1[index][i][:, 1], "r--", alpha = 0.5)
                cx.plot(datanc_to_fit1[index][i][:, 0], datanc_to_fit1[index][i][:, 1], "b--", alpha = 0.5)
            cx.title.set_text("numerosity %s" % numerosity_list[index])
        plt.show()
        figc.savefig("try.svg")



