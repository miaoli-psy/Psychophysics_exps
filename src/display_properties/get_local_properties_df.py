import pandas as pd

from src.analysis.ms2_local_density_analysis import get_local_density_for_single_display
from src.commons.process_dataframe import insert_new_col
from src.commons.process_str import str_to_list

if __name__ == '__main__':
    PATH = "../../displays/ms2_displays/"
    # FILE = "ms2_displays.xlsx"
    FILE = "ms2_displays_triplets.xlsx"
    # read display file
    all_displays = pd.read_excel(PATH + FILE)
    # process str (to list)
    insert_new_col(all_displays, "allposis", "allposis_list_of_tuple", str_to_list)
    # add local density list column
    insert_new_col(all_displays, "allposis_list_of_tuple", "local_density_list", get_local_density_for_single_display)

    all_displays.to_excel("try.xlsx")

