import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class CA:
	"""
	NOTES:
		According to Topa the complexity of the river system is measured by the number of
		channels and bifurcations

		”Anastomosing river” term refers to river system that possess extremely complex
		network of forking and joining channels

		The new channels usually merge with the others, creating a complex network composed
		of splitting and merging water channels and small lakes

	"""

	def __init__(
			self, size, slope, mu, gamma, rho, time_limit, rand_lower=0.9999, rand_upper=1.00001,
			branch_tresh=0.1, init_water=1, delta_water=0.001
	):
		self.size = size
		self.slope = slope
		self.time_limit = time_limit
		self.branch_tresh = branch_tresh
		self.init_water_level = init_water
		# starting point in the middle of the grid
		self.starting_column = int(self.size / 2)
		self.delta_w = delta_water
		self.terrain = np.zeros((size, size))
		self.peat_bog = np.zeros((size, size))
		self.nutrients = np.zeros((size, size))
		self.cur_river_nr = 0
		self.rivers = {}

		self.path = np.zeros((size, size))

		self.mu = mu             # viscosity
		self.gamma = gamma       # gradient of nutrients concentration
		self.rho = rho           # proportionality coefficient
		self.rand_lower = rand_lower
		self.rand_upper = rand_upper
		self.river_coors = set()

	def moore_neighborhood(self, grid, i, j):

		if i == 0 and j == 0:
			neighborhood = [
				grid[i + 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
			]
			locations = [
				[i + 1, j + 1],
				[i, j + 1],
				[i + 1, j]
			]

		elif i == 0 and j == (self.size-1):
			neighborhood = [
				grid[i, j - 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
			]
			locations = [
				[i, j - 1],
				[i + 1, j - 1],
				[i + 1, j],
			]

		elif i == 0 and 0 < j < (self.size-1):
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]
			locations = [
				[i, j - 1],
				[i, j + 1],
				[i + 1, j - 1],
				[i + 1, j],
				[i + 1, j + 1],
			]

		elif i == (self.size-1) and j == 0:
			neighborhood = [
				grid[i, j + 1],
				grid[i - 1, j + 1],
				grid[i - 1, j],
			]
			locations = [
				[i, j + 1],
				[i - 1, j + 1],
				[i - 1, j],
			]

		elif i == (self.size-1) and j == (self.size-1):
			neighborhood = [
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i - 1, j],
			]
			locations = [
				[i - 1, j - 1],
				[i, j - 1],
				[i - 1, j],
			]

		elif i == (self.size-1) and 0 < j < (self.size-1):
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i - 1, j - 1],
				grid[i - 1, j],
				grid[i - 1, j + 1],
			]
			locations = [
				[i, j - 1],
				[i, j + 1],
				[i - 1, j - 1],
				[i - 1, j],
				[i - 1, j + 1],
			]

		elif 0 < i < (self.size-1) and j == 0:
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]
			locations = [
				[i - 1, j],
				[i - 1, j + 1],
				[i, j + 1],
				[i + 1, j],
				[i + 1, j + 1],
			]

		elif 0 < i < (self.size-1) and j == (self.size-1):
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i + 1, j],
				grid[i + 1, j - 1],
			]
			locations = [
				[i - 1, j],
				[i - 1, j - 1],
				[i, j - 1],
				[i + 1, j],
				[i + 1, j - 1],
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
				[i - 1, j - 1],
				[i - 1, j],
				[i - 1, j + 1],
				[i, j - 1],
				[i, j + 1],
				[i + 1, j - 1],
				[i + 1, j],
				[i + 1, j + 1],
			]

		return neighborhood, locations

	def initialize_terrain(self):
		"""
		slope of 0.05% and randomness,

		NEW: add "hills" to the terrain
		"""
		terrain = np.ones((self.size, self.size))

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * (1 - self.slope)

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				if rd.random() < 0.01:
					perturb = rd.uniform(0.999, 1.0001)
				else:
					perturb = rd.uniform(self.rand_lower, self.rand_upper)
				terrain[i, j] = np.mean(neighbors) * perturb

		# create hill top
		hill_coords = [
			(0, int(self.size/2)),
			(int(self.size / 4), int(self.size / 2)),
		]
		terrain[hill_coords] = terrain[hill_coords] * 1.05

		# from hill top, create hill
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

		self.terrain = terrain
		return self.terrain

	def get_location_of_lowest_neighbor(self, grid, i, j, temp_ends):
		neighborhood = self.moore_neighborhood(grid, i, j)
		neighborhood0, neighborhood1 = [], []
		for i, val in enumerate(neighborhood[1]):
			if tuple(val) not in self.river_coors:
				# and tuple(val) not in temp_ends
				neighborhood0.append(neighborhood[0][i])
				neighborhood1.append(val)
		try:
			value, location = (list(t) for t in zip(*sorted(zip(neighborhood0, neighborhood1))))
		except ValueError:
			value, location = [], []
		
		return value, location

	def get_path(self, prev_val, coor_list, value_list):
		for i, coor in enumerate(coor_list):
			tup = tuple(coor)
			if tup not in self.river_coors:
				self.river_coors.add(tup)
			else:
				pass
			self.path[tup] = self.path[tup] + float(prev_val[i])*(1-self.delta_w)
		return self.path

	def create_path_from_start(self):
		self.path = self.get_path([self.init_water_level/(1-self.delta_w)],[(0, self.starting_column)], [self.init_water_level])

		self.river_coors.add((0, self.starting_column))
		cur_ends = set()
		cur_ends.add((0, self.starting_column))

		for x in range(1, self.time_limit):
			temp_ends = set()
			for i, item in enumerate(cur_ends):
				if self.path[item] > self.branch_tresh:
					old_value = self.terrain[item]
					sort_values, sort_location = self.get_location_of_lowest_neighbor(self.terrain, item[0], item[1], temp_ends)
					if not sort_values:
						continue
					next_cell, next_value = [tuple(sort_location[0])], [sort_values[0]]
					temp_ends.add(next_cell[0])
					next_water = [self.path[item]]
					if old_value < sort_values[0] and len(sort_location) > 1:
						next_cell.append(tuple(sort_location[1]))
						next_value.append(sort_values[1])
						next_water = self.new_water_ratio(item, tuple(sort_location[0]), tuple(sort_location[1]))
						temp_ends.add(next_cell[1])
						# print('value', next_cell, next_value, self.path[next_cell[0]])
					self.path = self.get_path(next_water, next_cell, next_value)
					# try:
					# 	print(self.path[tuple(sort_location[0])], self.path[tuple(sort_location[1])])
					# except:
					# 	pass
			cur_ends = temp_ends.copy()
			if not cur_ends:
				return self.path

		return self.path

	def new_water_ratio(self, old, coor_split1, coor_split2):
		new_l = self.terrain[coor_split1] - self.terrain[old]
		new_r = self.terrain[coor_split2] - self.terrain[old]
		l = new_l/(new_l + new_r) * self.path[old]
		r = new_r/(new_l + new_r) * self.path[old]
		return [l, r]


if __name__ == "__main__":
	for i in range(1):
		size = 200
		slopes = [0.0001, 0.0002, 0.0005, 0.0008, 0.001]
		for slope in slopes:
			ca = CA(size=size, slope=slope, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=size)
			terrain = ca.initialize_terrain()
			path = ca.create_path_from_start()
			np.savetxt(f'tests/test_final.csv', path, delimiter=',')
			fig, axes = plt.subplots(1, 2)
			sns.heatmap(terrain[:, 0:size-1], cmap="Greens", ax=axes[0])
			sns.heatmap(path, cmap="Blues", ax=axes[1])
			axes[1].set_title("Path of river without bifurcation")
			# plt.savefig(f'plots/river_{i}.png', dpi=300)
			plt.show()
