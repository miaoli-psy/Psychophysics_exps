from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np


def cal_average(lst):
    return round(sum(lst) / len(lst), 2)


class Properties:
    def __init__(self, posilist):
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.average_spacing = self.get_average_spacing()
        self.numerosity = len(posilist)
        self.density_reduced = self.cal_reduced_density()

    def cal_convexhull(self, pix_to_deg = 0.03):
        return round((ConvexHull(self.__posilist_array).area * pix_to_deg), 2)

    def cal_occupancyarea(self, pix_to_deg = 0.03):
        return round((ConvexHull(self.__posilist_array).volume * pix_to_deg ** 2), 2)

    def cal_averge_eccentricity(self, pix_to_deg = 0.03):
        all_eccentricity = [distance.euclidean(posi, (0, 0)) * pix_to_deg for posi in self.__posilist_array]
        return cal_average(all_eccentricity)

    def get_reduced_occupancyarea(self, pix_to_deg = 0.03):
        if Properties.cal_occupancyarea(self, pix_to_deg = pix_to_deg) - 24.3 <= 0:
            return 0.01
        else:
            return Properties.cal_occupancyarea(self, pix_to_deg = pix_to_deg) - 24.3

    def cal_reduced_density(self, pix_to_deg = 0.03):
        return self.numerosity / Properties.get_reduced_occupancyarea(self, pix_to_deg = pix_to_deg)

    def get_average_spacing(self, pix_to_deg = 0.03):
        distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(self.__posilist_array, 2)]
        return round(sum(distances) / len(distances) * pix_to_deg, 2)


if __name__ == "__main__":
    debug = False
    if debug:
        display = [(50.0, -110.0), (130.0, -100.0), (60.0, 90.0), (100.0, -30.0), (120.0, 110.0), (-140.0, -90.0),
                   (-40.0, -100.0), (150.0, 40.0), (110.0, 70.0), (-140.0, 100.0), (-100.0, 0.0), (110.0, -70.0),
                   (-120.0, 30.0), (-40.0, 100.0), (-90.0, -100.0), (-120.0, -40.0), (-100.0, 90.0), (-150.0, 20.0),
                   (130.0, 0.0), (60.0, -80.0), (-90.0, -50.0), (100.0, 30.0), (-80.0, 60.0), (10.0, -100.0),
                   (10.0, 100.0)]

        display = [(50.0, -110.0), (130.0, -100.0), (60.0, 90.0), (100.0, -30.0), (120.0, 110.0), (-140.0, -90.0),
                   (-40.0, -100.0)]

        f = Properties(display).cal_reduced_density(0.03)
