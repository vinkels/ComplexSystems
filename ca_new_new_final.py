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

	def __init__(self, size, mu, gamma, rho, time_limit, rand_lower=0.9999, rand_upper=1.00001, branch_tresh = 0.1, init_water=1, delta_water=0.001):
		self.size = size
		self.time_limit = time_limit
		self.branch_tresh = branch_tresh
		self.init_water_level = init_water
		# starting point in the middle of the grid
		self.starting_column = int(self.size / 2)
		self.delta_w = delta_water
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
		self.segment_grid = np.zeros()
		self.river_segments = {}
		self.cur_river_nr = 1

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
		slope of 0.05% and randomness, else the river will be a strait line down
		"""
		terrain = self.terrain
		terrain[0] = np.ones(self.size)

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * 0.9995

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				if rd.random() < 0.01:
					perturb = rd.uniform(0.999, 1.0001)
				else:
					perturb = rd.uniform(self.rand_lower, self.rand_upper)
				terrain[i, j] = np.mean(neighbors) * perturb

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

	def get_path(self, prev_val, coor_list, value_list, prev_coor):
		for i, coor in enumerate(coor_list):
			tup = tuple(coor)
			# if self.path[tup] > self.branch_tresh:
			if tup not in self.river_coors:
				self.river_coors.add(tup)
				# self.path[tup] = prev_val[i]*(1-self.delta_w)
				if len(coor_list) > 1:
					self.segment_grid[tuple(coor)] = self.cur_river_nr
					self.river_segments[self.cur_river_nr] = [self.cur_river_nr, self.segment_grid[prev_coor]]
					self.cur_river_nr += 1
				else:
					self.segment_grid[coor] = self.segment_grid[prev_coor]

			else:
				self.river_segments[self.cur_river_nr] = [self.cur_river_nr] + [self.segment_grid[tup], self.segment_grid[prev_coor]]
				self.segment_grid[tup] = self.cur_river_nr
				self.cur_river_nr += 1
				# print('jup', self.path[tup], value_list[i])
			self.path[tup] = self.path[tup] + float(prev_val[i])*(1-self.delta_w)
			# self.path[tup] = self.path[tup] + prev_val[i]*(1-self.delta_w)
		return self.path

	def create_path_from_start(self):
		# print(self.init_water_level/(1-self.delta_w))
		self.path = self.get_path([self.init_water_level/(1-self.delta_w)],[(0, self.starting_column)], [self.init_water_level], [(0, self.starting_column)])
		self.segment_grid[(0, self.starting_column)] = self.cur_river_nr
		self.river_segments[(0, self.starting_column)] = [self.cur_river_nr]
		self.cur_river_nr += 1
		# sort_values, sort_location = self.get_location_of_lowest_neighbor(self.terrain, 0, self.starting_column, self.river_coors)
		
		# next_cell = sort_location[0]
		self.river_coors.add((0, self.starting_column))
		cur_ends = set()
		cur_ends.add((0, self.starting_column))
		

		for x in range(1, self.time_limit):
			temp_ends = set()
			for i, item in enumerate(cur_ends):
				# print(item)
				if self.path[item] > self.branch_tresh:
					# print('kom ik hier???')
					old_value = self.terrain[item]
					sort_values, sort_location = self.get_location_of_lowest_neighbor(self.terrain, item[0], item[1], temp_ends)
					if not sort_values:
						# print('hier eerst')
						continue
					# print(old_value, sort_values[0])
					# print('zit ik hier vast?',i)

					next_cell, next_value = [tuple(sort_location[0])], [sort_values[0]]
					temp_ends.add(next_cell[0])
					next_water = [self.path[item]]
					# print(old_value, sort_values, sort_location)
					if old_value < sort_values[0] and len(sort_location) > 1:
						next_cell.append(tuple(sort_location[1]))
						next_value.append(sort_values[1])
						self.segment_grid[tuple(sort_location[0])] = self.cur_river_nr
						self.river_segments[self.cur_river_nr] = [self.cur_river_nr, self.segment_grid[item]]
						self.cur_river_nr += 1
						self.segment_grid[tuple(sort_location[1])] = self.cur_river_nr
						self.river_segments[self.cur_river_nr] = [self.cur_river_nr, self.segment_grid[item]]
						self.cur_river_nr += 1

						next_water = self.new_water_ratio(item, tuple(sort_location[0]), tuple(sort_location[1]))

						temp_ends.add(next_cell[1])
					else:
						self.segment_grid[tuple(sort_location[0])] = self.segment_grid[item]
						# print('value', next_cell, next_value, self.path[next_cell[0]])
					self.path = self.get_path(next_water, next_cell, next_value, item)
					try:
						print(self.path[tuple(sort_location[0])], self.path[tuple(sort_location[1])])
					except:
						pass
			cur_ends = temp_ends.copy()
			# np.savetxt(f'tests/test_{x}.csv', self.path, delimiter=',')
			if not cur_ends:
				# print('kom ik hier')
				return self.path
			
			# print('---------------------------------------------------------')

		return self.path

	def new_water_ratio(self, old, coor_split1, coor_split2):
		new_l = self.terrain[coor_split1] - self.terrain[old]
		new_r = self.terrain[coor_split2] - self.terrain[old]
		l = new_l/(new_l + new_r) * self.path[old]
		r = new_r/(new_l + new_r) * self.path[old]
		return [l, r]


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
	for i in range(1):
		ca = CA(size=500, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=500)
		terrain = ca.initialize_terrain()
		path = ca.create_path_from_start()
		np.savetxt(f'tests/test_final.csv', path, delimiter=',')
		fig, axes = plt.subplots(1, 2)
		sns.heatmap(terrain[:, 0:99], cmap="BrBG_r", vmin=0.85, vmax=1.005, ax=axes[0])
		axes[0].set_title("Terrain with slope 5%")
		sns.heatmap(path, cmap="Blues", ax=axes[1])
		axes[1].set_title("Path of river without bifurcation")
		plt.savefig(f'plots/river_{i}.png', dpi=300)