# -*- coding: utf-8 -*-
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-20 21:07
IDE: PyCharm
Introduction: functions for preprocessed data of crowding and numerosity exp3a (online pilot)
"""
from src.preprocess.sub import merge_all_data
import pandas as pd


def preprocess_exp3a_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


