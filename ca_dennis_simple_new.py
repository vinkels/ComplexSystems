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

	def __init__(self, size, mu, gamma, rho, time_limit, rand_lower=0.9993, rand_upper=1.00001):
		self.size = size
		self.time_limit = time_limit

		# starting point in the middle of the grid
		self.starting_column = int(self.size / 2)

		self.terrain = np.zeros((size, size))
		self.peat_bog = np.zeros((size, size))
		self.nutrients = np.zeros((size, size))

		self.path = np.zeros((size, size))

		self.mu = mu             # viscosity
		self.gamma = gamma       # gradient of nutrients concentration
		self.rho = rho           # proportionality coefficient
		self.rand_lower = rand_lower
		self.rand_upper = rand_upper
		self.river_coors = set()

	def moore_neighborhood(self, grid, i, j):

		# vind de laagste en de location waar je heen moet
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
		# print(i,j,neighborhood)
		# print('------------------------------------')
		return neighborhood, locations

	def initialize_terrain(self):
		"""
		slope of 0.05% and randomness, else the river will be a strait line down
		"""
		terrain = self.terrain
		terrain[0] = np.ones(self.size)

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * 0.9995

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				terrain[i, j] = np.mean(neighbors) * rd.uniform(self.rand_lower, self.rand_upper)

		self.terrain = terrain
		return self.terrain

	def get_location_of_lowest_neighbor(self, grid, i, j):
		neighborhood = self.moore_neighborhood(grid, i, j)
		neighborhood0, neighborhood1 = [], []
		# print(i,j)
		for i, val in enumerate(neighborhood[1]):
			# print('river', neighborhood0, val, self.river_coors)
			if tuple(val) not in self.river_coors:
				neighborhood0.append(neighborhood[0][i])
				neighborhood1.append(val)
				# if neighborhood[0][i] > grid[i,j]:
					# print('dit kan gewoon')
			else:
				print(self.river_coors)
				# print(val)
		# index waar in neighbourhood[0] de laagste waarde zit
		
		# index_in_neighborhood_list = np.argmin(neighborhood0)
		# location = neighborhood1[index_in_neighborhood_list]
		# print(neighborhood0, neighborhood1)
		# print('check deze', neighborhood0, neighborhood1)
		try:
			value, location = (list(t) for t in zip(*sorted(zip(neighborhood0, neighborhood1))))
		except ValueError:
			value, location = [], []
		
		# print(value, location)
		# print(neighborhood0)
		# print(neighborhood1)
		# print(location)
		# print('+++++++++++++++++++++++++++++++++')
		return value, location

	# def get_next_cell_for_path(self, i, j):
	# 	next_cell_location = self.get_location_of_lowest_neighbor(self.terrain, i, j)[1]
	# 	return next_cell_location

	def get_path(self, coor_list):
		for coor in coor_list:
			self.river_coors.add(tuple(coor))
			self.path[coor[0], coor[1]] = 1
		return self.path

	def create_path_from_start(self):
		sort_values, sort_location = self.get_location_of_lowest_neighbor(self.terrain, 0, self.starting_column)
		next_cell = sort_location[0]
		self.path = self.get_path([next_cell])
		next_cell = sort_location[0]
		self.river_coors.add((next_cell[0], next_cell[1]))
		cur_ends = set()
		cur_ends.add((next_cell[0], next_cell[1]))
		

		for _ in range(1, self.time_limit):
			temp_ends = set()
			for i, item in enumerate(cur_ends):
				old_value = self.terrain[item]
				sort_values, sort_location = self.get_location_of_lowest_neighbor(self.terrain, item[0], item[1])
				if not sort_values:
					continue
				print(old_value, sort_values[0])
				print('zit ik hier vast?',i)
				next_cell = [tuple(sort_location[0])]
				temp_ends.add(next_cell[0])

				if old_value < sort_values[0] and len(sort_location) > 1:
					print(sort_location)
					next_cell.append(tuple(sort_location[1]))
					temp_ends.add(next_cell[1])
				self.path = self.get_path(next_cell)
			cur_ends = temp_ends.copy()
			if not cur_ends:
				return self.path

		return self.path

	def create_path_from_bifurcation(self):
		""" WIP """
		return self.path

	def calculate_flow(self):

		pass

	def calculate_nutrient_distribution(self):

		for i in range(self.size):
			for j in range(self.size):
				if self.water[i, j] > 0:
					self.nutrients[i, j] = 1
				else:
					neighborhood = self.moore_neighborhood(self.nutrients[i, j])
					max_value = max(neighborhood)
					self.nutrients[i, j] = self.gamma * max_value

		return self.nutrients

	def calculate_peat_growth(self):

		for i in range(self.size):
			for j in range(self.size):
				if self.water[i, j] > 0:
					self.peat_bog[i, j] = self.mu * self.nutrients[i, j]
				else:
					self.peat_bog[i, j] = self.rho * self.nutrients[i, j]

		return self.peat_bog


if __name__ == "__main__":
	for i in range(10):
		ca = CA(size=100, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=100)
		terrain = ca.initialize_terrain()
		path = ca.create_path_from_start()

		fig, axes = plt.subplots(1, 2)
		sns.heatmap(terrain[:, 0:99], cmap="BrBG_r", vmin=0.85, vmax=1.005, ax=axes[0])
		axes[0].set_title("Terrain with slope 5%")
		sns.heatmap(path, cmap="Blues", ax=axes[1])
		axes[1].set_title("Path of river without bifurcation")
		plt.savefig(f'plots/river_{i}.png', dpi=300)
