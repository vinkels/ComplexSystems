import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class CA:

	def __init__(
			self, size, time_limit, slope, rand_lower=0.9999, rand_upper=1.00001,
			branch_tresh=0.1, init_water=1, delta_water=0.001
	):
		self.size = size
		self.time_limit = time_limit
		self.branch_tresh = branch_tresh
		self.init_water_level = init_water

		# starting point in the middle of the grid
		self.starting_column = int(self.size / 2)
		self.delta_w = delta_water
		self.terrain = np.zeros((size, size))
		self.path = np.zeros((size, size))

		self.rand_lower = rand_lower
		self.rand_upper = rand_upper
		self.river_coors = set()
		self.segment_grid = {}
		self.excluded_segments = {}
		self.cur_river_nr = 1
		self.segment_dict = {}
		self.slope = slope
		self.temp_ends = set()

	def moore_neighborhood(self, grid, i, j):

		if i == 0 and j == 0:
			neighborhood = [
				grid[i + 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
			]
			locations = [
				(i + 1, j + 1),
				(i, j + 1),
				(i + 1, j)
			]

		elif i == 0 and j == (self.size - 1):
			neighborhood = [
				grid[i, j - 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
			]
			locations = [
				(i, j - 1),
				(i + 1, j - 1),
				(i + 1, j),
			]

		elif i == 0 and 0 < j < (self.size - 1):
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]
			locations = [
				(i, j - 1),
				(i, j + 1),
				(i + 1, j - 1),
				(i + 1, j),
				(i + 1, j + 1),
			]

		elif i == (self.size - 1) and j == 0:
			neighborhood = [
				grid[i, j + 1],
				grid[i - 1, j + 1],
				grid[i - 1, j],
			]
			locations = [
				(i, j + 1),
				(i - 1, j + 1),
				(i - 1, j),
			]

		elif i == (self.size - 1) and j == (self.size - 1):
			neighborhood = [
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i - 1, j],
			]
			locations = [
				(i - 1, j - 1),
				(i, j - 1),
				(i - 1, j),
			]

		elif i == (self.size - 1) and 0 < j < (self.size - 1):
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i - 1, j - 1],
				grid[i - 1, j],
				grid[i - 1, j + 1],
			]
			locations = [
				(i, j - 1),
				(i, j + 1),
				(i - 1, j - 1),
				(i - 1, j),
				(i - 1, j + 1),
			]

		elif 0 < i < (self.size - 1) and j == 0:
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]
			locations = [
				(i - 1, j),
				(i - 1, j + 1),
				(i, j + 1),
				(i + 1, j),
				(i + 1, j + 1),
			]

		elif 0 < i < (self.size - 1) and j == (self.size - 1):
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i + 1, j],
				grid[i + 1, j - 1],
			]
			locations = [
				(i - 1, j),
				(i - 1, j - 1),
				(i, j - 1),
				(i + 1, j),
				(i + 1, j - 1),
			]

		else:
			neighborhood = [
				grid[i - 1, j - 1],
				grid[i - 1, j],
				grid[i - 1, j + 1],
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]
			locations = [
				(i - 1, j - 1),
				(i - 1, j),
				(i - 1, j + 1),
				(i, j - 1),
				(i, j + 1),
				(i + 1, j - 1),
				(i + 1, j),
				(i + 1, j + 1),
			]

		return neighborhood, locations

	def initialize_terrain(self):
		terrain = np.ones((self.size, self.size))

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * (1 - self.slope)

		# create hill top coordinates
		hill_coordinates = [
			(0, int(self.size / 4)),
			(0, int(self.size / 2)),
			(0, int(self.size * 3 / 4)),
			# (int(self.size / 2), int(self.size / 2)),
			# (int(self.size / 3), int(self.size / 2.5)),
			# (int(self.size / 3), int(self.size / 2/5)),
			# (int(self.size / 1.6), int(self.size / 1.4)),
		]
		for hill_coords in hill_coordinates:
			terrain[hill_coords] = terrain[hill_coords] * 1.0

		for _ in range(1):

			for i in range(self.size):
				for j in range(self.size):
					neighborhood, locations = self.moore_neighborhood(terrain, i, j)
					for n, neighbor in enumerate(neighborhood):
						location = (locations[n][0], locations[n][1])
						if ((terrain[i, j] - neighbor) / neighbor) > 0.01:
							terrain[location] = terrain[i, j] * rd.uniform(0.995, 0.999)

			for i in range(self.size - 1, 0, -1):
				for j in range(self.size - 1, 0, -1):
					neighborhood, locations = self.moore_neighborhood(terrain, i, j)
					for n, neighbor in enumerate(neighborhood):
						location = (locations[n][0], locations[n][1])
						if ((terrain[i, j] - neighbor) / neighbor) > 0.01:
							terrain[location] = terrain[i, j] * rd.uniform(0.995, 0.999)

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				perturb = rd.uniform(self.rand_lower, self.rand_upper) #* (1 - self.slope)
				terrain[i, j] = np.mean(neighbors) * perturb

		self.terrain = terrain

		return self.terrain

	def new_water_ratio(self, old, coor_split1, coor_split2):
		new_l = self.terrain[coor_split1] - self.terrain[old]
		new_r = self.terrain[coor_split2] - self.terrain[old]
		l = new_l / (new_l + new_r) * self.path[old]
		r = new_r / (new_l + new_r) * self.path[old]
		return [l, r]
	
	def get_path(self, coordinates):
		self.path[coordinates] = 1
		return self.path
	
	def get_location_of_lowest_neighbor(self, grid, coordinates):
		neighborhood, locations = self.moore_neighborhood(grid, coordinates[0], coordinates[1])

		try:
			neighbor, location = (list(t) for t in zip(*sorted(zip(neighborhood, locations))))
		except ValueError:
			print("GEEN BUREN BESCHIKBAAR")
			neighbor, location = [], []

		return neighbor, location
	
	def create_path_from_start(self):
		self.path[0, self.starting_column] = self.init_water_level
		next_cell = (0, self.starting_column)

		previous_lowest_neighbor = []
		for _ in range(self.time_limit):
			neighbor, location = self.get_location_of_lowest_neighbor(self.terrain, next_cell)
			next_cell = location[0]
			self.path = self.get_path(next_cell)

		return self.path


if __name__ == "__main__":
	for i in range(1):
		ca = CA(size=200, time_limit=100, slope=0.0001)
		terrain = ca.initialize_terrain()
		path = ca.create_path_from_start()
		# np.savetxt(f'tests/test_final.csv', path, delimiter=',')

		plt.figure(figsize=(15, 5))

		plt.subplot2grid((1, 2), (0, 0))
		sns.heatmap(terrain[:, 0:199], cmap="Greens")
		plt.title("Terrain with slope")

		plt.subplot2grid((1, 2), (0, 1))
		sns.heatmap(path, cmap="Blues")
		plt.title("River")
		# plt.savefig(f'plots/river_{i}.png', dpi=300)
		plt.show()
