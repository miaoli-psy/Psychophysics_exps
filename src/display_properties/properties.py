from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np


class Properties:
    def __init__(self, posilist):
        self.numerosity = len(posilist)
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.occupancy_area = round(self.__hull.volume * 0.0016, 2)
        # self.occupancy_area = round(self.__hull.volume)
        self.density = round(len(posilist) / self.occupancy_area, 4)


if __name__ == "__main__":
    debug = True
    if debug:
        # properties = Properties([(-10, -10), (-10, 10), (10, 10), (10, -10)])
        properties = Properties([(50.0, -110.0), (130.0, -100.0), (60.0, 90.0), (100.0, -30.0), (120.0, 110.0), (-140.0, -90.0), (-40.0, -100.0), (150.0, 40.0), (110.0, 70.0), (-140.0, 100.0), (-100.0, 0.0), (110.0, -70.0), (-120.0, 30.0), (-40.0, 100.0), (-90.0, -100.0), (-120.0, -40.0), (-100.0, 90.0), (-150.0, 20.0), (130.0, 0.0), (60.0, -80.0), (-90.0, -50.0), (100.0, 30.0), (-80.0, 60.0), (10.0, -100.0), (10.0, 100.0)])

        a = properties.numerosity
        b = properties.occupancy_area
        e = properties.density
        print("numerosity is", a, ";",
              "occupancy area is", b, ";",
              "density is", e, "item/cm2")