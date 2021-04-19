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

from src.stat_tests.sub.process_data import cal_ds_mean, cal_ds_std

if __name__ == '__main__':
    PATH = "../../data/exp1_rerun_data/"
    DATA = "cleanedTotalData_fullinfo_v2.xlsx"
    mydata = pd.read_excel(PATH + DATA)

    # mean crowding vs. no-crowding
    crowdingcon = 0
    cal_ds_mean(mydata, crowdingcon = crowdingcon)
    cal_ds_std(mydata, crowdingcon = crowdingcon)

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
                                  padjust = "fdr_bh",
                                  effsize = "cohen")