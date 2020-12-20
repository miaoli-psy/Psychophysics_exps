import pandas as pd
from typing import List


# func_name: func_name is process each element in each column, instead of the whole column
def process_col(input_df: pd.DataFrame, col_name: str, func_name):
    if col_name in input_df.columns:
        input_df[col_name] = input_df[col_name].map(func_name)
    else:
        raise Exception(f"Warning: missing {col_name}")


# input_cols: col_name string in list
def process_cols(input_df: pd.DataFrame, input_cols: List[str], func_name):
    for col in input_cols:
        if col in input_df.columns:
            input_df[col] = input_df[col].map(func_name)
        else:
            raise Exception(f"Warning: Missing {col}")


# old_col: old_col name string already in input_df
# new_col: new_col name string which is to insert in input_df
def insert_new_col(input_df: pd.DataFrame, old_col: str, new_col: str, func_name):
    if old_col in input_df.columns:
        col_index = input_df.columns.get_loc(old_col)
        input_df.insert(col_index, new_col, input_df[old_col].map(func_name))
    else:
        raise Exception(f"Warning: missing {old_col}")


def insert_new_col_from_two_cols(input_df: pd.DataFrame, old_col1: str, old_col2: str, new_col: str, func_name):
    cols = input_df.columns
    if (old_col1 in cols) and (old_col2 in cols):
        input_df[new_col] = input_df.apply(lambda x: func_name(x[old_col1], x[old_col2]), axis = 1)
    else:
        raise Exception(f"Warning: missing {old_col1} or {old_col2}")
