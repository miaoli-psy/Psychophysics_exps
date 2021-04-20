# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-04-19 16:24
IDE: PyCharm
Introduction: exp2 online, anova, and pariwise comparison
"""
import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg

from src.stat_tests.sub.process_data import cal_ds_mean, cal_ds_std

if __name__ == '__main__':
    PATH = "../../data/exp2_data_online/"
    DATA = "exp2_online_preprocessed.xlsx"
    mydata = pd.read_excel(PATH + DATA)
    cal_mean_std = False
    pivot_t = False
    see_clustering_level = False
    include_baseline = False

    # convet data to anvoa formate
    if see_clustering_level:
        # remove crowding == 2 baseline condition
        mydata2test = mydata.loc[mydata["crowding"] != 2]
        mydata2test = mydata2test["deviation"].groupby(
                [mydata2test["crowding"], mydata2test["winsize"], mydata2test["clustering"],
                 mydata2test["participantID"]]).mean()
        mydata2test = mydata2test.reset_index(level = ["crowding", "winsize", "clustering", "participantID"])

    else:
        if include_baseline:
            mydata2test = mydata
        else:
            mydata2test = mydata.loc[mydata["crowding"] != 2]
        mydata2test = mydata2test["deviation"].groupby(
                [mydata2test["crowding"], mydata2test["winsize"],mydata2test["participantID"]]).mean()
        mydata2test = mydata2test.reset_index(level = ["crowding", "winsize","participantID"])

    if pivot_t:
        pivot_t = pd.pivot_table(mydata2test, index = ["crowding", "participantID"],
                                 columns = ["winsize", "clustering"], values = "deviation")
        pivot_t.to_csv("pt_exp2.csv")

    # mean values
    if cal_mean_std:
        crowdingcon = 0
        cal_ds_mean(mydata, crowdingcon = crowdingcon, col_name = "crowding")
        cal_ds_std(mydata, crowdingcon = crowdingcon, col_name = "crowding")

    # 3 ways anova
    if see_clustering_level:
        aov_table = AnovaRM(data = mydata2test, depvar = "deviation", subject = "participantID",
                            within = ["crowding", "winsize", "clustering"]).fit()
        aov_table.summary()
    else:
        aov = pg.rm_anova(dv = "deviation",
                          within = ["winsize", "crowding"],
                          subject = "participantID",
                          data = mydata2test)

        posthocs = pg.pairwise_ttests(dv = "deviation",
                                      within = ["winsize", "crowding"],
                                      subject = "participantID",
                                      data = mydata2test,
                                      padjust = "fdr_bh",
                                      effsize = "cohen")
