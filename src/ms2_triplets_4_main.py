import pandas as pd


if __name__ == '__main__':
    debug = True
    save_fig = False

    # read data
    PATH = "../data/ms2_triplets4/"
    DATA = "exp2_online_preprocessed.xlsx"
    data = pd.read_excel(PATH + DATA)