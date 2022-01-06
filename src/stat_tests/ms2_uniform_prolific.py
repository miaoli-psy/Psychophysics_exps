import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg


if __name__ == '__main__':
    PATH = "../../data/prolific_direct_estimate/"
    DATA = "prolifc_data_combine_num_each_pp.xlsx"
    DATA2 = "prolifc_data_each_pp.xlsx"
    winsize = 0.6

    # ANOVA within subject clustering (5) * type (2) for each winsize
    data = pd.read_excel(PATH + DATA)
    data = data[data["winsize"] == winsize]

    aov = pg.rm_anova(data = data,
                      dv = "mean_deviation_score",
                      within = ["percent_triplets", "protectzonetype"],
                      subject = "participant")

    posthocs = pg.pairwise_ttests(dv = "mean_deviation_score",
                                  within = ["percent_triplets", "protectzonetype"],
                                  subject = "participant",
                                  data = data,
                                  padjust = "fdr_bh",
                                  effsize = "cohen")

    # ANOVA within subject
    data2 = pd.read_excel(PATH + DATA2)
    data2 = data2[data2["winsize"] == 0.4] # winsize 0.4 unblanced data
    aov_table = AnovaRM(data = data2,
                        depvar = "mean_deviation_score",
                        subject = "participant",
                        within = ["protectzonetype", "numerosity", "percent_triplets"]).fit()
    aov_table.summary()








