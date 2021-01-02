"""
@author Miao Li
TODO: What does this code do?
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.transforms as mtransforms
from src.analysis.exp1_radial_displays_analysis import get_step_ranges_map, get_col_names, get_draw_ndisc_formate, \
    get_current_rangelist_to_draw, get_alignment_disc_num, get_alignment_value, get_algnment_rangelist
from src.commons.process_number import get_weighted_mean
from src.plots.exp1_radial_displays_plot import draw_ndisc_at_ray

if __name__ == '__main__':
    is_debug = True
    has_polar_plot = False
    has_plot = False
    has_indi_alinement_value = True
    write_to_excel = True

    # (1) Read stimuli display
    PATH = "../displays/"
    FILENAME = "update_stim_info_full.xlsx"
    simuli_df = pd.read_excel(PATH + FILENAME)

    # (2) Get step_ranges_map: key: step, value: range_list
    # max step = 12 deg (around 11.42 deg, defined by the size of crowding zones)
    step_range = (0, 13)
    all_positions_serise = simuli_df.positions_list
    # key(int):    angle step 
    # value(list): range_list [ [[angle, angle+step), num_points1], etc]*360, *250
    step_ranges_map = get_step_ranges_map(step_range, all_positions_serise)

    if has_indi_alinement_value:
        # (3) get the current range_list for each display - to draw
        curr_step = 12  # degree step: 0-12 (in theory 0-360)
        curr_countlist_index = 224  # 0-249 (250 displays)
        # [[[angle, angle+step), num_points1], [[angle+1, angle+step+1), num_points1], etc]
        curr_rangelist = get_current_rangelist_to_draw(step_ranges_map, curr_step, curr_countlist_index)

        # (4) calculate the alignment value for each display
        # n2: number of sectors that contain n number of discs
        curr_alignment_value, n_sectors = get_alignment_value(curr_rangelist, step = 1, weight = [0, 0, 0, 3, 4, 5],
                                                              is_counting = False)
        print(curr_alignment_value, n_sectors)

    # calculate alignment values (at given angle step:  6, 12 deg)
    included_step_range = [6, 12]
    sub_step_range_map = {k: v for k, v in step_ranges_map.items() if k in included_step_range}
    weight = [0, 0, 0, 3, 4, 5]

    alignment_value_dict = dict()
    # key: angle step
    # value: list of 250 alignment value
    n_sectors_dict = dict()
    # key: angle step
    # value: list of 250 lists of 6 sector numbers
    for step_range, all_range_list in sub_step_range_map.items():
        alignment_values = list()
        n_sectors_list = list()
        for range_list in all_range_list:
            alignment_value, n_sectors = get_alignment_value(range_list, step = 1, weight = weight, is_counting = True)
            alignment_values.append(alignment_value)
            n_sectors_list.append(n_sectors)
        alignment_value_dict.update({step_range: alignment_values})
        n_sectors_dict.update({step_range: n_sectors_list})

    # append alignment values to dataframe
    simuli_df["alignment_v_step_6"] = alignment_value_dict[6]
    simuli_df["alignment_v_step_12"] = alignment_value_dict[12]
    simuli_df["alignment_n_sectors_step_6"] = n_sectors_dict[6]
    simuli_df["alignment_n_sectors_step_12"] = n_sectors_dict[12]

    if write_to_excel:
        simuli_df.to_excel("exp1_stim_info.xlsx")

    if has_plot:
        # plot in Cartesian coordinates
        formate_rangelist = get_draw_ndisc_formate(curr_rangelist)
        draw_ndisc_at_ray(formate_rangelist)

    if has_polar_plot:
        xs = np.arange(360)
        ys = []
        for y in curr_rangelist:
            ys.append(y[1])
        ys = np.array(ys)

        fig = plt.figure(figsize = (5, 10))
        ax = plt.subplot(2, 1, 1)

        # If we want the same offset for each text instance,
        # we only need to make one transform.  To get the
        # transform argument to offset_copy, we need to make the axes
        # first; the subplot command above is one way to do this.
        trans_offset = mtransforms.offset_copy(ax.transData, fig = fig,
                                               x = 0.05, y = 0.10, units = 'inches')

        for x, y in zip(xs, ys):
            plt.plot(x, y, 'ro')
            # plt.text(x, y, '%d, %d' % (int(x), int(y)), transform = trans_offset)

        # offset_copy works for polar plots also.
        ax = plt.subplot(2, 1, 2, projection = 'polar')

        trans_offset = mtransforms.offset_copy(ax.transData, fig = fig,
                                               y = 6, units = 'dots')

        for x, y in zip(xs, ys):
            plt.polar(x, y, 'ro')
            # plt.text(x, y, '%d, %d' % (int(x), int(y)),
            #          transform = trans_offset,
            #          horizontalalignment = 'center',
            #          verticalalignment = 'bottom')

        plt.show()

    # Optional: only for debug
    if is_debug:
        c_names = get_col_names(simuli_df)
        # draw_temp(polar) # polar in sub_function cannot run here
