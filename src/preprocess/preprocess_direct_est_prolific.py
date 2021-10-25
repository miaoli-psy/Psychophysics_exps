import os
import pandas as pd

from src.commons.process_dataframe import keep_valid_columns, change_col_value_type
from src.constants.constants_direct_est_prolific import KEEP_COLS

if __name__ == '__main__':
    # read data
    PATH_DATA = "../../data/prolific_direct_estimate/raw/"
    dir_list = os.listdir(PATH_DATA)
    df_list = [pd.read_csv(PATH_DATA + file) for file in dir_list]
    subitizing = [2, 3, 4]

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

    df_data = pd.concat(df_list_prepro)


