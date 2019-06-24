import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class CA:
	def __init__(self, size):
		self.size = size
		self.time_limit = size

		self.starting_column = int(self.size / 2)

		self.terrain = np.zeros((size, size))
		self.path = np.zeros((size, size))

		self.mu = 0.0004          # viscosity
		self.gamma = 0.0002       # gradient of nutrients concentration
		self.rho = 0.02         # proportionality coefficient

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
		slope of 0.05% and random
		"""
		terrain = self.terrain
		terrain[0] = np.ones(self.size)

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * 0.9995

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)[0]
				terrain[i, j] = np.mean(neighbors) * rd.uniform(0.99995, 1.00005)

		self.terrain = terrain
		return self.terrain

	def get_location_of_lowest_neighbor(self, grid, i, j):
		neighborhood = self.moore_neighborhood(grid, i, j)
		index_in_neighborhood_list = np.argmin(neighborhood[0])
		location = neighborhood[1][index_in_neighborhood_list]
		return location

	def get_next_cell_for_path(self, i, j):
		next_cell_location = self.get_location_of_lowest_neighbor(self.terrain, i, j)[1]
		return next_cell_location

	def get_path(self, i, j):
		self.path[i, j] = 1
		return self.path

	def create_path_from_start(self):
		next_cell = self.get_location_of_lowest_neighbor(self.terrain, 0, self.starting_column)
		self.path = self.get_path(next_cell[0], next_cell[1])

		for _ in range(1, self.time_limit):
			next_cell = self.get_location_of_lowest_neighbor(self.terrain, next_cell[0], next_cell[1])
			self.path = self.get_path(next_cell[0], next_cell[1])

		return self.path


if __name__ == "__main__":
	ca = CA(100)
	terrain = ca.initialize_terrain()
	path = ca.create_path_from_start()

	fig, axes = plt.subplots(1, 2)
	sns.heatmap(terrain[:, 0:99], cmap="BrBG_r", vmin=0.85, vmax=1.005, ax=axes[0])
	sns.heatmap(path, ax=axes[1])

	plt.show()
