import pandas as pd

from src.commons.process_dataframe import insert_new_col_from_two_cols
from src.commons.process_number import cal_SEM

if __name__ == '__main__':
    to_excel = False
    # read data
    PATH = "../data/ms1_encircle/"
    DATA = "ms1_encircle_data.xlsx"

    data = pd.read_excel(PATH + DATA)

    dv = "average_group"

    indv = "numerosity"
    indv2 = "crowdingcons"
    indv3 = "winsize"

    data_1 = data.groupby([indv, indv2, indv3])[dv]\
        .agg(['mean', 'std']) \
        .reset_index(level = [indv, indv2, indv3])

    data_1["samplesize"] = [5 * 3] * data_1.shape[0] #5 displays, 3 pp
    insert_new_col_from_two_cols(data_1, "mean", "samplesize", "SEM", cal_SEM)

    if to_excel:
        data_1.to_excel("ms1_encircle_by_num.xlsx")