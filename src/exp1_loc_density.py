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

from src.analysis.exp1_local_density_analysis import dict_pix_to_deg, get_result_dict, interplote_result_dict_start, \
    get_fitted_res
from src.commons.process_dataframe import process_col
from src.commons.process_dict import get_sub_dict
from src.commons.process_str import str_to_list

if __name__ == '__main__':
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

# #%% fit a line to the economic data
# from numpy import sin
# from numpy import sqrt
# from numpy import arange
# from pandas import read_csv
#
# from matplotlib import pyplot
#
#
# # define the true objective function
# def objective(x, a, b, c, d):
#     return a * sin(b - x) + c * x ** 2 + d
#
# # load the dataset
# url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/longley.csv'
# dataframe = read_csv(url, header = None)
# data = dataframe.values
# # choose the input and output variables
# x, y = data[:, 4], data[:, -1]
# # curve fit
# popt1, _ = curve_fit(objective, x, y)
# # summarize the parameter values
# a, b, c, d = popt1
# print(popt1)
# # plot input vs output
# pyplot.scatter(x, y)
# # define a sequence of inputs between the smallest and largest known inputs
# x_line = arange(min(x), max(x), 1)
# # calculate the output for the range
# y_line = objective(x_line, a, b, c, d)
# # create a line plot for the mapping function
# pyplot.plot(x_line, y_line, '--', color = 'red')
# pyplot.show()
#
# # %%
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm
# from scipy.optimize import curve_fit
# from scipy.special import gammaln # x! = Gamma(x+1)
#
# meanlife = 550e-6
# decay_lifetimes = 1/np.random.poisson((1/meanlife), size=100000)
#
# def transformation_and_jacobian(x):
#     return 1./x, 1./x**2.
#
# def tfm_normal_pdf(x, lam):
#     y, J = transformation_and_jacobian(x)
#     return norm.pdf(y, lam, np.sqrt(lam)) * J
#
# def tfm_poisson_pdf(x, mu):
#     y, J = transformation_and_jacobian(x)
#     # For numerical stability, compute exp(log(f(x)))
#     return np.exp(y * np.log(mu) - mu - gammaln(y + 1.)) * J
#
# hist, bins = np.histogram(decay_lifetimes, bins=50, density=True)
# width = 0.8*(bins[1]-bins[0])
# center = (bins[:-1]+bins[1:])/2
# plt.bar(center, hist, align='center', width=width, label = 'Normalised data')
#
# # Important: Choose a reasonable starting point
# p0 = 1 / np.mean(decay_lifetimes)
#
# norm_opt, _ = curve_fit(tfm_normal_pdf, center, hist, p0=p0)
# pois_opt, _ = curve_fit(tfm_poisson_pdf, center, hist, p0=p0)
#
# plt.plot(center, tfm_normal_pdf(center, *norm_opt), 'g--', label='(Transformed) Normal fit')
# plt.plot(center, tfm_poisson_pdf(center, *pois_opt), 'r--', label='(Transformed) Poisson fit')
# plt.legend(loc = 'best')
# plt.tight_layout()
# plt.show()