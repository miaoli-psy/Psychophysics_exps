# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 22:27
IDE: PyCharm
Introduction:
"""
import pandas as pd


def get_pivot_table(input_df: pd.DataFrame) -> pd.DataFrame:
    pivot_table = pd.pivot_table(input_df,
                                 index = ["participant_N"],
                                 columns = ["winsize", "crowdingcons", "alignment_v_step_12"],
                                 values = ["deviation_score"])
    return pivot_table