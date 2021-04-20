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

from src.stat_tests.sub.process_data import cal_ds_mean, cal_ds_std

if __name__ == '__main__':
    PATH = "../../data/exp2_data_online/"
    DATA = "exp2_online_preprocessed.xlsx"
    mydata = pd.read_excel(PATH + DATA)
    cal_mean_std = False
    pivot_t = False

    # get anova data: remove crowding == 2
    mydata2test = mydata.loc[mydata["crowding"] != 2]

    if pivot_t:
        pivot_t = pd.pivot_table(mydata2test, index = ["crowding", "participantID"],
                                 columns = ["winsize", "clustering"], values = "deviation")
        pivot_t.to_csv("pt_exp2.csv")

    # convet data to anvoa formate
    mydata2test = mydata2test["deviation"].groupby(
            [mydata2test["crowding"], mydata2test["winsize"], mydata2test["clustering"],
             mydata2test["participantID"]]).mean()
    mydata2test = mydata2test.reset_index(level = ["crowding", "winsize", "clustering", "participantID"])

    # mean values
    if cal_mean_std:
        crowdingcon = 0
        cal_ds_mean(mydata, crowdingcon = crowdingcon, col_name = "crowding")
        cal_ds_std(mydata, crowdingcon = crowdingcon, col_name = "crowding")

    # 3 ways anova
    aov_table = AnovaRM(data = mydata2test, depvar = "deviation", subject = "participantID",
                        within = ["crowding", "winsize", "clustering"]).fit()
    aov_table.summary()
