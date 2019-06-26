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
		self.peat_bog = np.zeros((size, size))
		self.nutrients = np.zeros((size, size))
		self.path = np.zeros((size, size))

		self.rand_lower = rand_lower
		self.rand_upper = rand_upper
		self.river_coors = set()
		self.segment_grid = {}
		self.excluded_segments = {}
		self.cur_river_nr = 1
		self.segment_dict = {}
		self.slope = slope
		self.merge_dict, self.split_dict = {}, {}

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

		elif i == 0 and j == (self.size - 1):
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

		elif i == 0 and 0 < j < (self.size - 1):
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

		elif i == (self.size - 1) and j == 0:
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

		elif i == (self.size - 1) and j == (self.size - 1):
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

		elif i == (self.size - 1) and 0 < j < (self.size - 1):
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

		elif 0 < i < (self.size - 1) and j == 0:
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

		elif 0 < i < (self.size - 1) and j == (self.size - 1):
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

	def get_location_of_lowest_neighbor(self, grid, i, j, river_nr):
		neighborhood = self.moore_neighborhood(grid, i, j)
		neighborhood0, neighborhood1 = [], []
		for i, val in enumerate(neighborhood[1]):
			val_tup = tuple(val)
			if val_tup in self.segment_grid:
				if self.segment_grid[val_tup] not in self.excluded_segments[river_nr]:
					neighborhood0.append(neighborhood[0][i])
					neighborhood1.append(val)
			else:
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
			print(i)
			if tup not in self.river_coors:
				self.river_coors.add(tup)
				if not self.segment_grid and len(coor_list) == 1:
					self.excluded_segments[self.cur_river_nr] = [self.cur_river_nr]
					self.segment_grid[tup] = self.cur_river_nr
					self.segment_dict[self.cur_river_nr] = [tup]
					self.cur_river_nr += 1
				elif len(coor_list) > 1:
					# print('splitsing', coor_list, self.cur_river_nr)
					self.excluded_segments[self.cur_river_nr] = [self.cur_river_nr]
					self.segment_grid[tup] = self.cur_river_nr
					self.segment_dict[self.cur_river_nr] = [tup]
					self.cur_river_nr += 1

					
				else:
					self.segment_dict[self.segment_grid[prev_coor]].append(tup)
					self.segment_grid[tup] = self.segment_grid[prev_coor]

			else:
				self.excluded_segments[self.cur_river_nr] = [
					self.cur_river_nr, self.segment_grid[prev_coor], self.segment_grid[tup]
				]
				self.merge_dict[self.segment_grid[prev_coor], self.segment_grid[tup]] = self.cur_river_nr
				self.update_segment(tup, self.segment_grid[tup], self.cur_river_nr)
				self.segment_grid[tup] = self.cur_river_nr
				self.segment_dict[self.cur_river_nr] = [tup]
				self.cur_river_nr += 1
				self.split_dict[self.segment_grid[prev_coor]] = (self.cur_river_nr - 1, self.cur_river_nr)
			self.path[tup] = self.path[tup] + float(prev_val[i]) * (1 - self.delta_w)
		print(self.merge_dict)
		print(self.split_dict)
		return self.path

	def update_segment(self, coor, old_nr, new_nr):
		# print(coor)
		# print(self.segment_dict)
		# print(self.segment_grid)
		coor_idx = self.segment_dict[old_nr].index(coor)
		self.segment_dict[new_nr] = self.segment_dict[old_nr][coor_idx:]
		self.segment_dict[old_nr] = self.segment_dict[old_nr][:coor_idx]
		for val in self.segment_dict[new_nr]:
			self.segment_grid[val] = new_nr
		return self.segment_dict

	def create_path_from_start(self):

		self.path = self.get_path(
			[self.init_water_level / (1 - self.delta_w)], [(0, self.starting_column)],
			[self.init_water_level], [(0, self.starting_column)]
		)

		self.river_coors.add((0, self.starting_column))
		cur_ends = set()
		cur_ends.add((0, self.starting_column))

		x = 1
		while x < self.time_limit:
		# for x in range(1, self.time_limit - 1):
			temp_ends = set()
			for i, item in enumerate(cur_ends):
				if self.path[item] > self.branch_tresh:
					old_value = self.terrain[item]
					sort_values, sort_location = self.get_location_of_lowest_neighbor(
						self.terrain, item[0], item[1], self.segment_grid[item]
					)
					if not sort_values:
						continue

					next_cell, next_value = [tuple(sort_location[0])], [sort_values[0]]
					temp_ends.add(next_cell[0])
					# print("voor if", temp_ends)
					next_water = [self.path[item]]
					print(next_water)
					if old_value < sort_values[0] and len(sort_location) > 1:
						print("BINNEN DE IF")
						next_cell.append(tuple(sort_location[1]))
						next_value.append(sort_values[1])
						next_water = self.new_water_ratio(item, tuple(sort_location[0]), tuple(sort_location[1]))

						print("NEXT CELL", next_cell)
						previous_cells = next_cell
						print("NEXT VALUE", next_value)
						print("NEXT WATER", next_water)
						temp_ends.add(next_cell[1])
						print("TEMP_END BEFORE LEGS", temp_ends)

						self.path = self.get_path(next_water, next_cell, next_value, item)

						x += 1
						# SAVE AFTER SPLITTING LOCATION
						first_leg = sort_location[0]
						second_leg = sort_location[1]
						temp_ends.remove(next_cell[0])
						temp_ends.remove(next_cell[1])

						print("VOOR LOOP ", temp_ends)

						next_cell = []
						next_value = []
						next_water = []
						for leg in [first_leg, second_leg]:
							# print("BINNEN DE LOOP")
							print('leggy', leg, self.path[tuple(leg)])
							next_water.append(self.path[tuple(leg)])
							print('legz', next_water)
							
							if (leg[0]+1 < self.time_limit) and (leg[1]+1 < self.time_limit):
								if leg[1] > item[1]:
									next_cell.append((leg[0]+1, leg[1]+1))
									next_value.append(self.terrain[leg[0]+1, leg[1]+1])
								elif leg[1] < item[1]:
									next_cell.append((leg[0]+1, leg[1]-1))
									next_value.append(self.terrain[leg[0]+1, leg[1]-1])
								else:
									next_cell.append((leg[0]+1, leg[1]))
									next_value.append(self.terrain[leg[0]+1, leg[1]])
							else:
								print("KUT")
							# print("BINNEN LOOP", next_cell)
							# temp_ends.add(next_cell)
						
						print("NA LOOP")
						print("NEXT CELL", next_cell)
						print("NEXT VALUE", next_value)
						print("NEXT WATER", next_water)
						print(len(next_cell), next_cell)
						temp_ends.add(next_cell[0])
						
						temp_ends.add(next_cell[1])
						print("na if ", temp_ends)

						self.path = self.get_path(next_water, next_cell, [next_value], item)
						continue
					self.path = self.get_path(next_water, next_cell, next_value, item)

			cur_ends = temp_ends.copy()
			if not cur_ends:
				return self.path
			x += 1
		return self.path

	def new_water_ratio(self, old, coor_split1, coor_split2):
		new_l = self.terrain[coor_split1] - self.terrain[old]
		new_r = self.terrain[coor_split2] - self.terrain[old]
		l = new_l / (new_l + new_r) * self.path[old]
		r = new_r / (new_l + new_r) * self.path[old]
		return [l, r]

	def initialize_terrain(self):
		terrain = np.ones((self.size, self.size))

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				if rd.random() < 0.01:
					perturb = rd.uniform(0.999, 1.0001)
				else:
					perturb = rd.uniform(self.rand_lower, self.rand_upper)
				terrain[i, j] = np.mean(neighbors) * perturb

		# create hill top coordinates
		hill_coordinates = [
			(int(self.size / 8), int(self.size / 1.2)),
			(int(self.size / 3), int(self.size / 5)),
			(int(self.size / 1.6), int(self.size / 1.4)),
		]
		for hill_coords in hill_coordinates:
			terrain[hill_coords] = terrain[hill_coords] # * 1

		for _ in range(5):

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
			terrain[i] = terrain[i] * (1 - self.slope * i)

		self.terrain = terrain

		return self.terrain


if __name__ == "__main__":
	for i in range(1):
		ca = CA(size=200, time_limit=200, slope=0.0005)
		terrain = ca.initialize_terrain()
		path = ca.create_path_from_start()
		np.savetxt(f'tests/test_final.csv', path, delimiter=',')

		plt.figure(figsize=(15, 5))

		plt.subplot2grid((1, 2), (0, 0))
		sns.heatmap(terrain[:, 0:99], cmap="Greens")
		plt.title("Terrain with slope")

		plt.subplot2grid((1, 2), (0, 1))
		sns.heatmap(path, cmap="Blues")
		plt.title("River")
		plt.savefig(f'plots/river_{i}.png', dpi=300)
		# plt.show()
