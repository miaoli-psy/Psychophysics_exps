import pandas as pd

from src import exp1_radial_display2
from src.commons.process_dataframe import keep_valid_columns, rename_df_col, process_col
from src.constants.exp1_constants import KEEP_COL_Coor


def con_crowidngcons(crowdingcons):
    if crowdingcons == 1:
        return "radial"
    elif crowdingcons == 0:
        return "tangential"


if __name__ == '__main__':
    to_excel = False

    PATH_DATA = "../data/exp1_rerun_data/"
    FILENAME_DATA = "cleanedTotalData_fullinfo_v3.xlsx"

    ENCIRCLE_DATA = "../data/ms1_encircle/preprocessed_encircle.csv"

    stimuli_to_merge = exp1_radial_display2.stimuli_df
    data_to_merge = pd.read_excel(PATH_DATA + FILENAME_DATA)

    # merge stimuli file with estimation data
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = "left",
                      on = ["index_stimuliInfo", "N_disk", "crowdingcons", "winsize"])

    # keep valid columns estimation data
    all_df = keep_valid_columns(all_df, KEEP_COL_Coor)

    # encircle data
    encircle_df = pd.read_csv(ENCIRCLE_DATA)

    # group by the estimation data by each display
    data = all_df.groupby(["displayN", "crowdingcons", "list_index", "N_disk", "winsize"])["response"] \
        .agg(["mean", "std"]).reset_index(level = ["displayN", "crowdingcons", "list_index", "N_disk", "winsize"])

    rename_df_col(df = data, old_col_name = "mean", new_col_name = "response_mean")
    rename_df_col(df = data, old_col_name = "std", new_col_name = "response_std")

    # group by the encircle data - average participant
    data_encircle = encircle_df.groupby(["displayN", "crowdingcons", "list_index", "numerosity", "winsize"])["groups_n"] \
        .agg(["mean", "std"]).reset_index(level = ["displayN", "crowdingcons", "list_index", "numerosity", "winsize"])

    # rename N_disk to numerosity
    data = data.rename(columns = {"N_disk": "numerosity"})

    process_col(data, "crowdingcons", con_crowidngcons)
    # merge estimation
    all_df = pd.merge(data,
                      data_encircle,
                      how = "left",
                      on = ["numerosity", "displayN", "crowdingcons", "winsize", "list_index"])

    if to_excel:
        all_df.to_excel("try.xlsx")

