#practice heat map

import numpy as np
import matplotlib.pyplot as plt


x_axes = (1,2,3,4,5,6,7,8)
y_axes = ('circle 1', 'circle 2', 'circle 3')

heatmap = ((8,8,8,8,8,8,8,8), (9,9,9,9,9,9,9,10), (8,8,8,8,8,8,8,8))

data = np.array(heatmap)

#data = np.array([x_axes], [y_axes])
#data = np.random.random((12, 12))
plt.imshow(data, cmap = 'jet')

plt.colorbar()

plt.yticks((0, 1, 2), y_axes)

plt.title('fadfsa')
plt.xlabel('x axis')
plt.xlabel('y axis')
plt.show()