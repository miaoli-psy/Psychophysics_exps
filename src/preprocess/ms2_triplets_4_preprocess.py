import os
import pandas as pd

if __name__ == '__main__':
    to_excel = False

    PATH = "../../data/ms2_triplets4/rawdata/"
    # list raw data files
    files = os.listdir(PATH)

    # collect all raw fiels
    data_csv = [file for file in files if file.endswith('csv')]

    # read data files
    totalData = pd.DataFrame()
    for file_name in data_csv:
        data = pd.read_csv(PATH + file_name)
        totalData = totalData.append(data)
    if to_excel:
        totalData.to_excel('try.xlsx')

