# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-02-09 13:21
IDE: PyCharm
Introduction: Partial correlation between performance (deviation score) with local density's polynomial fit a
"""
import pandas as pd
import pingouin as pg
from scipy.stats import stats
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from src.analysis.exp1_alignment_analysis import add_color_code_by_crowdingcons, add_color_code_5levels, \
    get_analysis_dataframe, get_data_to_analysis, normalize_deviation, normalize_zerotoone, rename_norm_col
from src.commons.process_dataframe import keep_valid_columns, insert_new_col, insert_new_col_from_two_cols, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES4, KEPT_COL_NAMES5


def calculate_residuals(input_df):
    lin_fit_results_Y = sm.ols(formula = "deviation_score_norm ~ N_disk", data = input_df).fit()
    input_df["rY"] = lin_fit_results_Y.resid

    lin_fit_results_X = sm.ols(formula = "a_values_norm ~ N_disk", data = input_df).fit()
    input_df["rX"] = lin_fit_results_X.resid


def normalize_minusonetozero(input_df: pd.DataFrame, to_normalize_col: str):
    """
    :param input_df: dataframe contains col alignment values
    :param to_normalize_col: alignment_col name
    :return: new dataframe contains only normalized alignment_col range within(0, 1)
    """
    min_max_scaler = MinMaxScaler(feature_range = (-1, 0))
    return pd.DataFrame(min_max_scaler.fit_transform(input_df[[to_normalize_col]]), columns = [to_normalize_col])


if __name__ == '__main__':
    # TODO set parameters
    crowdingcons = 2  # 0, 1, 2 for no-crowding, crowding and all data
    parrtial_corr = True
    # read stimuli info and data
    PATH_DATA = "../data/exp1_rerun_data/"
    FILENAME_DATA = "cleanedTotalData_fullinfo_v2.xlsx"
    PATH_STIM = "../displays/"
    FILENAME_STIM = "update_stim_info_full.xlsx"
    data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)
    stimuli_to_merge = pd.read_excel(PATH_STIM + FILENAME_STIM)
    # keep needed cols
    stimuli_to_merge = keep_valid_columns(stimuli_to_merge, KEPT_COL_NAMES4)
    # merge data with stimuli info
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = "left",
                      on = ["index_stimuliInfo", "N_disk", "crowdingcons", "winsize"])
    # preprocess
    my_data = keep_valid_columns(all_df, KEPT_COL_NAMES5)
    # add color coded for crowding and no-crowding displays
    insert_new_col(my_data, "crowdingcons", 'colorcode', add_color_code_by_crowdingcons)
    # color coded
    insert_new_col_from_two_cols(my_data, "N_disk", "crowdingcons", "colorcode5levels", add_color_code_5levels)

    # %% correaltions
    winsize_list = [0.3, 0.4, 0.5, 0.6, 0.7]
    my_data = get_analysis_dataframe(my_data, crowding = crowdingcons)
    df_list_beforegb = [get_sub_df_according2col_value(my_data, "winsize", winsize) for winsize in winsize_list]
    df_list = [get_data_to_analysis(df, "deviation_score", "a_values", "N_disk", "list_index", "colorcode",
                                    "colorcode5levels") for df in df_list_beforegb]
    # correaltion paramters
    method = "pearson"
    x = "a_values"
    y = "deviation_score"
    covar = "N_disk"
    # corr: a values and numerosity
    corr_av_ndisc = list()
    corr_av_ndisc = [stats.pearsonr(sub_df[x], sub_df[covar]) for sub_df in df_list]
    if parrtial_corr:
        partial_corr_res_list = [pg.partial_corr(df, x = x, y = y, covar = covar, method = method) for df in df_list]
    else:
        corr_res_list = [stats.pearsonr(sub_df[x], sub_df[y]) for sub_df in df_list]
    # %% normalization
    df_list_norm_deviation = [normalize_deviation(df) for df in df_list]
    df_list_norm_avs = [normalize_minusonetozero(df, to_normalize_col = "a_values") for df in df_list]
    # rename normed cols
    old_name_dev = "deviation_score"
    new_name_dev = "deviation_score_norm"
    old_name_av = "a_values"
    new_name_av = "a_values_norm"
    df_list_norm_deviation = [rename_norm_col(df, old_name_dev, new_name_dev) for df in df_list_norm_deviation]
    df_list_norm_avs = [rename_norm_col(df, old_name_av, new_name_av) for df in df_list_norm_avs]
    # contact orig dataframe with new normalized dataframe
    df_list = [pd.concat([df, df_list_norm_deviation[index], df_list_norm_avs[index]], axis = 1) for index, df in
               enumerate(df_list)]
    # %% cal residuals (to plot)
    [calculate_residuals(df) for df in df_list]
    # %%plot partial corr between deviation score and a values (polynomial fit)
    sns.set(style = "white", color_codes = True)
    sns.set_style("ticks", {"xtick.major.size": 5, "ytick.major.size": 3})
    # some parameters
    x = "rX"
    # x = "a_values_norm"
    y = "rY"
    # y = "deviation_score"
    jitter = 0.001
    ci = 95
    color = "gray"
    x_label = "Residuals of liner regression predicting normalized"
    x_label2 = " local density fit (a-values) from numerosity"
    y_label = "Residuals of liner regression predicting"
    y_label2 = "normalized deviation score from numerosity"

    fig, axs = plt.subplots(2, 3, figsize = (16, 8), sharex = True, sharey = True)
    axs = axs.ravel()
    for index, df in enumerate(df_list):
        sns.regplot(x = x, y = y, data = df, x_jitter = jitter, ax = axs[index],
                    scatter_kws = {'facecolors': df['colorcode5levels']}, color = color, ci = ci)
    for index, ax in enumerate(axs):
        ax.set_ylim(-1.3, 1.3)
        ax.set_xlim(-1.1, 1.1)
        if index == 4:
            ax.set(xlabel = x_label + x_label2, ylabel = "")
            ax.xaxis.label.set_size(20)
        else:
            ax.set(xlabel = "", ylabel = "")
    # y-label
    fig.text(0.06, 0.5, y_label, va = 'center', rotation = 'vertical', fontsize = 20)
    fig.text(0.08, 0.5, y_label2, va = 'center', rotation = 'vertical', fontsize = 20)
    plt.show()