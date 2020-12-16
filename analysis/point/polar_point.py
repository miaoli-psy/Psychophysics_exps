from scipy.spatial import distance
import math
from typing import Tuple, List

# convert Cartesian corrdinates to Polar coordinates
def __get_radius(posi:Tuple[float, float]) -> float:
    """
    get distance between posi and the display center
    """
    return distance.euclidean(posi, (0,0))

def __get_angle_not_on_axis(posi:Tuple[float, float]) -> float:
    if posi[0] > 0 and posi[1] > 0:
        return math.degrees(math.atan(posi[1]/posi[0]))
    elif posi[0] > 0 and posi[1] < 0:
        return math.degrees(math.atan(posi[1]/posi[0]))+360
    else:
        return math.degrees(math.atan(posi[1]/posi[0]))+180

def __get_angle_on_axis(posi:Tuple[float, float]) -> float:
    if posi[0] == 0 and posi[1] > 0:
        return 90
    elif posi[0] ==0 and posi[1] < 0:
        return 270
    elif posi[0] > 0 and posi[1] == 0:
        return 0
    elif posi[0] < 0 and posi[1] == 0:
        return 180

def __get_angle(posi:Tuple[float, float]) -> float:
    """
    get angle for polor corrdinates
    """
    # Edge case
    if posi == (0, 0):
        raise Exception(f"Error: Current position {posi} cannot get valid angle, such as (0, 0)")
    # axis: 0, 90, 180, 270
    is_not_on_axis = (posi[0] != 0 and posi[1] != 0)
    if is_not_on_axis:
        angle = __get_angle_not_on_axis(posi)
    else:
        angle = __get_angle_on_axis(posi)
    return angle

def get_polar_coordinates(inputposilist:List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    """
    get polar coordinates for all disc positions
    """
    radius = [round(__get_radius(p)) for p in inputposilist]
    angle = [round(__get_angle(p)) for p in inputposilist]
    
    polar_coordinates = []
    for x, y in zip(angle, radius):
        polar_coordinates.append((x,y))
    
    #sort by tuple's first value (angle)
    polar_coordinates.sort()
    return polar_coordinates


if __name__ == '__main__':
    assert 90 == __get_angle((0, 18))
    assert 270 == __get_angle((0, -18))
    # __get_angle((0, 0))