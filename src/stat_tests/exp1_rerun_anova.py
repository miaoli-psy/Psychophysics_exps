# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-03-03 15:21
IDE: PyCharm
Introduction: ms anova and pairwise comparison
"""
import pandas as pd
import pingouin as pg

from src.commons.process_dataframe import rename_df_col
from src.stat_tests.sub.process_data import cal_ds_mean, cal_ds_std

if __name__ == '__main__':
    PATH = "../../data/exp1_rerun_data/"
    DATA = "cleanedTotalData_fullinfo_v3.xlsx"
    data = pd.read_excel(PATH + DATA)
    pivot_t = False

    if pivot_t:
        pivot_t = pd.pivot_table(data, index = ["crowdingcons", "participant_N"], columns = ["winsize"],
                                 values = "deviation_score")
        pivot_t.to_csv("pt_exp1.csv")

    # mean crowding vs. no-crowding

    dv = "percent_change"
    # dv = "deviation_score"

    data_1 = data.groupby(["participant_N", "winsize", "crowdingcons"])[dv].agg(
            ["mean", "std"]).reset_index(level = ["participant_N", "winsize", "crowdingcons"])
    rename_df_col(df = data_1, old_col_name = "mean", new_col_name = dv)
    crowdingcon = 0
    cal_ds_mean(data, crowdingcon = crowdingcon)
    cal_ds_std(data, crowdingcon = crowdingcon)

    # 2 way annova
    aov = pg.rm_anova(dv = dv,
                      within = ["winsize", "crowdingcons"],
                      subject = "participant_N",
                      data = data_1)
    # post hoc
    posthocs = pg.pairwise_ttests(dv = dv,
                                  within = ["winsize", "crowdingcons"],
                                  subject = "participant_N",
                                  data = data_1,
                                  padjust = "fdr_bh",
                                  effsize = "cohen")
