import pandas as pd
import matplotlib.pyplot as plt

from src.commons.process_dataframe import process_col
from src.commons.process_str import str_to_list


def get_local_density_df(local_density_list):
    return pd.DataFrame(local_density_list, columns = ["eccentricity", "local_density"])


def covert_e_to_pix(e):
    return round(e * 0.04, 2)


def get_dict_of_df(df_loc_density):
    # put dataframe "local_density_list" into a list
    local_density_dict = dict()
    for index, row in df_loc_density.iterrows():
        local_density_list = str_to_list(row["local_density_list"])
        df = get_local_density_df(local_density_list)
        # convert eccentricity to unit to pix
        process_col(df, "eccentricity", covert_e_to_pix)
        # remove extreme local density
        df = df[(df["local_density"] < 1) & (df["local_density"] > 0)]
        local_density_dict.update({(row["numerosity"], row["display_i"]): df})
    return local_density_dict


if __name__ == '__main__':
    PATH = "../../displays/ms2_displays/"
    FILE = "ms2_displays_loc_density.xlsx"
    # read display file and drop unnamed column
    displays = pd.read_excel(PATH + FILE)
    displays = displays.drop(["Unnamed: 0", "index"], axis = 1)
    # make sure indexes pair with number of rows
    displays = displays.reset_index()

    # radial and tangential df
    displays_radial = displays[displays["protectzonetype"] == "radial"]
    displays_tangential = displays[displays["protectzonetype"] == "tangential"]

    # sep for diff condition (percent paris)
    radial_0 = displays_radial[displays_radial["perceptpairs"] == 0]
    radial_25 = displays_radial[displays_radial["perceptpairs"] == 0.25]
    radial_50 = displays_radial[displays_radial["perceptpairs"] == 0.5]
    radial_75 = displays_radial[displays_radial["perceptpairs"] == 0.75]
    radial_100 = displays_radial[displays_radial["perceptpairs"] == 1]

    tangential_0 = displays_tangential[displays_tangential["perceptpairs"] == 0]
    tangential_25 = displays_tangential[displays_tangential["perceptpairs"] == 0.25]
    tangential_50 = displays_tangential[displays_tangential["perceptpairs"] == 0.5]
    tangential_75 = displays_tangential[displays_tangential["perceptpairs"] == 0.75]
    tangential_100 = displays_tangential[displays_tangential["perceptpairs"] == 1]

    radial_0_dict = get_dict_of_df(radial_0)

    # fig, aex = plt.subplots(6, 2, sharex = True, sharey = True)
    # aex = aex.ravel()
    # for index, ax in enumerate(aex):
    #     for



    local_density_single = radial_0_dict[(34, 2)]
    local_density_single.plot(x = "eccentricity",
                              y = "local_density",
                              style = "r--",
                              alpha = 0.5)
    plt.show()