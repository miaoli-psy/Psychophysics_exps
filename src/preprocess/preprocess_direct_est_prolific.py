import copy
import os
import pandas as pd

from src.commons.process_dataframe import keep_valid_columns, change_col_value_type, insert_new_col_from_two_cols
from src.constants.constants_direct_est_prolific import KEEP_COLS


def get_deviation(resp: int, numerosity: int) -> int:
    return resp - numerosity


if __name__ == '__main__':
    # read data
    PATH_DATA = "../../data/prolific_direct_estimate/raw/"
    dir_list = os.listdir(PATH_DATA)
    df_list = [pd.read_csv(PATH_DATA + file) for file in dir_list]

    # preprocess
    df_list_prepro = list()
    for df in df_list:
        # keep useful clos
        df = keep_valid_columns(df = df, kept_columns_list = KEEP_COLS)

        # drop practice trials
        df = df.dropna(subset = ["trials.thisN"])

        # remove spaces
        if df["responseN"].dtypes == "object":
            df["responseN"] = df["responseN"].str.strip()
            # remove non numeric responses
            df["is_num"] = df["responseN"].str.isnumeric()
            drop_index = df[df["is_num"] == False].index
            df.drop(drop_index, inplace = True)

            # change responseN to float
            change_col_value_type(df, "responseN", float)

        df_list_prepro.append(df)

    # drop participants more than 5% of invalid trials
    # remove pp 12 data: only 311 valid trials out of 330 trials
    df_list_prepro.pop(2)

    # add deviation score col
    for df in df_list_prepro:
        insert_new_col_from_two_cols(df, "responseN", "numerosity", "deviation_score", get_deviation)

    # check subitizing results
    # take subitizing trials out
    subitizing_df_list = list()
    for df in df_list_prepro:
        sub_df = df.loc[df["numerosity"] <= 4]
        subitizing_df_list.append(sub_df)

    # 30 subitizing trials (only keep participant has 28, 29 and 30 correct)
    correct_trial_list = list()
    for sub_df in subitizing_df_list:
        correct_trial_list.append((sub_df["deviation_score"] == 0).sum())

    # removed index
    index_list = list()
    for i, n_correct in enumerate(correct_trial_list):
        if n_correct < 28:
            index_list.append(i)

    # removed participant performance not more than 90%
    df_list_prepro = [df for i, df in enumerate(df_list_prepro) if i not in index_list]



    # concat all participant
    df_data = pd.concat(df_list_prepro)
    df_data = df_data.drop(["is_num"], axis = 1)



