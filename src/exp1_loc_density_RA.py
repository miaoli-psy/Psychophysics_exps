import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from src.commons.process_dataframe import get_sub_df_according2col_value, insert_new_col_from_two_cols
from src.analysis.exp1_local_density_analysis import normolizedLD, get_data2fit

from src.commons.process_str import str_to_list


def is_ra_score_high(ra_score: float, mean: float) -> int:
    if ra_score >= mean:
        return 1
    else:
        return 0


if __name__ == '__main__':
    PATH = "../displays/"
    FILE = "uodate_stim_info_RAscores.xlsx"
    stimuli_df = pd.read_excel(PATH + FILE)

    # calculate mean of the RA scores for each numerosity range
    winsize_list = [0.3, 0.4, 0.5, 0.6, 0.7]
    stimuli_df_list = [get_sub_df_according2col_value(stimuli_df, col_name = "winsize", col_value = winsize) for winsize
                       in winsize_list]

    mean_ra_score_list = list()
    for df in stimuli_df_list:
        mean_ra_score_list.append(df["align_v_size6"].mean())

    mean = list()
    for i in mean_ra_score_list:
        mean += ([i] * 50)

    stimuli_df.sort_values(by = ["winsize"], inplace = True)
    stimuli_df["mean_ra"] = mean

    # new column split display by high and low RA scores
    insert_new_col_from_two_cols(stimuli_df, "align_v_size6", "mean_ra", "ra_group", is_ra_score_high)

    # high and low ra group
    high_ra_df = stimuli_df[stimuli_df["ra_group"] == 1]
    low_ra_df = stimuli_df[stimuli_df["ra_group"] == 0]

    h = {k: g['result_density_projection'].tolist() for k, g in high_ra_df.groupby('N_disk')}
    l = {k: g['result_density_projection'].tolist() for k, g in low_ra_df.groupby('N_disk')}

    a = str_to_list(h[25][0])

    high_ra_dict = dict()
    for key, value in h.items():
        lst = []
        for display in value:
            lst.append(str_to_list(display))
            high_ra_dict.update({key: lst})

    low_ra_dict = dict()
    for key, value in l.items():
        lst = []
        for display in value:
            lst.append(str_to_list(display))
            low_ra_dict.update({key: lst})

    high_ra_dict_no_repli = dict()
    for key, value in high_ra_dict.items():
        new_v = []
        for display in value:
            saved = []
            for i, tuple in enumerate(display):
                if i == 0:
                    saved.append(tuple)
                else:
                    if tuple[1] > display[i - 1][1]:
                        saved.append(tuple)
            new_v.append(saved)
        high_ra_dict_no_repli.update({key: new_v})

    low_ra_dict_no_repli = dict()
    for key, value in low_ra_dict.items():
        new_v = []
        for display in value:
            saved = []
            for i, tuple in enumerate(display):
                if i == 0:
                    saved.append(tuple)
                else:
                    if tuple[1] > display[i - 1][1]:
                        saved.append(tuple)
            new_v.append(saved)
        low_ra_dict_no_repli.update({key: new_v})

    h_to_fit = {}
    for key, value in high_ra_dict_no_repli.items():
        new_v_lst = []
        for display in value:
            new_v_lst.append(get_data2fit(display))
            h_to_fit.update({key: new_v_lst})

    l_to_fit = {}
    for key, value in low_ra_dict_no_repli.items():
        new_v_lst = []
        for display in value:
            new_v_lst.append(get_data2fit(display))
            l_to_fit.update({key: new_v_lst})

    fitted_h = {}
    for key, value in h_to_fit.items():
        new_v_lst = []
        for display in value:
            new_v_lst.append(np.polyfit(x = display[:, 0], y = display[:, 1], deg = 2)[0])
            fitted_h.update({key: new_v_lst})

    fitted_l = {}
    for key, value in l_to_fit.items():
        new_v_lst = []
        for display in value:
            new_v_lst.append(np.polyfit(x = display[:, 0], y = display[:, 1], deg = 2)[0])
            fitted_l.update({key: new_v_lst})

    data_2ttesth03, data_2ttesth04, data_2ttesth05, data_2ttesth06, data_2ttesth07 = [], [], [], [], []

    for key, value in fitted_h.items():
        for v in value:
            if 21 <= key <= 25:
                data_2ttesth03.append(v)
            elif 31 <= key <= 35:
                data_2ttesth04.append(v)
            elif 41 <= key <= 45:
                data_2ttesth05.append(v)
            elif 49 <= key <= 53:
                data_2ttesth06.append(v)
            elif 54 <= key <= 58:
                data_2ttesth07.append(v)

    data_2ttestl03, data_2ttestl04, data_2ttestl05, data_2ttestl06, data_2ttestl07 = [], [], [], [], []

    for key, value in fitted_l.items():
        for v in value:
            if 21 <= key <= 25:
                data_2ttestl03.append(v)
            elif 31 <= key <= 35:
                data_2ttestl04.append(v)
            elif 41 <= key <= 45:
                data_2ttestl05.append(v)
            elif 49 <= key <= 53:
                data_2ttestl06.append(v)
            elif 54 <= key <= 58:
                data_2ttestl07.append(v)

    t03, p03 = stats.ttest_ind(data_2ttestl03, data_2ttesth03)
    t04, p04 = stats.ttest_ind(data_2ttestl04, data_2ttesth04)
    t05, p05 = stats.ttest_ind(data_2ttestl05, data_2ttesth05)
    t06, p06 = stats.ttest_ind(data_2ttestl06, data_2ttesth06)
    t07, p07 = stats.ttest_ind(data_2ttestl07, data_2ttesth07)

    plot_numerosity = 55
    res_h = high_ra_dict_no_repli[plot_numerosity][1]
    res_l = low_ra_dict_no_repli[plot_numerosity][1]

    x_h = [t[0] for t in res_h]
    y_h = [t[1] for t in res_h]
    x_l = [t[0] for t in res_l]
    y_l = [t[1] for t in res_l]
    norm_y_h = normolizedLD(y_h)
    norm_y_l = normolizedLD(y_l)

    np_arr_h = np.array([x_h, norm_y_h]).transpose()
    np_arr_l = np.array([x_l, norm_y_l]).transpose()

    fig1, ax1 = plt.subplots()
    ax1.plot(np_arr_h[:, 0], np_arr_h[:, 1], 'r--', alpha = 0.5, label = "high RA display")
    ax1.plot(np_arr_l[:, 0], np_arr_l[:, 1], 'b--', alpha = 0.5, label = "low RA display")
    plt.legend(loc = 'best')
    ax1.set_xlabel("Eccentricity", fontsize = 15)
    ax1.set_ylabel("Normalized Local Density", fontsize = 15)
    ax1.set_title("Sample displays(numerosity %s): high vs. low" % plot_numerosity, fontsize = 12)
    plt.show()
    fig1.savefig("try1.svg")