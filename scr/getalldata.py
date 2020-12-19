"""
read raw data in xlsx and csv
"""
import os
import pandas as pd


if __name__ == '__main__':
    is_debug = True

    # data path
    data_path = "../data/rawdata_exp3a_pilot"
    # list data files
    files = os.listdir(data_path)
    # read data
    data = [file for file in files if file.startswith("P") & file.endswith(".csv")]