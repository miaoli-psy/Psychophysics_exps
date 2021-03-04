# -*- coding: utf-8 -*- 
"""
Project: CrowdingNumerosityGit
Creator: Miao
Create time: 2021-03-03 15:21
IDE: PyCharm
Introduction:
"""
import pandas as pd
import pingouin as pg

if __name__ == '__main__':
    PATH = "../../data/exp1_rerun_data/"
    DATA = "cleanedTotalData_fullinfo_v3.xlsx"
    mydata = pd.read_excel(PATH + DATA)

    # 2 way annova
    aov = pg.rm_anova(dv = "deviation_score",
                      within = ["winsize", "crowdingcons"],
                      subject = "participant_N",
                      data = mydata)
    # post hoc
    posthocs = pg.pairwise_ttests(dv = "deviation_score",
                                   within = ["winsize", "crowdingcons"],
                                   subject = "participant_N",
                                   data = mydata,
                                   padjust = "holm",
                                   effsize = "cohen")