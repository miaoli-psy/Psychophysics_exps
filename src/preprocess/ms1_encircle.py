import os

import pandas as pd

if __name__ == '__main__':
    write_to_excel = False
    # read data
    PATH_DATA = "../../data/ms1_encircle/raw/"
    dir_list = os.listdir(PATH_DATA)
    df_list_all = [pd.read_excel(PATH_DATA + file) for file in dir_list]

    df_data = pd.concat(df_list_all, ignore_index = True)

    if write_to_excel:
        df_data.to_csv("preprocessed_encircle.csv")

