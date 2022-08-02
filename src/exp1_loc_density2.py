import pandas as pd

from src.commons.process_dataframe import keep_valid_columns

if __name__ == '__main__':
    PATH = "../displays/"
    FILE = "update_stim_info_full.xlsx"
    stimuli_df = pd.read_excel(PATH + FILE)
    COL = ["displayN",
           "positions_list",
           "occupancyArea",
           "density_itemsperdeg2",
           "winsize",
           "crowdingcons",
           "list_index"]
    # keep useful cols
    stimuli_df = keep_valid_columns(stimuli_df, COL)

