from scr.preprocess.sub import merge_all_data
import pandas as pd
import copy
import math


def preprocess_exp3a_func(data_path: str, filetype: str, filename_prefix: str) -> pd.DataFrame:
    all_df = merge_all_data.merge_all_file2dataframe(data_path, filetype, filename_prefix)
    return all_df


def keep_valid_columns(df: pd.DataFrame, kept_columns_list: list) -> pd.DataFrame:
    all_col_name_list = list(df.columns)
    all_col_name_copy_list = copy.deepcopy(all_col_name_list)
    drop_name_list = list()
    for name in all_col_name_copy_list:
        if name not in kept_columns_list:
            drop_name_list.append(name)
    df = df.drop(drop_name_list, axis = 1)
    return df


def drop_df_nan_rows_according2cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    :param df:
    :param cols: list of column names that dropna applied on
    :return:
    """
    df = df.dropna(subset = cols)
    return df


def drop_df_rows_according2_one_col(df: pd.DataFrame, col_name: str, lowerbondary: float,
                                    upperbondary: float) -> pd.DataFrame:
    """
    :param df:
    :param col:  column name(str)
    :param lowerbondary:
    :param upperbondary:
    :return:
    """
    df = df[(df[col_name] < upperbondary) & (df[col_name] > lowerbondary)]
    return df


def __cal_std_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    std = df[col_name].std()
    return std


def __cal_mean_of_one_col(df: pd.DataFrame, col_name: str) -> float:
    mean = df[col_name].mean()
    return mean


def get_col_boundary(df: pd.DataFrame, col_name: str, n_std = 2) -> tuple:
    mean = __cal_mean_of_one_col(df, col_name)
    std = __cal_std_of_one_col(df, col_name)
    return mean - n_std * std, mean + n_std * std


if __name__ == "__main__":
    is_debug = False
    write_to_excel = False
    data_path = "../../data/rawdata_exp3a_pilot/"
    filename_prefix = "P"
    filetype = ".csv"
    kept_col_names = ["D1",
                      "D1Crowding",
                      "D1Ndisplay",
                      "D1aggregateSurface",
                      "D1averageE",
                      "D1avg_spacing_c",
                      "D1convexHull_perimeter",
                      "D1density",
                      "D1density_itemsperdeg2",
                      "D1mirror",
                      "D1numerosity",
                      "D1occupancyArea",
                      "D1ref",
                      "D1rotate",
                      "D2",
                      "D2Crowding",
                      "D2Ndisplay",
                      "D2aggregateSurface",
                      "D2averageE",
                      "D2avg_spacing_c",
                      "D2convexHull_perimeter",
                      "D2density",
                      "D2density_itemsperdeg2",
                      "D2mirror",
                      "D2numerosity",
                      "D2occupancyArea",
                      "D2ref",
                      "D2rotate",
                      "group",
                      "key_resp.keys",
                      "key_resp.rt",
                      "participantN",
                      "probe_c",
                      "ref_c",
                      "ref_first"]
    all_df = preprocess_exp3a_func(data_path, filetype, filename_prefix)
    all_df = keep_valid_columns(all_df, kept_col_names)

    # drop practice trials: drop all rows with NaNs in key_resp.keys
    col_to_dropna = ['key_resp.keys']
    all_df = drop_df_nan_rows_according2cols(all_df, col_to_dropna)

    # drop too fast and too slow response
    col_to_drop_rows = "key_resp.rt"
    min_rt = 0.15
    max_rt = 3
    all_df = drop_df_rows_according2_one_col(all_df, col_to_drop_rows, min_rt, max_rt)

    # drop response that are outside 2 standard deviation
    col_rt = "key_resp.rt"
    boundary = get_col_boundary(all_df, col_rt)
    resp_min = boundary[0]
    resp_max = boundary[1]
    all_df = drop_df_rows_according2_one_col(all_df, col_rt, resp_min, resp_max)

    if is_debug:
        col_names = list(all_df.columns)
    if write_to_excel:
        all_df.to_excel("preprocess_exp3a_pilot.xlsx")