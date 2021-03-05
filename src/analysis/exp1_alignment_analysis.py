import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import statsmodels.formula.api as sm
from matplotlib.lines import Line2D

from src.commons.process_dataframe import get_sub_df_according2col_value


def add_color_code_by_crowdingcons(crowding_cons: str):
    if crowding_cons == 0:
        return "royalblue"
    elif crowding_cons == 1:
        return "orangered"
    else:
        raise Exception(f"crowding_cons == {crowding_cons} is not recognized. O for no-crowding, 1 for crowding")


def add_color_code_by_winsize(N_disk: str):
    if 21 <= N_disk <= 25:
        return "cornflowerblue"
    elif 31 <= N_disk <= 35:
        return "orange"
    elif 41 <= N_disk <= 45:
        return "limegreen"
    elif 49 <= N_disk <= 53:
        return "red"
    elif 54 <= N_disk <= 58:
        return "mediumpurple"
    else:
        raise Exception(f"N_disk == {N_disk} is not recognized. 24-25, 31-35, 41-45, 49-53, 54-58 are allowed")


def add_color_code_5levels(N_disk: str, crowdingcons: str):
    if N_disk == 21 or N_disk == 31 or N_disk == 41 or N_disk == 49 or N_disk == 54:
        if crowdingcons == 0:
            return "#ccccff"
        else:
            return "#ffd6cc"
    elif N_disk == 22 or N_disk == 32 or N_disk == 42 or N_disk == 50 or N_disk == 55:
        if crowdingcons == 0:
            return "#9999ff"
        else:
            return "#ffad99"
    elif N_disk == 23 or N_disk == 33 or N_disk == 43 or N_disk == 51 or N_disk == 56:
        if crowdingcons == 0:
            return "#6666ff"
        else:
            return "#ff8566"
    elif N_disk == 24 or N_disk == 34 or N_disk == 44 or N_disk == 52 or N_disk == 57:
        if crowdingcons == 0:
            return "#3333ff"
        else:
            return "#ff5c33"
    elif N_disk == 25 or N_disk == 35 or N_disk == 45 or N_disk == 53 or N_disk == 58:
        if crowdingcons == 0:
            return "#0000ff"
        else:
            return "#ff3300"
    else:
        raise Exception(f"N_disk == {N_disk} is not correct")

def get_analysis_dataframe(my_data, crowding):
    if crowding == 1:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 1)
    elif crowding == 0:
        return get_sub_df_according2col_value(my_data, "crowdingcons", 0)
    elif crowding == 2:
        return my_data
    else:
        raise Exception(f"crowding == {crowding} is not recognized. 0 for no-crowding, 1 for crowding, 2 for all")


def __get_groupby_df(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str,
                     col_name4: str, col_name5: str):
    return input_df[val_col].groupby(
            [input_df[col_name1], input_df[col_name2], input_df[col_name3], input_df[col_name4], input_df[col_name5]]).mean()


def __convert_index2column(input_df: pd.DataFrame, col_name1: str, col_name2: str, col_name3: str, col_name4: str, col_name5: str):
    return input_df.reset_index(level = [col_name1, col_name2, col_name3, col_name4, col_name5])


def get_data_to_analysis(input_df: pd.DataFrame, val_col: str, col_name1: str, col_name2: str, col_name3: str,
                         col_name4: str, col_name5: str):
    grouped = __get_groupby_df(input_df, val_col, col_name1, col_name2, col_name3, col_name4, col_name5)
    return __convert_index2column(grouped, col_name1, col_name2, col_name3, col_name4, col_name5)


def normalize_deviation(input_df: pd.DataFrame):
    """
    :param input_df:dataframe contains col "deviation_score"
    :return: new dataframe contains only normalized "deviation_score" range within(-1, 1)
    """
    min_max_scaler = MinMaxScaler(feature_range = (-1, 1))
    return pd.DataFrame(min_max_scaler.fit_transform(input_df[["deviation_score"]]), columns = ["deviation_score"])


def normalize_zerotoone(input_df: pd.DataFrame, to_normalize_col: str):
    """
    :param input_df: dataframe contains col alignment values
    :param to_normalize_col: alignment_col name
    :return: new dataframe contains only normalized alignment_col range within(0, 1)
    """
    min_max_scaler = MinMaxScaler(feature_range = (0, 1))
    return pd.DataFrame(min_max_scaler.fit_transform(input_df[[to_normalize_col]]), columns = [to_normalize_col])


def rename_norm_col(input_df: pd.DataFrame, old_name: str, new_name: str):
    return input_df.rename(columns = {old_name: new_name})


def calculate_residuals(w_df):
    lin_fit_results_Y = sm.ols(formula = "deviation_score_norm ~ N_disk", data = w_df).fit()
    w_df["rY"] = lin_fit_results_Y.resid

    lin_fit_results_X = sm.ols(formula = "align_v_size6_norm ~ N_disk", data = w_df).fit()
    w_df["rX"] = lin_fit_results_X.resid


def add_legend(colorc, corlornc, marker = "o", line_color = "w", markersize = 8):
    circle_legend = [
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = colorc[0], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = colorc[1], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = colorc[2], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = colorc[3], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = colorc[4], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = corlornc[0], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = corlornc[1], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = corlornc[2], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = corlornc[3], markersize = markersize),
        Line2D([0], [0], marker = marker, color = line_color, markerfacecolor = corlornc[4], markersize = markersize)
    ]
    return circle_legend

