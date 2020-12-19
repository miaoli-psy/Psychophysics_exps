from scr.preprocess import preprocess_exp3a_pilot


data_path = "../data/rawdata_exp3a_pilot/"
filename_prefix = "P"
filetype = ".csv"
all_df = preprocess_exp3a_pilot.preprocess_exp3a_func(data_path, filetype, filename_prefix)