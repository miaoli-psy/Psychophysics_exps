# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-01-05 19:14
IDE: PyCharm
Introduction:
"""

from scipy.stats import poisson
import pandas as pd
import numpy as np

from src.analysis.exp1_local_density_analysis import dict_pix_to_deg, get_result_dict, interplote_result_dict_start, \
    normolizedLD
from src.commons.fitfuncs import get_lambda
from src.commons.process_dataframe import process_col
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

    res_list = list()
    for numerosity, loc_density_list in result_dict_c.items():
        for loc_density in loc_density_list:
            x_value = list()
            y_value = list()
            for loc_tuple in loc_density:
                x_value.append(loc_tuple[0])
                y_value.append(loc_tuple[1])
            np_array = np.array([x_value, normolizedLD(y_value)]).transpose()
            res_list.append(get_lambda(np_array))

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