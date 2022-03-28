import pandas as pd

from src.commons.process_dataframe import rename_df_col
import pingouin as pg

if __name__ == '__main__':
    PATH = "../../data/ms1_encircle/"
    DATA = "preprocessed_encircle.csv"
    data = pd.read_csv(PATH + DATA)

    data_1 = data.groupby(["evaluation", "winsize", "crowdingcons"])["groups_n"].agg(
            ["mean", "std"]).reset_index(level = ["evaluation", "winsize", "crowdingcons"])
    rename_df_col(df = data_1, old_col_name = "mean", new_col_name = "groups_n")


    # 2 way annova
    aov = pg.rm_anova(dv = "groups_n",
                      within = ["winsize", "crowdingcons"],
                      subject = "evaluation",
                      data = data_1)
    # post hoc
    posthocs = pg.pairwise_ttests(dv = "groups_n",
                                  within = ["winsize", "crowdingcons"],
                                  subject = "evaluation",
                                  data = data_1,
                                  padjust = "fdr_bh",
                                  effsize = "cohen")