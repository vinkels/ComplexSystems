import numpy as np
import random as rd

grid = np.zeros((10, 10))

for i in range(10):
    for j in range(10):
        grid[i,j] = (10 - (i + 1)) + (rd.randint(0,10)/10 - 0.5)
print(grid)

