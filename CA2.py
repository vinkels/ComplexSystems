import numpy as np
import random as rd
import matplotlib.pyplot as plt


class River:
	def __init__(self, size, n):
		self.n = n
		self.size = size
		self.grid = np.zeros((size, size))
		self.river_layer = 0
		self.river_end = 0

		self.ca = self.initiate_n_rivers(size, self.grid, n)

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

	def calculate_flow(self):
		# initialize the water distribution array
		pass

	def update_water(self):
		pass

	def update_peatbog(self):
		pass

	def update_terrain(self):
		pass


if __name__ == "__main__":
	rv = River(100, 4)
	for i in range(99):
		rv.generate_river()

	plt.imshow(rv.grid)
	plt.show()
