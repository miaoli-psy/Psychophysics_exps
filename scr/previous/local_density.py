# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:49:39 2019

@author: MiaoLi
"""
# =============================================================================
# IMPORTANT! This code converts pix to degree of visual angle directly
# e.g. in the algorithm, we removed a foveal region of r = 100 (pix),
# therefore, in visual angle degree, r = 3.839 deg
# =============================================================================

#%% =============================================================================
import os
import pandas as pd
import ast
# import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import operator
# import seaborn as sns'
# from collections import OrderedDict
# from shapely.geometry import Polygon, Point
# sys.path.append('C:\\Users\\MiaoLi\\Desktop\\SCALab\\Programming\\crowdingnumerositygit\\GenerationAlgorithm\\VirtualEllipseFunc')
# import m_defineEllipses
# import seaborn as sns

#%% =============================================================================
# display properties
# =============================================================================
def cal_eccentricity(posi) ->int:
    '''This function returns the distance between the input position and (0,0)'''
    eccenticity = math.sqrt(posi[0]**2+posi[1]**2)
    return eccenticity

def max_eccentricities(dis_list):
    '''returns the max_x_axis and the corrosponding posi'''
    e = []
    for posi in dis_list:
        e_temp = cal_eccentricity(posi)
        e.append(e_temp)
    # this only give the index of one posi, it my have more posis that are all max...doens't matter in this case.
    max_posi = dis_list[e.index(max(e))]
    max_x_axis = int(max(e))
    # min_posi = dis_list[e.index(min(e))]
    return max_x_axis, max_posi

def get_point_number(x_axis:int, list_point:list):
    '''for each x-axis, calculate the number of discs'''
    number = 0
    points = []
    for point in list_point:
        if cal_eccentricity((x_axis,0)) >= cal_eccentricity(point):
            number += 1
            points.append(point)
    return number,points

def get_x_y(list_point:list)-> list:
    ''''''
    x_max = abs(max_eccentricities(list_point)[0])
    list_result, y = [], 0
    for x in range(int(x_max)+2):
        new_y,points = get_point_number(x, list_point)
        if new_y != y:
            y = new_y
            list_result.append((x,y))
            # For degug: see the x,y point details
            # print("x,y: " ,x, ",",y, "points: ", points)
    return list_result

#FIXME the below 3 functions
def get_point_number_step(x_range:int, x_y:list)->int:
    for index, point in enumerate(x_y):
        if point[0] > x_range:
            return x_y[index-1][1]

def get_x_y_step(x_y_result:list,x_step:int)->list:
    x_init,x_max = x_y_result[0][0],x_y_result[-1][0]
    result_step = []
    for x in range(x_init,x_max+1,x_step):
        num_step = get_point_number_step(x,x_y_result)
        result_step.append((x,num_step))
    return result_step

def get_x_y_density(result_step:list)->list:
    curr_point_number = 0
    result_density = []
    for point in result_step:
        result_density.append((point[0],point[1]-curr_point_number))
        curr_point_number = point[1]
    return result_density

#%% =============================================================================
# import stimuli info
# =============================================================================
path = os.path.abspath(os.path.dirname(os.getcwd()))

#stimuliInfo_toMerge = pd.read_excel('../fullStimuliInfo.xlsx')
stimuliInfo_toMerge = pd.read_excel('fullStimuliInfo.xlsx')
#Mian
# stimuliInfo_toMerge = pd.read_excel('fullStimuliInfo.xlsx')
stimuliInfo_toMerge=stimuliInfo_toMerge.reset_index(drop = True)

# positions of each display
posi_lists_temp = stimuliInfo_toMerge['positions'].tolist()
posi_list=[]
for i in posi_lists_temp:
    i = ast.literal_eval(i)# megic! remore ' ' of the str
    posi_list.append(i)
#add positions as a list (not str) as a new coloum
    
stimuliInfo_toMerge['positions_list'] = posi_list
# crowding vs. nocrowding displays
df_c     = stimuliInfo_toMerge[(stimuliInfo_toMerge['crowdingcons'] == 1)]
df_nc    = stimuliInfo_toMerge[(stimuliInfo_toMerge['crowdingcons'] == 0)]
# convert pix to visual deg
k = 3.839/100

#%% =============================================================================
# separte dict
# =============================================================================
# per numerosity
crowding_dic    = {k: g['positions_list'].tolist() for k,g in df_c.groupby('N_disk')}
no_crowding_dic = {k: g['positions_list'].tolist() for k,g in df_nc.groupby('N_disk')}

def pix_to_deg_tuple(input_tuple, changeN):
    if changeN == 1:
        return (round(input_tuple[0] * k, 4), input_tuple[1])
    else:
        return (round(input_tuple[0] * k, 4), round(input_tuple[1] * k,4))
def dict_pix_to_deg(input_dict, changeN):
    '''Convert pix to deg for a given dictionary format,
    changeN is 1 or 2, to let the fucntion works for the first
    or both elements of the tuple'''
    dict_deg = {}
    for key, values in input_dict.items():
        new_display = []
        for display in values:
            new_posi = []
            for posi in display:
                new_posi.append(pix_to_deg_tuple(posi, changeN))
            new_display.append(new_posi)
        dict_deg.update({key:new_display})
    return dict_deg
crowding_dic_deg    = dict_pix_to_deg(crowding_dic, 2)
no_crowding_dic_deg = dict_pix_to_deg(no_crowding_dic, 2)

# averaged numerosity
def get_avrg_dict(inpudict):
    '''This function returns the accumulation display that contain the same numerosity
    eg. 5 displays with numerosity 21 --> 1 display contains 105 discs'''
    avrg_dic = {}
    for numerosity, lists in inpudict.items():
        avrg_nmrsty = []
        for plist in lists:
            for posi in plist:
                avrg_nmrsty.append(posi)
        avrg_dic.update({numerosity: avrg_nmrsty})
    return avrg_dic

avrg_c_dic      = get_avrg_dict(crowding_dic)
avrg_nc_dic     = get_avrg_dict(no_crowding_dic)

avrg_c_dic_deg  = get_avrg_dict(crowding_dic_deg)
avrg_nc_dic_deg = get_avrg_dict(no_crowding_dic_deg)

#%% =============================================================================
# get results: N discs against eccentricity
# =============================================================================
def get_result_dict(posis_dict):
    '''calculates the local density'''
    result_dict = {}
    for key, posis in posis_dict.items():
        result_list_t = []
        for posi in posis:
            result_t = get_x_y(posi)
            result_list_t.append(result_t)
        result_dict.update({key: result_list_t})
    return result_dict

result_dict_c  = get_result_dict(crowding_dic)
result_dict_nc = get_result_dict(no_crowding_dic)

def interplote_result_dict_start(result_dict: dict)->dict:
    '''make sure every display local density starts from (100,...)'''
    for key, values in result_dict.items():
        for value in values:
            if value[0][0] != 100:
                value.insert(0,(100,0))
    return result_dict

result_dict_c  = interplote_result_dict_start(result_dict_c)
result_dict_nc = interplote_result_dict_start(result_dict_nc)

#pix to deg 1
result_dict_c_deg    = dict_pix_to_deg(result_dict_c, 1)
result_dict_nc_deg   = dict_pix_to_deg(result_dict_nc, 1)

# note that the avrg_c_dic and crowding_dic are different in values
def get_avrg_result_dict(posis_dict):
    result_avrg_dict = {}
    for key, posi in posis_dict.items():
        result_avrg_t = get_x_y(posi)
        result_avrg_dict.update({key: result_avrg_t})
    return result_avrg_dict

result_avrg_dict_c  = get_avrg_result_dict(avrg_c_dic)
result_avrg_dict_nc = get_avrg_result_dict(avrg_nc_dic)

# convert pix to deg for averaged dict
def pix_to_deg_avrg_dict(inputAvrgDict):
    result_avrg_dict_deg = {}
    for key, long_list in inputAvrgDict.items():
        new_long_list = []
        for posi in long_list:
            new_long_list.append(pix_to_deg_tuple(posi,1))
        result_avrg_dict_deg.update({key:new_long_list})
    return result_avrg_dict_deg

result_avrg_dict_c_deg  = pix_to_deg_avrg_dict(result_avrg_dict_c)
result_avrg_dict_nc_deg = pix_to_deg_avrg_dict(result_avrg_dict_nc)

# averaged numerosity: devided y by 5
def averaged_tuple_y(input_tuple):
    return(input_tuple[0],round(input_tuple[1]/5,4))

def averaged_dictby5(averaged_dict):
    resultf_avrg_dict_deg = {}
    for key, long_list in averaged_dict.items():
        new_list = []
        for result_tuple in long_list:
            new_list.append(averaged_tuple_y(result_tuple))
        resultf_avrg_dict_deg.update({key:new_list})
    return resultf_avrg_dict_deg

resultf_avrg_dict_c_deg  = averaged_dictby5(result_avrg_dict_c_deg)
resultf_avrg_dict_nc_deg = averaged_dictby5(result_avrg_dict_nc_deg)

#%% =============================================================================
# get plots
# 100pix  = 3.839 visual degrees
# =============================================================================
#per display
N = 55
#crowding
to_plot_c  = result_dict_c_deg[N][0]
x_val_1    = [x[0] for x in to_plot_c]
y_val_1    = [x[1] for x in to_plot_c]

norm_y_val_1 = [float(i)/max(y_val_1) for i in y_val_1]

#no-crwoding
to_plot_nc = result_dict_nc_deg[N][0]
x_val_2    = [x[0] for x in to_plot_nc]
y_val_2    = [x[1] for x in to_plot_nc]

norm_y_val_2 = [float(i)/max(y_val_2) for i in y_val_2]
# here is the plot 1 vs 1
fig, ax = plt.subplots(figsize=(7,4.5))
#ax.plot(x_val_1, y_val_1, 'or', label = 'crowding')
ax.plot(x_val_1, norm_y_val_1, '--r', label = 'crowding')
#ax.plot(x_val_2, y_val_2, 'og', label = 'no-crowding')
ax.plot(x_val_2, norm_y_val_2, '--g', label = 'no-crowding')
ax.set_ylabel('Average numerosity')
ax.set_xlabel('Eccentricity(deg)')
#ax.set_title('crowding vs no-crowding 1 display numerosity%s' %(N))
ax.legend(loc = 'best')
ax.set_ylabel('Local Density',fontsize = 15)
ax.set_xlabel('Eccentricity (deg)',fontsize =15)

plt.savefig("try3.svg")
plt.show()

#%% add all display contains same numerosities into one figures, 5 vs. 5
#crowding
N = 55
to_plot_c0  = result_dict_c_deg[N][0]
to_plot_c1  = result_dict_c_deg[N][1]
to_plot_c2  = result_dict_c_deg[N][2]
to_plot_c3  = result_dict_c_deg[N][3]
to_plot_c4  = result_dict_c_deg[N][4]
x_val_c0    = [x[0] for x in to_plot_c0]
x_val_c1    = [x[0] for x in to_plot_c1]
x_val_c2    = [x[0] for x in to_plot_c2]
x_val_c3    = [x[0] for x in to_plot_c3]
x_val_c4    = [x[0] for x in to_plot_c4]
y_val_c0    = [x[1] for x in to_plot_c0]
y_val_c1    = [x[1] for x in to_plot_c1]
y_val_c2    = [x[1] for x in to_plot_c2]
y_val_c3    = [x[1] for x in to_plot_c3]
y_val_c4    = [x[1] for x in to_plot_c4]

def normolizedLD(y_val):
    return [float(i)/max(y_val) for i in y_val]


# dic字典化：key:变量名，value:变量的值
dic_plot = {}
for i in range(5):
    dic_plot["to_plot_nc_deg"+str(i)] = result_dict_nc_deg[N][i]
#no-crowding
# to_plot_nc0 = result_dict_nc[N][0]
# to_plot_nc1 = result_dict_nc[N][1]
# to_plot_nc2 = result_dict_nc[N][2]
# to_plot_nc3 = result_dict_nc[N][3]
# to_plot_nc4 = result_dict_nc[N][4]

# 利用local函数，直接建立变量，本质也是字典
# https://blog.csdn.net/ztf312/article/details/51122027
# https://blog.csdn.net/Baoli1008/article/details/47980779
for i in range(5):
    locals()['x_val_nc'+str(i)] = [x[0] for x in dic_plot["to_plot_nc_deg"+str(i)]]
# x_val_nc0   = [x[0] for x in to_plot_nc0]
# x_val_nc1   = [x[0] for x in to_plot_nc1]
# x_val_nc2   = [x[0] for x in to_plot_nc2]
# x_val_nc3   = [x[0] for x in to_plot_nc3]
# x_val_nc4   = [x[0] for x in to_plot_nc4]

for i in range(5):
    locals()['y_val_nc'+str(i)] = [x[1] for x in dic_plot["to_plot_nc_deg"+str(i)]]
# y_val_nc0   = [x[1] for x in to_plot_nc0]
# y_val_nc1   = [x[1] for x in to_plot_nc1]
# y_val_nc2   = [x[1] for x in to_plot_nc2]
# y_val_nc3   = [x[1] for x in to_plot_nc3]
# y_val_nc4   = [x[1] for x in to_plot_nc4]

fig2, ax2 = plt.subplots(figsize=(7,4.5))

# for num_c in range(5):
#     for point_line in ['or','--r']:
#         ax2.plot(x_val_c0, y_val_c0, 'or', label = 'crowding')

#ax2.plot(x_val_c0, normolizedLD(y_val_c0), 'or')
#ax2.plot(x_val_c1, normolizedLD(y_val_c1), 'or')
#ax2.plot(x_val_c2, normolizedLD(y_val_c2), 'or')
#ax2.plot(x_val_c3, normolizedLD(y_val_c3), 'or')
#ax2.plot(x_val_c4, normolizedLD(y_val_c4), 'or')
ax2.plot(x_val_c0, normolizedLD(y_val_c0), '--r', label = 'crowding')
ax2.plot(x_val_c1, normolizedLD(y_val_c1), '--r')
ax2.plot(x_val_c2, normolizedLD(y_val_c2), '--r')
ax2.plot(x_val_c3, normolizedLD(y_val_c3), '--r')
ax2.plot(x_val_c4, normolizedLD(y_val_c4), '--r')

#ax2.plot(x_val_nc0, normolizedLD(y_val_nc0), 'og')
#ax2.plot(x_val_nc1, normolizedLD(y_val_nc1), 'og')
#ax2.plot(x_val_nc2, normolizedLD(y_val_nc2), 'og')
#ax2.plot(x_val_nc3,normolizedLD (y_val_nc3), 'og')
#ax2.plot(x_val_nc4, normolizedLD(y_val_nc4), 'og')
ax2.plot(x_val_nc0, normolizedLD(y_val_nc0), '--g', label = 'no-crowding')
ax2.plot(x_val_nc1, normolizedLD(y_val_nc1), '--g')
ax2.plot(x_val_nc2, normolizedLD(y_val_nc2), '--g')
ax2.plot(x_val_nc3, normolizedLD(y_val_nc3), '--g')
ax2.plot(x_val_nc4, normolizedLD(y_val_nc4), '--g')




# =============================================================================
# add the average to the same plot
# =============================================================================
N = 55
#crowding
to_plot_avrg_c  = resultf_avrg_dict_c_deg[N]
x_val_avrg_c    = [x[0] for x in to_plot_avrg_c]
y_val_avrg_c    = [x[1] for x in to_plot_avrg_c]
#no-crowding
to_plot_avrg_nc = resultf_avrg_dict_nc_deg[N]
x_val_avrg_nc   = [x[0] for x in to_plot_avrg_nc]
y_val_avrg_nc   = [x[1] for x in to_plot_avrg_nc]


ax2.plot(x_val_avrg_c, normolizedLD(y_val_avrg_c), '-r',linewidth = 3,label = 'crowding average')
ax2.plot(x_val_avrg_nc, normolizedLD(y_val_avrg_nc), '-g',linewidth =3, label = 'no-crowding average')



# =============================================================================
# add difference line
# =============================================================================

#crowding
to_plot_avrg_c  = resultf_avrg_dict_c_deg[N]
x_val_avrg_c    = [x[0] for x in to_plot_avrg_c]
y_val_avrg_c    = [x[1] for x in to_plot_avrg_c]

norm_y_val_avrg_c = [float(i)/max(y_val_avrg_c) for i in y_val_avrg_c]
#no-crowding
to_plot_avrg_nc = resultf_avrg_dict_nc_deg[N]
x_val_avrg_nc   = [x[0] for x in to_plot_avrg_nc]
y_val_avrg_nc   = [x[1] for x in to_plot_avrg_nc]
norm_y_val_avrg_nc = [float(i)/max(y_val_avrg_nc) for i in y_val_avrg_nc]

list_c  = result_avrg_dict_c[N]
list_nc = result_avrg_dict_nc[N]

#call the function here
diffList          = get_max_local_density_eccentricity(list_c, list_nc)[1]
max_local_density = get_max_local_density_eccentricity(list_c, list_nc)[0]

diffList_deg = []
#change pix to deg
for posi in diffList:
    diffList_deg.append(pix_to_deg_tuple(posi,1))
#diveided y by 5
diffList_degf = []
for p in diffList_deg:
    diff = round(p[1]/5,4)
    diffList_degf.append((p[0],diff))

# see difference curve
x_val_diff    = [x[0] for x in diffList_degf]
y_val_diff    = [x[1] for x in diffList_degf]

norm_y_val_diff = [float(i)/55 for i in y_val_diff]
ax2.plot(x_val_diff, norm_y_val_diff, '--k',linewidth =1,label = 'difference')



ax2.set_ylabel('Local Density')
ax2.set_xlabel('eccentricity(deg)')
ax2.set_title('crowding vs no-crowding 5 displays numerosity%s' %(N))
ax2.legend(loc = 'best')

plt.savefig("try3.svg")


#%%=============================================================================
# get plots- average per numerosity (5 display)
# =============================================================================

#here is the plot
fig3,ax3 = plt.subplots(figsize=(7,4.5))
#ax3.plot(x_val_avrg_c, y_val_avrg_c, 'or')
ax3.plot(x_val_avrg_c, y_val_avrg_c, '--r', label = 'crowding')
#ax3.plot(x_val_avrg_nc, y_val_avrg_nc, 'og')
ax3.plot(x_val_avrg_nc, y_val_avrg_nc, '--g', label = 'no-crowding')
ax3.set_ylabel('5 displays total discs')
ax3.set_xlabel('eccentricity(deg)')
ax3.set_title('crowding vs no-crowding average display numerosity%s' %(N))
ax3.legend(loc = 'best')
plt.savefig("try3.svg")

#%%=============================================================================
# find the eccentricity where the 2 displays have the maximum local desnity
# =============================================================================

#TODO : visually-QQ plot 

#direct comparison
# [(10,2),(13,10),(14,17)] --> [(10,2),(11,2),(12,2),(13,10),(14,17)]
def projection_list_all_nature_number(scatter_list:list) ->list:
    '''This function expand y1 and y2 lists with interpolation so that
    they have as many elements as x '''
    all_nature_number_list = []
    # Get individual x, y list
    x_list, y_list = [], []
    for point in scatter_list:
        x_list.append(point[0]) # (10,13,14)
        y_list.append(point[1]) # (2, 10,17)
    x_start, x_end = x_list[0],x_list[-1] # 10, 14
    y_start = y_list[0]
    # loop in (x_min, x_max)
    for x in range(x_start, x_end+1): #(10,11,12,13,14)
        # if init_x already have the nature_number_x, then we add this point into result
        if x in x_list:
            all_nature_number_list.append((x,y_list[0]))
            # remove checked point
            x_list.pop(0)
            y_list.pop(0)
        # if nature_number_x is not in init_x_list, then we add curr_nature_number_x, perious_result_y
        else:
            all_nature_number_list.append((x, all_nature_number_list[-1][1]))
    return all_nature_number_list #this list has continues x

def keep_same_length(list_1_input:list, list_2_input:list):
    '''This function interpolate the 2 inputlist to same length list 
    accourding to 'local density' of the display'''
    list1_temp, list2_temp = copy.deepcopy(list_1_input), copy.deepcopy(list_2_input)
    x_start_1, x_start_2 = list1_temp[0][0], list2_temp[0][0]
    x_end_1, x_end_2 = list1_temp[-1][0], list2_temp[-1][0]
    if x_start_1 != x_start_2:#FIXME
        if x_start_1 < x_start_2:
            for x in range(x_start_2 - 1, x_start_1 - 1, -1):
                list2_temp.insert(0,(x, list2_temp[0][1]))
        else:
            for x in range(x_start_1 - 1, x_start_2 - 1, -1):
                list1_temp.insert(0,(x, list1_temp[0][1]))
    
    if x_end_1 != x_end_2:#Correct
        if x_end_1 > x_end_2:
            for x in range(x_end_2 + 1, x_end_1 + 1):
                list2_temp.append((x, list2_temp[-1][1]))
        else:
            for x in range(x_end_1 + 1, x_end_2 + 1):
                list1_temp.append((x, list1_temp[-1][1]))

    return list1_temp, list2_temp

def get_diff_list(listC: list, listNC: list) -> list: # 2 lists with same length
    '''This function returns the different list of two same length list'''
    diff_list = []
    for i in range(len(listC)):
        d_x = listC[i][0]
        d_y = listC[i][1] - listNC[i][1]
        diff_list.append((d_x,d_y))
    return diff_list

# 得到重合点区间集合list [[x_index_区间1_start, x_index_区间1_end], [区间2],[区间3]....]
# determine when the curves cross by checking whether y2-y1 has changed sign!!!!
def get_range_index(diff_list:list) -> list:
    '''This function returns input lists ranges where the sign of the y_value changed'''
    #将输入的list中按照tuple的y值进行正负划分
    sign_list = []
    for posi in diff_list:
        if posi[1] >= 0:
            sign_list.append((posi[0], 1))
        else:
            sign_list.append((posi[0], -1))
    #get index of of sign_list where the sign changed
    index_list_bv       = [sign_list[0][0]]
    range_index_list_bv = [0]
    for i, posi in enumerate(sign_list):
        y_sign_curr = posi[1]
        if i < len(sign_list)-1:
            y_sign_next = sign_list[i+1][1]
        if y_sign_curr != y_sign_next:
            index_list_bv.append(posi[0])
            range_index_list_bv.append(i)
    # get the output list that is the range where the sign of sign_list chenged
    range_index_list = []
    for index, range_i in enumerate(range_index_list_bv): #value of range_index_list_bv is index of sign_list
        if index < len(range_index_list_bv)-1:
            range_index_list.append((range_i, range_index_list_bv[index+1]))
    # minor correction of the output list
    result_r = [range_index_list[0]]
    for r in range_index_list[1:]:
        result_r.append((r[0]+1,r[1]))
    return result_r

def find_largest_difference_in_each_range(diff_list:list, range_list:list, minDiffVal = 5) -> list:
    '''This function returns the x of the list where the different of two displays
    has the largest local density differnece'''
    curr_diff = []
    result_max = []
    for curr_range in range_list:
        curr_diff = diff_list[curr_range[0]:curr_range[1]+1]
        max_diff_value = max([diff_point[1] for diff_point in curr_diff],key=abs)
        x_max_list = [point[0] for point in curr_diff if point[1] == max_diff_value]
        # median_max_x = int(np.median(x_max_list))
        result_max.append((x_max_list,max_diff_value))
    #del the small difference 
    copy_result_max = copy.copy(result_max)
    for i, result in enumerate(result_max):
        if abs(result[1]) < minDiffVal:
            copy_result_max.remove((result))
    return copy_result_max

def get_max_local_density_eccentricity(listC: list, listNC: list)->list:
    
    new_list1 = projection_list_all_nature_number(listC)
    new_list2 = projection_list_all_nature_number(listNC)
    listC_sameL, listNC_sameL = keep_same_length(new_list1, new_list2)
    dl = get_diff_list(listC_sameL, listNC_sameL)
    current_range = get_range_index(dl)
    result_max_list = find_largest_difference_in_each_range(dl,current_range)
    return result_max_list, dl


#%%sample list
N = 55

#crowding
to_plot_avrg_c  = resultf_avrg_dict_c_deg[N]
x_val_avrg_c    = [x[0] for x in to_plot_avrg_c]
y_val_avrg_c    = [x[1] for x in to_plot_avrg_c]

norm_y_val_avrg_c = [float(i)/max(y_val_avrg_c) for i in y_val_avrg_c]
#no-crowding
to_plot_avrg_nc = resultf_avrg_dict_nc_deg[N]
x_val_avrg_nc   = [x[0] for x in to_plot_avrg_nc]
y_val_avrg_nc   = [x[1] for x in to_plot_avrg_nc]
norm_y_val_avrg_nc = [float(i)/max(y_val_avrg_nc) for i in y_val_avrg_nc]

list_c  = result_avrg_dict_c[N]
list_nc = result_avrg_dict_nc[N]

#call the function here
diffList          = get_max_local_density_eccentricity(list_c, list_nc)[1]
max_local_density = get_max_local_density_eccentricity(list_c, list_nc)[0]

diffList_deg = []
#change pix to deg
for posi in diffList:
    diffList_deg.append(pix_to_deg_tuple(posi,1))
#diveided y by 5
diffList_degf = []
for p in diffList_deg:
    diff = round(p[1]/5,4)
    diffList_degf.append((p[0],diff))

# see difference curve
x_val_diff    = [x[0] for x in diffList_degf]
y_val_diff    = [x[1] for x in diffList_degf]

norm_y_val_diff = [float(i)/55 for i in y_val_diff]

# fig4,ax4 = plt.subplots(figsize=(10,8))
fig4,ax4 = plt.subplots(figsize=(7,4.5))
# ax4.plot(x_val_avrg_c, y_val_avrg_c, 'or')
# c1, = ax4.plot(x_val_avrg_c, y_val_avrg_c, '-r')
# ax4.plot(x_val_avrg_nc, y_val_avrg_nc, 'og')
# nc1, = ax4.plot(x_val_avrg_nc, y_val_avrg_nc, '-g')
d1, = ax4.plot(x_val_diff, norm_y_val_diff, '-k')
# y =0
#plt.axhline(y = 0, color='k', linestyle='-', linewidth=1)

# ax4.set_ylabel('5 displays total discs')
# ax4.set_xlabel('eccentricity(deg)')
# ax4.set_title('crowding vs no-crowding average display numerosity%s' %(N))
# ax4.legend(loc = 'best')

N2 = 23
to_plot_avrg_c  = resultf_avrg_dict_c_deg[N2]
x_val_avrg_c    = [x[0] for x in to_plot_avrg_c]
y_val_avrg_c    = [x[1] for x in to_plot_avrg_c]
#no-crowding
to_plot_avrg_nc = resultf_avrg_dict_nc_deg[N2]
x_val_avrg_nc   = [x[0] for x in to_plot_avrg_nc]
y_val_avrg_nc   = [x[1] for x in to_plot_avrg_nc]

list_c  = result_avrg_dict_c[N2]
list_nc = result_avrg_dict_nc[N2]

#call the function here
diffList          = get_max_local_density_eccentricity(list_c, list_nc)[1]
max_local_density = get_max_local_density_eccentricity(list_c, list_nc)[0]

diffList_deg = []
#change pix to deg
for posi in diffList:
    diffList_deg.append(pix_to_deg_tuple(posi,1))
#diveided y by 5
diffList_degf = []
for p in diffList_deg:
    diff = round(p[1]/5,4)
    diffList_degf.append((p[0],diff))

# see difference curve
x_val_diff    = [x[0] for x in diffList_degf]
y_val_diff    = [x[1] for x in diffList_degf]


# c2, = ax4.plot(x_val_avrg_c, y_val_avrg_c, '--r')
# ax4.plot(x_val_avrg_nc, y_val_avrg_nc, 'og')
# nc2, = ax4.plot(x_val_avrg_nc, y_val_avrg_nc, '--g')
#d2, = ax4.plot(x_val_diff, y_val_diff, '--k')
# y =0
plt.axhline(y = 0, color='gray', linestyle='--', linewidth=1)

ax4.set_ylabel('Local Density Difference',fontsize = 15)
ax4.set_xlabel('Eccentricity(deg)',fontsize =15)
# ax4.set_title('crowding vs no-crowding average display numerosity%s' %(N),fontsize = 20)
# ax4.legend(loc = 'best')

# ax4.legend((c1, nc1, d1, c2, nc2, d2), ('Numerosity 56 crowding', 'Numerosity 56 no-crowding', \
#            'Numerosity 56 difference','Numerosity 23 crowding', 'Numerosity 23 no-crowding', \
#            'Numerosity 23 difference'), loc = 'upper left', shadow = True)
#ax4.legend(( d2, d1), ('Numerosity 23 difference','Numerosity 56 difference'), loc = 'best', shadow = True)
ax4.tick_params(direction='out', length=6, width=2, colors='k', grid_color='r', grid_alpha=0.5)


plt.savefig("try4.svg")
plt.show()
#%%
#call the function for all crowding vs. no-crowding displays
Nmrsty = [21, 22, 23, 24, 25, \
          31, 32, 33, 34, 35, \
          41, 42, 43, 44, 45, \
          49, 50, 51, 52, 53, \
          54, 55, 56, 57, 58]

#for each display,find the max local density difference for between each cross and their corresponding eccentricity 
max_local_density_full_dict = {}
for N in Nmrsty:
    list_c  = result_avrg_dict_c[N]
    list_nc = result_avrg_dict_nc[N]
    max_local_density = get_max_local_density_eccentricity(list_c, list_nc)[0]
    max_local_density_full_dict.update({N: max_local_density})

# FIXME: for now, select the largest local density difference between c and nc displays. 
# for each display, the largerst local density
max_local_density_signle = {}
for key, values in max_local_density_full_dict.items():
    local_density_difference = []
    for i, local_density in enumerate(values):
        local_density_difference.append(local_density[1])
        #find max abs value and its index of the list (the eccentricity and the max local density difference)
        max_index = -1
        max_value = 0
        for i, z in enumerate(local_density_difference):
            value = abs(z)
            if value > max_value:
                max_index = i
                max_value = value
        max_local_density_signle.update({key:(values[max_index])})

#TODO: find max and min values instead of abs values
max_locD_single = {}
min_locD_single = {}

for key, values in max_local_density_full_dict.items():
    locD_diff = []
    for i, locD in enumerate(values):
        locD_diff.append(locD[1])
        #find max values and its index
        max_index, max_value = max(enumerate(locD_diff), key=operator.itemgetter(1))
        max_locD_single.update({key:(values[max_index])})
        #find min
        min_index, min_value = min(enumerate(locD_diff), key=operator.itemgetter(1))
        min_locD_single.update({key:(values[min_index])})

def get_final_result(locD_single):
    '''eccentricity pix to deg, difference divided by 5'''
    locD_singlef = {}
    for key, tuple_values in locD_single.items():
        new_ps = []
        for p in tuple_values[0]:
            new_ps.append(round(p*k,4))
        diff = round(tuple_values[1]/5,4)
        locD_singlef.update({key:(new_ps,diff)})
    return locD_singlef
max_locD_singlef = get_final_result(max_locD_single)
min_locD_singlef = get_final_result(min_locD_single)

#%%
#the original local density for each display result_dic_c_projection, result_dic_nc_projection
#eccentricity where is the max local density differnce between crowding and no-crowding disply: max_local_densitn_dict
def get_result_dic_porjection(inputdict: dict)->dict:
    result_dic_projection = {}
    for key, values in inputdict.items():
        project_list = []
        for list_t in values:
            project_list_t = projection_list_all_nature_number(list_t)
            project_list.append(project_list_t)
        result_dic_projection.update({key: project_list})
    return result_dic_projection

result_dic_c_projection     = get_result_dic_porjection(result_dict_c)
result_dic_nc_projection    = get_result_dic_porjection(result_dict_nc)

def get_deg_projection(input_projection_result):
    result_dic_projection_deg ={}
    for key, values in input_projection_result.items():
        new_values = []
        for display in values:
            new_display = []
            for result_tuple in display:
                new_display.append((round(result_tuple[0]*k,4), result_tuple[1]))
            new_values.append(new_display)
        result_dic_projection_deg.update({key:new_values})
    return result_dic_projection_deg
result_dic_c_projection_deg  = get_deg_projection(result_dic_c_projection)
result_dic_nc_projection_deg = get_deg_projection(result_dic_nc_projection)

#FIXME
def find_local_density_dict(inputdict: dict)->dict:
    '''find local density of all crowding/no-crowding displays in which largerest loc density difference was observed'''
    local_density_list = []
    local_density_dict = {}
    for key, values in inputdict.items():
        local_density_values = []
        for loc_density_list in values:
            eccentricity_at_max_local_density_diff = max_local_density_signle[key][0][0]
            for i, e in enumerate(loc_density_list):
                if e[0] == eccentricity_at_max_local_density_diff:
                    local_density_values.append([loc_density_list[i][1]])
        local_density_list.append(local_density_values)
        local_density_dict.update({key:local_density_values})
    return local_density_dict

local_density_c_dict  = find_local_density_dict(result_dic_c_projection)
local_density_nc_dict = find_local_density_dict(result_dic_nc_projection)
#TODO
#find loc density for all displays at given eccentricty
def find_local_density_dicts(inputdict):
    loc_dnsty_dict_at_max = {}
    loc_dnsty_dict_at_min = {}
    for key, values in inputdict.items():
        loc_dnsty_vlus_at_max_diff = []
        loc_dnsty_vlus_at_min_diff = []
        for loc_den_list in values:
            e_at_max_diff = max_locD_singlef[key][0][0]
            e_at_min_diff = min_locD_singlef[key][0][0]
            for i, e in enumerate(loc_den_list):
                if e[0] == e_at_max_diff:
                    loc_dnsty_vlus_at_max_diff.append([loc_den_list[i][1]])
                elif e[0] == e_at_min_diff:
                    loc_dnsty_vlus_at_min_diff.append([loc_den_list[i][1]])
        loc_dnsty_dict_at_max.update({key:loc_dnsty_vlus_at_max_diff})
        loc_dnsty_dict_at_min.update({key:loc_dnsty_vlus_at_min_diff})
    return loc_dnsty_dict_at_max, loc_dnsty_dict_at_min

local_den_c_dict_at_maxDiff,  local_den_c_dict_at_minDiff  = find_local_density_dicts(result_dic_c_projection_deg)
local_den_nc_dict_at_maxDiff, local_den_nc_dict_at_minDiff = find_local_density_dicts(result_dic_nc_projection_deg)
#%% =============================================================================
# get updated stimuliInfo new
# =============================================================================

# for crowding
df_c3  = df_c.copy()
# add coloum to df, the eccentricity for each dispaly where the local density difference reaches max
df_c3  = df_c3.assign(e_at_max_locDenDiff = [max_locD_singlef[N][0][0] for N in df_c3['N_disk']])
# local density difference researches min
df_c3  = df_c3.assign(e_at_min_locDenDiff = [min_locD_singlef[N][0][0] for N in df_c3['N_disk']])
# new df add coloum positions_list
df_c3_toMerge1  = pd.concat({k: pd.Series(v) for k, v in crowding_dic.items()}, names = ['N_disk','list_index'])
df_c3_toMerge1  = df_c3_toMerge1.to_frame()
df_c3_toMerge1.rename(columns ={0:'positions_list'},inplace = True)
# new df add coloum result_density_projection
df_c3_toMerge2  = pd.concat({k: pd.Series(v) for k, v in result_dic_c_projection_deg.items()}, names = ['N_disk','list_index'])
df_c3_toMerge2  = df_c3_toMerge2.to_frame()
df_c3_toMerge2.rename(columns ={0:'result_density_projection'},inplace = True)
# new df add coloum local_density
df_c3_toMerge3  = pd.concat({k: pd.Series(v) for k, v in local_den_c_dict_at_maxDiff.items()}, names = ['N_disk','list_index'])
df_c3_toMerge3  = df_c3_toMerge3.to_frame()
df_c3_toMerge3.rename(columns ={0:'local_density_at_maxDiff'},inplace = True)

df_c3_toMerge4  = pd.concat({k: pd.Series(v) for k, v in local_den_c_dict_at_minDiff.items()}, names = ['N_disk','list_index'])
df_c3_toMerge4  = df_c3_toMerge4.to_frame()
df_c3_toMerge4.rename(columns ={0:'local_density_at_minDiff'},inplace = True)
# final df to merge
df_c3_toMerge_t    = pd.merge(df_c3_toMerge1,  df_c3_toMerge2,  how = 'left', on = ['N_disk', 'list_index'])
df_c3_toMerge_t2   = pd.merge(df_c3_toMerge_t, df_c3_toMerge3, how = 'left', on = ['N_disk', 'list_index'])
df_c3_toMerge      = pd.merge(df_c3_toMerge_t2,df_c3_toMerge4, how = 'left', on = ['N_disk', 'list_index'])
# merge
df_c3_merged    = pd.merge(df_c3,df_c3_toMerge, how = 'left', on = ['N_disk', 'list_index'])

# for no-crowding
df_nc3  = df_nc.copy()
df_nc3  = df_nc3.assign(e_at_max_locDenDiff = [max_locD_singlef[N][0][0] for N in df_nc3['N_disk']])
df_nc3  = df_nc3.assign(e_at_min_locDenDiff = [min_locD_singlef[N][0][0] for N in df_nc3['N_disk']])
df_nc3_toMerge1  = pd.concat({k: pd.Series(v) for k, v in no_crowding_dic.items()}, names = ['N_disk','list_index'])
df_nc3_toMerge1  = df_nc3_toMerge1.to_frame()
df_nc3_toMerge1.rename(columns ={0:'positions_list'},inplace = True)
df_nc3_toMerge2  = pd.concat({k: pd.Series(v) for k, v in result_dic_nc_projection_deg.items()}, names = ['N_disk','list_index'])
df_nc3_toMerge2  = df_nc3_toMerge2.to_frame()
df_nc3_toMerge2.rename(columns ={0:'result_density_projection'},inplace = True)
df_nc3_toMerge3  = pd.concat({k: pd.Series(v) for k, v in local_den_nc_dict_at_maxDiff.items()}, names = ['N_disk','list_index'])
df_nc3_toMerge3  = df_nc3_toMerge3.to_frame()
df_nc3_toMerge3.rename(columns ={0:'local_density_at_maxDiff'},inplace = True)
df_nc3_toMerge4  = pd.concat({k: pd.Series(v) for k, v in local_den_nc_dict_at_minDiff.items()}, names = ['N_disk','list_index'])
df_nc3_toMerge4  = df_nc3_toMerge4.to_frame()
df_nc3_toMerge4.rename(columns ={0:'local_density_at_minDiff'},inplace = True)

df_nc3_toMerge_t  = pd.merge(df_nc3_toMerge1,  df_nc3_toMerge2,  how = 'left', on = ['N_disk', 'list_index'])
df_nc3_toMerge_t2 = pd.merge(df_nc3_toMerge_t, df_nc3_toMerge3,  how = 'left', on = ['N_disk', 'list_index'])
df_nc3_toMerge    = pd.merge(df_nc3_toMerge_t2,df_nc3_toMerge4, how = 'left', on = ['N_disk', 'list_index'])
df_nc3_merged     = pd.merge(df_nc3,df_nc3_toMerge, how = 'left', on = ['N_disk', 'list_index'])

# contact c and nc
updated_stim_info_df = pd.concat([df_c3_merged, df_nc3_merged])
# check coloum names
updated_stim_info_df.rename(columns ={'positions_list_x':'positions_list'},inplace = True) 
updated_stim_info_df = updated_stim_info_df.drop(['positions_list_y'], axis = 1)

# 'local_density' list of int to int

def convert(list): 
    '''to convert a list of integers into a single integer '''
    # Converting integer list to string list 
    s = [str(i) for i in list] 
    # Join list items using join() 
    res = int("".join(s)) 
    return res
updated_stim_info_df['local_density_at_maxDiff'] = updated_stim_info_df['local_density_at_maxDiff'].apply(lambda coloum: convert(coloum))
updated_stim_info_df['local_density_at_minDiff'] = updated_stim_info_df['local_density_at_minDiff'].apply(lambda coloum: convert(coloum))

# # write to excel if necessary
# updated_stim_info_df.to_excel('../updated_fullstimuliInfo.xlsx',sheet_name = 'Sheet1')
# updated_stim_info_df.to_excel('try1.xlsx',sheet_name = 'Sheet1')

#TODO merge update_stim_info_df with totalData
#totalData_new = pd.read_excel('../cleanedTotalData_fullinfo.xlsx')
totalData_new = pd.read_excel('cleanedTotalData_fullinfo.xlsx')
#to_drop = ['pk',
#           'strictResponse',
#           'expName',
#           'handness',
#           'stimuliPresentTime', 
#           'positions', 
#           'convexHull', 
#           'averageE', 
#           'avg_spacing', 
#           'occupancyArea', 
#           'aggregateSurface', 
#           'density',
#           'count_number1',
#           'count_number2',
#           'count_number3',
#           'count_number4',
#           'count_number5',
#           'count_number6',
#           'count_number7',
#           'count_number8',
#           'count_number9',
#           'count_number10',
#           'count_number11',
#           'count_number12',
#           'count_number13',
#           'count_number14',
#           'count_number15',
#           'count_number16',
#           'count_number17',
#           'count_number18',
#           'count_number19',
#           'count_number20',
#           'count_number21',
#           'count_number22',
#           'count_number23',
#           'count_number24',
#           'count_number25',
#           'count_number26',
#           'count_number27',
#           'count_number28',
#           'count_number29',
#           'count_number30',
#           'count_number']

#totalData_new.drop(columns=to_drop, inplace = True)
# make sure the colums type are same for both files
totalData_new['crowdingcons']     = totalData_new['crowdingcons'].astype(int)
totalData_new['winsize']          = totalData_new['winsize'].astype(float)
totalData_new['index_stimuliInfo']= totalData_new['index_stimuliInfo'].astype(str)
totalData_new['N_disk']           = totalData_new['N_disk'].astype(int)

updated_stim_info_df['crowdingcons']     = updated_stim_info_df['crowdingcons'].astype(int)
updated_stim_info_df['winsize']          = updated_stim_info_df['winsize'].astype(float)
updated_stim_info_df['index_stimuliInfo']= updated_stim_info_df['index_stimuliInfo'].astype(str)
updated_stim_info_df['N_disk']           = updated_stim_info_df['N_disk'].astype(int)
# updated_stim_info_df.to_excel('update_stim_info.xlsx')
# totalData_new.to_excel('try2.xlsx', sheet_name = 'Shee1')
#TODO: Check 2 df coloums that are to be merged
# for col in totalData_new.columns:
#     print(col)
# for col in updated_stim_info_df.columns:
#     print(col)
totalData_new = pd.merge(totalData_new,updated_stim_info_df, how = 'left', on = ['index_stimuliInfo', 'N_disk', 'crowdingcons','winsize'])
# totalData_new.to_excel('try3.xlsx')
# pp_data.drop_duplicates()
#%% =============================================================================
# get updated stimuliInfo (abs value)
# =============================================================================

# # for crowding
# df_c2  = df_c.copy()
# # add coloum to df, the eccentricity for each dispaly where the local density difference reaches max
# df_c2  = df_c2.assign(e_at_max_locDenDiff = [max_local_density_signle[N][0][0] for N in df_c2['N_disk']])
# # new df add coloum positions_list
# df_c_toMerge1  = pd.concat({k: pd.Series(v) for k, v in crowding_dic.items()}, names = ['N_disk','list_index'])
# df_c_toMerge1  = df_c_toMerge1.to_frame()
# df_c_toMerge1.rename(columns ={0:'positions_list'},inplace = True)
# # new df add coloum result_density_projection
# df_c_toMerge2  = pd.concat({k: pd.Series(v) for k, v in result_dic_c_projection.items()}, names = ['N_disk','list_index'])
# df_c_toMerge2  = df_c_toMerge2.to_frame()
# df_c_toMerge2.rename(columns ={0:'result_density_projection'},inplace = True)
# # new df add coloum local_density
# df_c_toMerge3  = pd.concat({k: pd.Series(v) for k, v in local_density_c_dict.items()}, names = ['N_disk','list_index'])
# df_c_toMerge3  = df_c_toMerge3.to_frame()
# df_c_toMerge3.rename(columns ={0:'local_density'},inplace = True)
# # final df to merge
# df_c_toMerge_t = pd.merge(df_c_toMerge1,df_c_toMerge2,  how = 'left', on = ['N_disk', 'list_index'])
# df_c_toMerge   = pd.merge(df_c_toMerge_t,df_c_toMerge3, how = 'left', on = ['N_disk', 'list_index'])
# # merge
# df_c_merged    = pd.merge(df_c2,df_c_toMerge, how = 'left', on = ['N_disk', 'list_index'])

# # do same for no crowding
# df_nc2  = df_nc.copy()
# df_nc2  = df_nc2.assign(e_at_max_locDenDiff = [max_local_density_signle[N][0][0] for N in df_nc2['N_disk']])
# df_nc_toMerge1  = pd.concat({k: pd.Series(v) for k, v in no_crowding_dic.items()}, names = ['N_disk','list_index'])
# df_nc_toMerge1  = df_nc_toMerge1.to_frame()
# df_nc_toMerge1.rename(columns ={0:'positions_list'},inplace = True)
# df_nc_toMerge2  = pd.concat({k: pd.Series(v) for k, v in result_dic_nc_projection.items()}, names = ['N_disk','list_index'])
# df_nc_toMerge2  = df_nc_toMerge2.to_frame()
# df_nc_toMerge2.rename(columns ={0:'result_density_projection'},inplace = True)
# df_nc_toMerge3  = pd.concat({k: pd.Series(v) for k, v in local_density_nc_dict.items()}, names = ['N_disk','list_index'])
# df_nc_toMerge3  = df_nc_toMerge3.to_frame()
# df_nc_toMerge3.rename(columns ={0:'local_density'},inplace = True)
# df_nc_toMerge_t = pd.merge(df_nc_toMerge1, df_nc_toMerge2,  how = 'left', on = ['N_disk', 'list_index'])
# df_nc_toMerge   = pd.merge(df_nc_toMerge_t,df_nc_toMerge3, how = 'left', on = ['N_disk', 'list_index'])
# df_nc_merged    = pd.merge(df_nc2,df_nc_toMerge, how = 'left', on = ['N_disk', 'list_index'])

# # contact c and nc
# updated_stim_info_df = pd.concat([df_c_merged, df_nc_merged])
# # check coloum names
# updated_stim_info_df.rename(columns ={'positions_list_x':'positions_list'},inplace = True) 
# updated_stim_info_df = updated_stim_info_df.drop(['positions_list_y'], axis = 1)

# # 'local_density' list of int to int
# updated_stim_info_df['local_density'] = updated_stim_info_df['local_density'].apply(lambda coloum: convert(coloum))

# # # write to excel if necessary
# # updated_stim_info_df.to_excel('../updated_fullstimuliInfo.xlsx',sheet_name = 'Sheet1')
# # updated_stim_info_df.to_excel('try1.xlsx',sheet_name = 'Sheet1')

# #TODO merge update_stim_info_df with totalData
# totalData_new = pd.read_excel('../cleanedTotalData_fullinfo.xlsx')
# to_drop = ['pk',
#            'strictResponse',
#            'expName',
#            'handness',
#            'stimuliPresentTime', 
#            'positions', 
#            'convexHull', 
#            'averageE', 
#            'avg_spacing', 
#            'occupancyArea', 
#            'aggregateSurface', 
#            'density',
#            'count_number1',
#            'count_number2',
#            'count_number3',
#            'count_number4',
#            'count_number5',
#            'count_number6',
#            'count_number7',
#            'count_number8',
#            'count_number9',
#            'count_number10',
#            'count_number11',
#            'count_number12',
#            'count_number13',
#            'count_number14',
#            'count_number15',
#            'count_number16',
#            'count_number17',
#            'count_number18',
#            'count_number19',
#            'count_number20',
#            'count_number21',
#            'count_number22',
#            'count_number23',
#            'count_number24',
#            'count_number25',
#            'count_number26',
#            'count_number27',
#            'count_number28',
#            'count_number29',
#            'count_number30',
#            'count_number']

# totalData_new.drop(columns=to_drop, inplace = True)
# # make sure the colums type are same for both files
# totalData_new['crowdingcons']     = totalData_new['crowdingcons'].astype(int)
# totalData_new['winsize']          = totalData_new['winsize'].astype(float)
# totalData_new['index_stimuliInfo']= totalData_new['index_stimuliInfo'].astype(str)
# totalData_new['N_disk']           = totalData_new['N_disk'].astype(int)

# updated_stim_info_df['crowdingcons']     = updated_stim_info_df['crowdingcons'].astype(int)
# updated_stim_info_df['winsize']          = updated_stim_info_df['winsize'].astype(float)
# updated_stim_info_df['index_stimuliInfo']= updated_stim_info_df['index_stimuliInfo'].astype(str)
# updated_stim_info_df['N_disk']           = updated_stim_info_df['N_disk'].astype(int)
# # totalData_new.to_excel('try2.xlsx', sheet_name = 'Shee1')
# #TODO: Check 2 df coloums that are to be merged
# # for col in totalData_new.columns:
# #     print(col)
# # for col in updated_stim_info_df.columns:
# #     print(col)
# totalData_new = pd.merge(totalData_new,updated_stim_info_df, how = 'left', on = ['index_stimuliInfo', 'N_disk', 'crowdingcons','winsize'])
# # totalData_new.to_excel('try3.xlsx')
# # pp_data.drop_duplicates()
#%% =============================================================================
# deviation against local density (local density as a interpreter)
# =============================================================================
pivotT1 = pd.pivot_table(totalData_new,index = ['crowdingcons','participant_N',], columns = ['winsize','N_disk', 'local_density_at_maxDiff', 'e_at_max_locDenDiff'],values = ['deviation_score'])
# pivotT1.to_excel('try4_1.xlsx')

pivotT2 = pd.pivot_table(totalData_new,index = ['crowdingcons','participant_N',], columns = ['winsize','N_disk', 'local_density_at_minDiff', 'e_at_min_locDenDiff'],values = ['deviation_score'])
# pivotT2.to_excel('try4_2.xlsx')



