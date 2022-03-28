import pandas as pd
import pingouin as pg

if __name__ == '__main__':
    PATH = "../../data/ms1_encircle/"
    DATA = "ms1_encircle_corr.xlsx"
    data = pd.read_excel(PATH + DATA)

    # par correlation
    x = "deviation_score_mean"
    y = "groups_mean"
    covar = "numerosity"
    method = "pearson"

    # TODO
    # alignmentcon = "radial"
    alignmentcon = "tangential"
    winsize = 0.7

    data_to_analysis = data[(data["winsize"] == winsize) & (data["crowdingcons"] == alignmentcon)]
    # data_to_analysis = data[(data["crowdingcons"] == alignmentcon)]

    partial_corr = pg.partial_corr(data_to_analysis,
                                   x = x,
                                   y = y,
                                   covar = covar,
                                   method = method)

