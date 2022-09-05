from scipy.spatial import distance, ConvexHull
from itertools import combinations
import numpy as np

def cal_average(lst):
    return round(sum(lst) / len(lst), 2)

class Properties:
    def __init__(self, posilist, pix_to_deg = 0.04):
        self.__posilist_array = np.asarray(posilist)
        self.__hull = ConvexHull(self.__posilist_array)
        self.pix_to_deg_index = pix_to_deg
        # self.convexhull = round(self.__hull.area * (0.25 / 3.82), 2)
        self.convexhull = round(self.__hull.area * pix_to_deg, 2)
        # self.occupancy_area = round(self.__hull.volume * ((0.25 / 3.82) ** 2), 2)
        self.occupancy_area = round(self.__hull.volume * pix_to_deg ** 2, 2)
        self.occupancy_area_reduced = round(self.__hull.volume * pix_to_deg ** 2 - 46.28, 2)
        self.averge_eccentricity = self.cal_averge_eccentricity()
        self.average_spacing = self.get_average_spacing()
        self.density = round(len(posilist) / self.occupancy_area, 4)
        self.density_no_fovea = round(len(posilist) / self.occupancy_area_reduced, 4)
        self.numerosity = len(posilist)

    def cal_averge_eccentricity(self):
        all_eccentricity = [distance.euclidean(posi, (0, 0)) * self.pix_to_deg_index for posi in self.__posilist_array]
        return cal_average(all_eccentricity)

    def get_average_spacing(self, pix_to_deg_index = 0.04):
        distances = [distance.euclidean(p1, p2) for p1, p2 in combinations(self.__posilist_array, 2)]
        return round(sum(distances) / len(distances) * pix_to_deg_index, 2)


if __name__ == "__main__":
    debug = True
    if debug:
        # properties = Properties([(-10, -10), (-10, 10), (10, 10), (10, -10)])
        # properties = Properties([(90.0, -190.0), (-50.0, 110.0), (70.0, 130.0), (-230.0, 200.0), (10.0, 130.0), (-90.0, 50.0), (-120.0, -210.0), (120.0, -20.0), (100.0, 20.0), (-180.0, -100.0), (190.0, 210.0), (-30.0, -160.0), (300.0, 160.0), (280.0, 0.0), (170.0, 20.0), (40.0, 200.0), (250.0, -220.0), (130.0, 80.0), (-280.0, -220.0), (-110.0, -10.0), (190.0, -50.0), (-130.0, 100.0), (60.0, 80.0), (-70.0, -110.0), (-80.0, -60.0), (-250.0, -20.0), (-190.0, 60.0), (-50.0, 170.0), (80.0, -80.0), (10.0, -100.0), (63.037706991355776, -186.5867510442862), (-34.42698896095055, 108.65922909332131), (95.03880962487848, 113.68041214099404), (-208.99972765453114, 242.54079395347063), (29.135565369164937, 137.63002738726308), (-77.02909088370784, 64.01737629295614), (-139.54912402820702, -178.92601842434098), (117.23745014660392, -33.35724150684963), (109.23239521926628, 4.495434582161053), (-200.06114557053814, -68.63171126040928), (197.44905442513948, 175.34056439316666), (-48.25179101779932, -146.94149383038612), (329.5541003029318, 90.91737086790616), (298.75832730563, -45.45807606409417), (185.26092922843597, -6.5106514677005975), (5.351317018743657, 210.42113202484728), (276.4401496090195, -167.11977413018496), (131.54793417257366, 102.76234744685618), (-233.13482495295005, -267.0948026751147), (-110.37970192579482, -26.44579833940338), (209.37128769061644, -10.254593327727719), (-137.23157059745478, 80.94436495259325), (47.30726118969915, 96.14145649461105), (-42.4030234586609, -123.03210206891787), (-71.1230293097679, -75.66461499282164), (-228.44060248761286, -56.57164363967263), (-187.55412387759475, 31.666739874747748), (-86.41046588650889, 168.53821269877704), (89.54737853708588, -59.8959692021973), (26.25331084554105, -94.71357939782682)])
        properties = Properties([(50.0, -110.0), (130.0, -100.0), (60.0, 90.0), (100.0, -30.0), (120.0, 110.0), (-140.0, -90.0), (-40.0, -100.0), (150.0, 40.0), (110.0, 70.0), (-140.0, 100.0), (-100.0, 0.0), (110.0, -70.0), (-120.0, 30.0), (-40.0, 100.0), (-90.0, -100.0), (-120.0, -40.0), (-100.0, 90.0), (-150.0, 20.0), (130.0, 0.0), (60.0, -80.0), (-90.0, -50.0), (100.0, 30.0), (-80.0, 60.0), (10.0, -100.0), (10.0, 100.0)])

        a = properties.numerosity
        b = properties.occupancy_area
        e = properties.density
        print("numerosity is", a, ";",
              "occupancy area is", b, ";",
              "density is", e, "item/cm2")