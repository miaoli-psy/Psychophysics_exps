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

from src.commons.process_dataframe import process_col
from src.commons.process_str import str_to_list

if __name__ == '__main__':
    PATH = "../displays/"
    FILE = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILE)

    # positions
    process_col(stimuli_df, "positions", str_to_list)

    stimuli_df_c = stimuli_df[(stimuli_df['crowdingcons'] == 1)]
    stimuli_df_nc = stimuli_df[(stimuli_df['crowdingcons'] == 0)]

    crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_c.groupby('N_disk')}
    no_crowding_dic = {k: g['positions'].tolist() for k, g in stimuli_df_nc.groupby('N_disk')}

    # crowding and no-crowding dictionary, in deg
    crowding_dic = dict_pix_to_deg(crowding_dic, 1)
    no_crowding_dic = dict_pix_to_deg(no_crowding_dic, 1)