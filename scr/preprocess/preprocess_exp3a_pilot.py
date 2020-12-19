from scr.preprocess.sub import merge_all_data
import pandas as pd


def preprocess_exp3a_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


if __name__ == "__main__":
    data_path = "../../data/rawdata_exp3a_pilot/"
    filename_prefix = "P"
    filetype = ".csv"
    all_df = preprocess_exp3a_func(data_path, filetype, filename_prefix)