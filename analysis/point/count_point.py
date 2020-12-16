from typing import List


def get_point_count_list(polar:list) -> list:
    # polar:                                 [(angle, distance),etc]
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    count_list = [[i, 0] for i in range(360)]
    for point in polar:
        # point: (angle, distance)
        angle = point[0]
        # angle_num: [angle, point_count_number]
        angle_num = count_list[angle]
        point_count_number = angle_num[1]
        angle_num[1] = point_count_number + 1
    return count_list

def __get_point_num_in_range(count_list:List[List[int]], curr_range:List[int]) -> int:
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    # curr_range: angle range [start: end)
    # point_num: how many disc in curr_range
    point_num = 0
    start, end = curr_range[0], curr_range[1]
    # range is 0, (0, 0), (1,1),etc.
    if start == end:
        point_num = count_list[start][1]
    # such as (2, 10)
    elif start < end:
        for angle_num in count_list[start:end]:
            point_num += angle_num[1]
    # start > end: (358, 2)
    else:
        for angle_num in count_list[start:]:
            point_num += angle_num[1]
        for angle_num in count_list[0:end]:
            point_num += angle_num[1]
    return point_num

def get_range_count(count_list:list, step:int) -> list:
    # count_list: disc num for given angle: [[angle, point_count_number], etc]
    # res_count: [[[angle, angle+step), num_points1], [[angle+1, angle+step+1), num_points1], etc]
    range_step = list()
    res_count = list()
    # build ranges
    for angle_num in count_list:
        angle = angle_num[0]
        next_degree = angle + step
        if next_degree <= 359:
            range_step.append([angle, next_degree])
        else:
            range_step.append([angle, next_degree-360])
    # give numbers for range
    for curr_range in range_step:
        point_number = __get_point_num_in_range(count_list, curr_range)
        res_count.append([curr_range, point_number])
    return res_count