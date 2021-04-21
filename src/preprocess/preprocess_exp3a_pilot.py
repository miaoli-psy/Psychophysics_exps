# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-20 21:07
IDE: PyCharm
Introduction: preprocessed data of crowding and numerosity exp3a (online pilot)
"""
from src.analysis.exp3a_pilot_analysis import insert_is_resp_ref_more, insert_probeN, insert_refN, insert_probeCrowding, \
    insert_refCrowing, insert_exp_condition
from src.preprocess.sub import merge_all_data
import pandas as pd

from src.constants.exp3a_pilot_constants import KEPT_COL_NAMES
from src.preprocess.sub.get_data2analysis import drop_df_nan_rows_according2cols, drop_df_rows_according2_one_col, \
    get_col_boundary
from src.commons.process_dataframe import keep_valid_columns, insert_new_col_from_two_cols, \
    insert_new_col_from_three_cols


def preprocess_exp3a_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


if __name__ == '__main__':
    DATA_PATH = "../../data/exp3_data/exp3_pilot_data/rawdata/"
    FILENAME_PREFIX = "P"
    FILETYPE = ".csv"
    drop_fastandslow_resp = False
    save_preprocessed = False

    # load raw data
    mydata = preprocess_exp3a_func(DATA_PATH, FILETYPE, FILENAME_PREFIX)

    # preprocess starts here
    mydata = keep_valid_columns(mydata, KEPT_COL_NAMES)

    # drop practice trials: drop all rows with NaNs in key_resp.keys
    col_to_dropna = ['key_resp.keys']
    mydata = drop_df_nan_rows_according2cols(mydata, col_to_dropna)

    # drop too fast and too slow response
    if drop_fastandslow_resp:
        col_to_drop_rows = "key_resp.rt"
        min_rt = 0.15
        max_rt = 3
        mydata = drop_df_rows_according2_one_col(mydata, col_to_drop_rows, min_rt, max_rt)

    # add numerosity difference between D1 and D2
    mydata["dff_D1D2"] = mydata["D1numerosity"] - mydata["D2numerosity"]
    # add correct answer
    insert_new_col_from_two_cols(mydata, "ref_first", "key_resp.keys", "is_resp_ref_more", insert_is_resp_ref_more)
    # add probe numerosity
    insert_new_col_from_three_cols(mydata, "D1numerosity", "D2numerosity", "ref_first", "probeN", insert_probeN)
    # add ref numerosity
    insert_new_col_from_three_cols(mydata, "D1numerosity", "D2numerosity", "ref_first", "refN", insert_refN)
    # add probe crowding condition
    insert_new_col_from_three_cols(mydata, "D1Crowding", "D2Crowding", "ref_first", "probeCrowding",
                                   insert_probeCrowding)
    # add ref crowding condition
    insert_new_col_from_three_cols(mydata, "D1Crowding", "D2Crowding", "ref_first", "refCrowding", insert_refCrowing)

    # %% experiment conditions
    # indicate different condition with extra columns
    insert_new_col_from_two_cols(mydata, "ref_c", "probe_c", "ref_probe_condi", insert_exp_condition)

    if save_preprocessed:
        mydata.to_excel("exp3a_preprocessed.xlsx")
