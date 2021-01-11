# -*- coding: utf-8 -*- 
"""
Project: Psychophysics_exps
Creator: Miao
Create time: 2020-12-29 20:02
IDE: PyCharm
Introduction:
"""
import pandas as pd
from scipy.stats import stats

from src.analysis.exp1_alignment_analysis import get_data_to_analysis
from src.commons.process_dataframe import change_col_value_type, keep_valid_columns, get_pivot_table, \
    get_sub_df_according2col_value
from src.constants.exp1_constants import KEPT_COL_NAMES_STIMU_DF, KEPT_COL_NAMES

if __name__ == '__main__':
    is_debug = True
    write_to_excel = False

    # read stimuli info and data
    PATH_STIMULI = "../displays/"
    PATH_DATA = "../data/exp1_rerun_data/"
    STIMULI_FILENAME = "exp1_stim_info.xlsx"
    DATA_FILENAME = "cleanedTotalData_fullinfo_v2.xlsx"

    stimuli_to_merge = pd.read_excel(PATH_STIMULI + STIMULI_FILENAME)
    data_to_merge = pd.read_excel(PATH_DATA + DATA_FILENAME)

    # unify col value type
    change_col_value_type(stimuli_to_merge, "crowdingcons", int)
    change_col_value_type(stimuli_to_merge, "winsize", float)
    change_col_value_type(stimuli_to_merge, "index_stimuliInfo", str)
    change_col_value_type(stimuli_to_merge, "N_disk", int)

    change_col_value_type(data_to_merge, "crowdingcons", int)
    change_col_value_type(data_to_merge, "winsize", float)
    change_col_value_type(data_to_merge, "index_stimuliInfo", str)
    change_col_value_type(data_to_merge, "N_disk", int)

    # remove duplicated cols
    stimuli_to_merge = keep_valid_columns(stimuli_to_merge, KEPT_COL_NAMES_STIMU_DF)

    # merge data with stimuli info
    all_df = pd.merge(data_to_merge,
                      stimuli_to_merge,
                      how = 'left',
                      on = ['index_stimuliInfo', 'N_disk', 'crowdingcons', 'winsize'])

    # %% preprocess
    my_data = keep_valid_columns(all_df, KEPT_COL_NAMES)

    # %% output
    alignment = ["alig_v_angle6_step1",
                 "alig_v_angle12_step1",
                 "alig_v_angle6_step6",
                 "alig_v_angle12_step12",
                 "alig_v_line_step1"]
    # index of alignment list
    n = 4
    # pivot table
    pt = get_pivot_table(my_data,
                         index = ["participant_N"],
                         columns = ["winsize", "crowdingcons", alignment[n]],
                         values = ["deviation_score"])
    # %% correlation
    my_data_c = get_sub_df_according2col_value(my_data, "crowdingcons", 1)
    # data for each winsize
    w03_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.3)
    w04_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.4)
    w05_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.5)
    w06_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.6)
    w07_c = get_sub_df_according2col_value(my_data_c, "winsize", 0.7)

    # w03_c = w03_c["deviation_score"].groupby(
    #         [w03_c["alig_v_angle12_step1"], w03_c["N_disk"], w03_c["list_index"]]).mean()
    # # convert index to column
    # w03_c = w03_c.reset_index(level = ["alig_v_angle12_step1", "list_index", "N_disk"])

    # which alignment value 0-4
    n = 1
    w03_c = get_data_to_analysis(w03_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w04_c = get_data_to_analysis(w04_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w05_c = get_data_to_analysis(w05_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w06_c = get_data_to_analysis(w06_c, "deviation_score", alignment[n], "N_disk", "list_index")
    w07_c = get_data_to_analysis(w07_c, "deviation_score", alignment[n], "N_disk", "list_index")

    r03, p03 = stats.pearsonr(w03_c["deviation_score"], w03_c[alignment[n]])
    r04, p04 = stats.pearsonr(w04_c["deviation_score"], w04_c[alignment[n]])
    r05, p05 = stats.pearsonr(w05_c["deviation_score"], w05_c[alignment[n]])
    r06, p06 = stats.pearsonr(w06_c["deviation_score"], w06_c[alignment[n]])
    r07, p07 = stats.pearsonr(w07_c["deviation_score"], w07_c[alignment[n]])

    print(f"correlation coefficient is {round(r03, 2)}, and p-value is {round(p03, 4)} for numerosity range 21-25")
    print(f"correlation coefficient is {round(r04, 2)}, and p-value is {round(p04, 4)} for numerosity range 31-35")
    print(f"correlation coefficient is {round(r05, 2)}, and p-value is {round(p05, 4)} for numerosity range 41-45")
    print(f"correlation coefficient is {round(r06, 2)}, and p-value is {round(p06, 4)} for numerosity range 49-53")
    print(f"correlation coefficient is {round(r07, 2)}, and p-value is {round(p07, 4)} for numerosity range 54-58")



# %% debug and write to excel
    if is_debug:
        col_names_stimuli = list(stimuli_to_merge.columns)
        col_names_data = list(data_to_merge)
        col_names_my_data = list(my_data)
    if write_to_excel:
        pt.to_excel("exp1_alig_%s.xlsx" % n)