# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2021-04-19 16:24
IDE: PyCharm
Introduction: exp2 online, anova, and pariwise comparison
"""
import pandas as pd
from statsmodels.formula.api import ols
import statsmodels.api as sm

from src.stat_tests.sub.process_data import cal_ds_mean, cal_ds_std

if __name__ == '__main__':
    PATH = "../../data/exp2_data_online/"
    DATA = "exp2_online_preprocessed.xlsx"
    mydata = pd.read_excel(PATH + DATA)
    cal_mean_std = True
    save_data2test = True

    # get anova data: remove crowding == 2
    mydata2test = mydata.loc[mydata["crowding"] != 2]
    # pivot_t = pd.pivot_table(mydata2test, index = ["crowding", "participantID"], columns = [ "winsize", "clustering"], values = "deviation")
    #
    #
    #
    # mydata2test = mydata2test["deviation"].groupby(
    #         [mydata2test["crowding"], mydata2test["winsize"], mydata2test["clustering"], mydata2test["participantID"]]).mean()
    # mydata2test = mydata2test.reset_index(level = ["crowding", "winsize", "clustering", "participantID"])

    # if save_data2test:
    #     pivot_t.to_csv("exp2_data_r.csv")

    # mean values
    if cal_mean_std:
        crowdingcon = 0
        cal_ds_mean(mydata, crowdingcon = crowdingcon, col_name = "crowding")
        cal_ds_std(mydata, crowdingcon = crowdingcon, col_name = "crowding")

    # 3 ways anova
    model = ols(
            "deviation ~ C(crowding, Sum) + C(clustering, Sum) + C(winsize, Sum) + C(crowding, Sum)*C(clustering, "
            "Sum)*C(winsize, Sum)",
            data = mydata2test).fit()
    aov_table1 = sm.stats.anova_lm(model, typ = 3)

    # The interaction between crowding, clustering, and winsize is statistically non-significant. This indicates
    # that different level combinations of the factors do not produce a significant difference in the deviation.
    # Thus this term should be removed from the ANOVA model and re-ran looking at the 2-factor interactions.
    # https://www.pythonfordatascience.org/factorial-anova-python/#test_with_python

    model = ols(
            "deviation ~ C(crowding, Sum) + C(clustering, Sum) + C(winsize, Sum) + C(crowding, Sum):C(clustering, "
            "Sum) + C(crowding, Sum):C(winsize, Sum) + C(clustering, Sum):C(winsize, Sum)",
            data = data2plot).fit()

    aov_table2 = sm.stats.anova_lm(model, typ = 3)

    # esq_sm = aov_table['sum_sq'][0] / (aov_table['sum_sq'][0] + aov_table['sum_sq'][1])
    # aov_table['EtaSq'] = [esq_sm, 'NaN']
    # print(aov_table)
    # post hoc
