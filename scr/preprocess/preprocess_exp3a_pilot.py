from scr.preprocess.sub import merge_all_data
import pandas as pd
import copy


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


def drop_df_rows(df: pd.DataFrame, subset_cols: list) -> pd.DataFrame:
    """
    :param df:
    :param subset_cols: list of column names that dropna applied on
    :return:
    """
    df = df.dropna(subset = subset_cols)
    return df


if __name__ == "__main__":
    is_debug = False
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
    subset = ['key_resp.keys']
    d_all_df = drop_df_rows(all_df, subset)

    if is_debug:
        col_names = list(all_df.columns)