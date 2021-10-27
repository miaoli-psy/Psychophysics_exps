import pandas as pd

from src.commons.process_dataframe import rename_df_col, insert_new_col, insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM


def get_percent_triplets(percentpairs):
    if percentpairs == 1:
        return 0
    elif percentpairs == 0.75:
        return 0.25
    elif percentpairs == 0.5:
        return 0.5
    elif percentpairs == 0.25:
        return 0.75
    elif percentpairs == 0:
        return 1
    else:
        raise Exception(f"percentpair {percentpairs} is unexpected")


def get_samplesize(winsize):
    if winsize == 0.4:
        return 34
    else:
        return 32


if __name__ == '__main__':
    write_to_excel = False
    # read data
    PATH = "../data/prolific_direct_estimate/"
    DATA = "preprocessed_prolific.xlsx"
    data = pd.read_excel(PATH + DATA)
    # process the cols
    rename_df_col(data, "Unnamed: 0", "n")
    # convert percentpairs to percent_triplets
    insert_new_col(data, "perceptpairs", "percent_triplets", get_percent_triplets)

    # averaged data: averaged deviation for each condition per participant
    data_1 = data.groupby(["percent_triplets", "numerosity", "protectzonetype", "participant", "winsize"])[
        "deviation_score"] \
        .agg(['mean', 'std']) \
        .reset_index(level = ["percent_triplets", "numerosity", "protectzonetype", "participant", "winsize"])

    rename_df_col(df = data_1, old_col_name = "mean", new_col_name = "mean_deviation_score")
    data_1["samplesize"] = [5] * data_1.shape[0]  # each participant repeat each condition 5 times (5 displays)
    insert_new_col_from_two_cols(data_1, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: averaged across participant
    data_2 = data.groupby(["percent_triplets", "numerosity", "protectzonetype", "winsize"])["deviation_score"] \
        .agg(["mean", "std"]).reset_index(level = ["percent_triplets", "numerosity", "protectzonetype", "winsize"])

    rename_df_col(df = data_2, old_col_name = "mean", new_col_name = "mean_deviation_score")
    insert_new_col(data_2, "winsize", "samplesize",
                   get_samplesize)  # 66 participants, 34 for winsize0.4, 32 for winsize0.6
    insert_new_col_from_two_cols(data_2, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: averaged deviation for different winsize per participant
    data_3 = data.groupby(["percent_triplets", "protectzonetype", "participant", "winsize"])["deviation_score"] \
        .agg(['mean', 'std']).reset_index(level = ["percent_triplets", "protectzonetype", "participant", "winsize"])
    rename_df_col(df = data_3, old_col_name = "mean", new_col_name = "mean_deviation_score")
    data_3["samplesize"] = [30] * data_3.shape[0]  # each participant repeat 6 numerosity * 5 displays = 30 times
    insert_new_col_from_two_cols(data_3, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    # averaged data: averaged deviation for different winsize, across participant
    data_4 = data.groupby(["percent_triplets", "protectzonetype", "winsize"])["deviation_score"] \
        .agg(['mean', 'std']).reset_index(level = ["percent_triplets", "protectzonetype", "winsize"])
    rename_df_col(df = data_4, old_col_name = "mean", new_col_name = "mean_deviation_score")
    insert_new_col(data_4, "winsize", "samplesize",
                   get_samplesize)  # 66 participants, 34 for winsize0.4, 32 for winsize0.6
    insert_new_col_from_two_cols(data_4, "mean_deviation_score", "samplesize", "SEM", cal_SEM)

    if write_to_excel:
        data_2.to_excel("prolifc_data.xlsx", index = False)