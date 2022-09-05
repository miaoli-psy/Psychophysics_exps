import matplotlib.pyplot as plt
from scipy.spatial import distance
import numpy as np
import math
from operator import itemgetter

posi = [(90.0, 110.0), (-120.0, -80.0), (140.0, -80.0), (-120.0, 100.0), (130.0, -130.0), (-100.0, 50.0), (-60.0, -90.0), (200.0, 130.0), (-150.0, -10.0), (140.0, 10.0), (-200.0, 30.0), (-60.0, 120.0), (100.0, 60.0), (-150.0, -140.0), (-40.0, -140.0), (-160.0, -50.0), (200.0, -70.0), (10.0, -110.0), (30.0, 120.0), (-30.0, 120.0), (190.0, -20.0), (50.0, -120.0), (-180.0, 80.0), (170.0, 50.0), (100.0, -30.0), (0.0, 130.0), (70.0, -100.0), (-100.0, 130.0), (80.0, -70.0), (-110.0, 20.0), (100.0, 30.0), (60.0, 120.0)]

eccen_list = list()
for p in posi:
    e = math.sqrt(p[0] ** 2 + p[1] ** 2)
    eccen_list.append(e)

eccen_array = np.array(eccen_list)
sort_index = np.argsort(eccen_array).tolist()


x_val = [x[0] for x in posi]
y_val = [x[1] for x in posi]

fig, ax = plt.subplots()
ax.plot(x_val, y_val, "ro")

plt.show()