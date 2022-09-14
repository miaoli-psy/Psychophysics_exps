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

    def cal_convexhull(self, pix_to_deg = 0.04):
        return round((ConvexHull(self.__posilist_array).area * pix_to_deg), 2)

    def cal_occupancyarea(self, pix_to_deg = 0.04):
        return round((ConvexHull(self.__posilist_array).volume * pix_to_deg ** 2), 2)

    def cal_averge_eccentricity(self, pix_to_deg = 0.04):
        all_eccentricity = [distance.euclidean(posi, (0, 0)) * pix_to_deg for posi in self.__posilist_array]
        return cal_average(all_eccentricity)

    def get_reduced_occupancyarea(self, pix_to_deg = 0.04):
        if Properties.cal_occupancyarea(self, pix_to_deg = pix_to_deg) - 24.3 <= 0:
            return 0.01
        else:
            return Properties.cal_occupancyarea(self, pix_to_deg = pix_to_deg) - 24.3

    def cal_reduced_density(self, pix_to_deg = 0.04):
        return self.numerosity / Properties.get_reduced_occupancyarea(self, pix_to_deg = pix_to_deg)

    def get_average_spacing(self, pix_to_deg = 0.04):
        distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(self.__posilist_array, 2)]
        return round(sum(distances) / len(distances) * pix_to_deg, 2)


if __name__ == "__main__":
    debug = True
    if debug:

        display = [(40.0, -120.0), (-100.0, -140.0), (-150.0, 140.0), (190.0, -40.0), (160.0, 30.0), (40.0, 130.0),
                 (-110.0, 50.0), (-90.0, -60.0), (-70.0, 130.0), (-10.0, 110.0), (-170.0, -100.0), (200.0, 110.0),
                 (200.0, -140.0), (110.0, -100.0), (-180.0, 10.0), (-60.0, 80.0), (90.0, -50.0), (-100.0, 0.0),
                 (110.0, 0.0), (120.0, 100.0), (70.0, 80.0), (-20.0, -100.0), (-77.46746137207484, 2.633735716099064),
                 (100.77865346429805, -80.55853892438033), (-55.11543431918825, 64.09025858456687),
                 (43.41089642228717, 113.26120732511156), (-54.12481099211016, 97.8047455823826),
                 (73.45857468321843, -37.05748374547572), (128.7911073973631, -2.154502220810187),
                 (-3.951072287525264, 129.1561544176747), (230.69706598541285, -145.24359535169557),
                 (-210.72275077315788, 9.0151591088567), (-110.04880816563916, -72.9412842659512),
                 (243.64978031413, 141.56896918845945), (-149.87905683994097, -76.37328038636734),
                 (-192.76819914312085, -121.38254784166146), (99.23817650830601, 82.94450092367947),
                 (149.0120832744205, 120.51691786480215), (61.16271055665176, 73.11424164328652),
                 (80.51701522204715, 99.57680558473928), (-15.325125728324442, -76.82531515345265),
                 (-24.77065585760659, -122.66256808728733), (-87.79120464780723, 47.99903513352782),
                 (-126.56572616491628, 46.21025035216981)]

        a = Properties(display).get_reduced_occupancyarea(0.04)
        b = Properties(display).cal_occupancyarea(0.04)
        f = Properties(display).cal_reduced_density(0.04)
