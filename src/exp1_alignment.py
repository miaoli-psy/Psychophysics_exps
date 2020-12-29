# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 20:02
IDE: PyCharm
Introduction:
"""
import pandas as pd

from src.commons.process_dataframe import change_col_value_type

if __name__ == '__main__':
    is_debug = True

    # read stimuli info and data
    PATH_STIMULI = "../displays/"
    PATH_DATA = "../data/"
    STIMULI_FILENAME = "exp1_stim_info.xlsx"
    DATA_FILENAME = "cleanedTotalData_fullinfo_v2.xlsx"

    stimuli_to_merge = pd.read_excel(PATH_STIMULI + STIMULI_FILENAME)
    data_to_merge = pd.read_excel(PATH_DATA + DATA_FILENAME)

    # unify col value type
    change_col_value_type(stimuli_to_merge, "crowdingcons", int)
    change_col_value_type(stimuli_to_merge, "winsize", float)
    change_col_value_type(stimuli_to_merge, "index_stimuliInfo", str)
    change_col_value_type(stimuli_to_merge, "N_disk", int)

    change_col_value_type(data_to_merge, "crowdingcons", int)
    change_col_value_type(data_to_merge, "winsize", float)
    change_col_value_type(data_to_merge, "index_stimuliInfo", str)
    change_col_value_type(data_to_merge, "N_disk", int)

    # merge data with stimuli info
    my_data = pd.merge(data_to_merge,
                       stimuli_to_merge,
                       how = 'left',
                       on = ['index_stimuliInfo', 'N_disk', 'crowdingcons', 'winsize'])

    # %% preprocess starts here





    if is_debug:
        col_names_stimuli = list(stimuli_to_merge.columns)
        col_names_data = list(data_to_merge)
        col_names_my_data = list(my_data)
