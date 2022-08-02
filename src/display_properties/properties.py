from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np


class Properties:
    def __init__(self, posilist):
        self.numerosity = len(posilist)
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.occupancy_area = round(self.__hull.volume * ((0.25 / 3.82) ** 2), 2)
        self.density = round(len(posilist) / self.occupancy_area, 4)


if __name__ == "__main__":
    debug = True
    if debug:
        properties = Properties([(20, 0), (25, 5), (100, 75), (50, 50), (-75, 65)])
        a = properties.numerosity
        b = properties.occupancy_area
        e = properties.density
        print("numerosity is", a, ";",
              "occupancy area is", b, ";",
              "density is", e, "item/cm2")