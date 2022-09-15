import pandas as pd
import matplotlib.pyplot as plt

from src.commons.process_dataframe import process_col
from src.commons.process_str import str_to_list


def get_local_density_df(local_density_list):
    return pd.DataFrame(local_density_list, columns = ["eccentricity", "local_density"])


def covert_e_to_pix(e):
    return round(e * 0.04, 2)


def numerosity_to_ax(numerosity):
    if numerosity == 34:
        return 0
    elif numerosity == 36:
        return 1
    elif numerosity == 38:
        return 2
    elif numerosity == 40:
        return 3
    elif numerosity == 42:
        return 4
    elif numerosity == 44:
        return 5
    elif numerosity == 54:
        return 6
    elif numerosity == 56:
        return 7
    elif numerosity == 58:
        return 8
    elif numerosity == 60:
        return 9
    elif numerosity == 62:
        return 10
    elif numerosity == 64:
        return 11


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

    #%% TODO 改需要画的名字，title
    radial_name = radial_100
    tangential_name = tangential_100
    plot_title = "75"

    radial_dict = get_dict_of_df(radial_name)
    tangential_dict = get_dict_of_df(tangential_name)

    fig, aex = plt.subplots(2, 6, figsize = (50, 20), sharex = True, sharey = True)
    aex = aex.ravel()
    for key, df in radial_dict.items():
        df.plot(x = "eccentricity", y = "local_density", style = "r--", alpha = 0.5,
                ax = aex[numerosity_to_ax(key[0])],
                legend = None,
                title = "%s" % (key[0]))
    for key, df in tangential_dict.items():
        df.plot(x = "eccentricity", y = "local_density", style = "b--", alpha = 0.5,
                ax = aex[numerosity_to_ax(key[0])],
                legend = None)

    plt.suptitle("displays with %s percent pairs" % plot_title, fontsize = 20)
    plt.show()
