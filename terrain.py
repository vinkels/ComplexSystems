import numpy as np
import matplotlib.pyplot as plt
import random as rd
import seaborn as sns


terrain = np.zeros((100, 100))
terrain[0] = np.ones(100)

rd.seed(1)
for j in range(1, 100):
	terrain[0, 0] = terrain[0, 0] * rd.uniform(0.96, 1.04)
	terrain[0, j] = terrain[0, j - 1] * rd.uniform(0.96, 1.04)

for i in range(99):
	for j in range(99):
		if terrain[i, j + 1] and terrain[i, j - 1]:
			mean = (terrain[i, j - 1] + terrain[i, j] + terrain[i, j + 1])/3
			terrain[i+1, j] = mean * rd.uniform(0.98, 1)
		if terrain[i, j + 1] and not terrain[i, j - 1]:
			mean = (terrain[i, j] + terrain[i, j + 1]) / 2
			terrain[i + 1, j] = mean * rd.uniform(0.98, 0.99)
		if terrain[i, j - 1] and not terrain[i, j + 1]:
			mean = (terrain[i, j] + terrain[i, j - 1]) / 2
			terrain[i + 1, j] = mean * rd.uniform(0.98, 0.99)


river_starting_point = rd.sample(range(100), 1)
terrain[0, river_starting_point] = 2

for i in range(99):
	col = river_starting_point[0]
	if terrain[i + 1, col - 1] == min(terrain[i + 1, col - 1], terrain[i + 1, col], terrain[i + 1, col + 1]):
		terrain[i + 1, col - 1] = 2
	if terrain[i + 1, col] == min(terrain[i + 1, col - 1], terrain[i + 1, col], terrain[i + 1, col + 1]):
		terrain[i + 1, col] = 2
	if terrain[i + 1, col + 1] == min(terrain[i + 1, col - 1], terrain[i + 1, col], terrain[i + 1, col + 1]):
		terrain[i + 1, col + 1] = 2


ax = sns.heatmap(terrain[:, 0:99])
plt.show()
