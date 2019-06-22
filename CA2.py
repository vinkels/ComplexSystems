import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class River:
	def __init__(self, size, n, p_branch=0.0, p_direct=0.5):
		self.n = n
		self.size = size

		self.grid = np.zeros((size, size))
		self.terrain = np.zeros((size, size))

		self.river_layer = 0
		self.river_end = 0

		self.p_branch = p_branch
		self.p_direct = p_direct

		self.ca = self.initiate_n_rivers(self.size, self.grid, self.n)

	def initiate_n_rivers(self, size, grid, n):
		starting_points = rd.sample(range(0, size - 1), n)
		grid[0, starting_points] = 1
		self.river_end = list(zip([0] * n, starting_points))
		return grid

	def generate_river(self):
		self.river_layer += 1

		new_river_end = []
		for val in self.river_end:
			if val[1] == self.size - 1:
				direct = rd.randint(-1, 0)
			elif val[1] == 0:
				direct = rd.randint(0, 1)
			else:
				direct = rd.randint(-1, 1)
			x, y = self.river_layer, (val[1] + direct)
			self.grid[(x, y)] = 1
			new_river_end.append((x, y))
		self.river_end = new_river_end
		return new_river_end

	def terrain_height(self):
		"""
		According to the paper, the terrain is slightly inclined (the slope is 0.05%) and rough

		On plot, the height decreases approximately 5% in 100 steps
		"""
		terrain = self.terrain
		terrain[0] = np.ones(100)

		for i in range(self.size - 1):
			for j in range(self.size - 1):
				if terrain[i, j + 1] and terrain[i, j - 1]:
					mean = (terrain[i, j - 1] + terrain[i, j] + terrain[i, j + 1]) / 3
					terrain[i + 1, j] = mean * rd.uniform(0.999, 1)
				if terrain[i, j + 1] and not terrain[i, j - 1]:
					mean = (terrain[i, j] + terrain[i, j + 1]) / 2
					terrain[i + 1, j] = mean * rd.uniform(0.999, 0.9999)
				if terrain[i, j - 1] and not terrain[i, j + 1]:
					mean = (terrain[i, j] + terrain[i, j - 1]) / 2
					terrain[i + 1, j] = mean * rd.uniform(0.999, 0.9999)

		self.terrain = terrain
		return self.terrain

	def calculate_flow(self):
		# initialize the water distribution array
		pass

	def update_water(self):
		"""

		:return:
		"""
		pass

	def update_peatbog(self):
		pass

	def update_terrain(self):
		pass


if __name__ == "__main__":
	rv = River(100, 4)
	for i in range(99):
		rv.generate_river()

	terrain = rv.terrain_height()

	ax = sns.heatmap(terrain[:, 0:99])
	plt.show()

	plt.imshow(rv.grid)
	plt.show()
