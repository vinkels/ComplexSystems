import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class CA:
	def __init__(self, size):
		self.size = size
		self.terrain = np.zeros((size, size))

		self.mu = 0.0004          # viscosity
		self.gamma = 0.0002       # gradient of nutrients concentration
		self.rho = 0.02         # proportionality coefficient

	def moore_neighborhood(self, grid, i, j):
		if not grid[i - 1, j]:
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]

		elif not grid[i + 1, j]:
			neighborhood = [
				grid[i, j - 1],
				grid[i, j + 1],
				grid[i - 1, j - 1],
				grid[i - 1, j],
				grid[i - 1, j + 1],
			]

		elif not grid[i, j - 1]:
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
				grid[i + 1, j + 1],
			]

		elif not grid[i, j + 1]:
			neighborhood = [
				grid[i - 1, j],
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i + 1, j],
				grid[i + 1, j - 1],
			]

		elif not grid[i, j - 1] and not grid[i - 1, j]:
			neighborhood = [
				grid[i + 1, j + 1],
				grid[i, j + 1],
				grid[i + 1, j],
			]

		elif not grid[i, j + 1] and not grid[i + 1, j]:
			neighborhood = [
				grid[i - 1, j - 1],
				grid[i, j - 1],
				grid[i - 1, j],
			]

		elif not grid[i, j + 1] and not grid[i - 1, j]:
			neighborhood = [
				grid[i, j - 1],
				grid[i + 1, j - 1],
				grid[i + 1, j],
			]

		elif not grid[i, j - 1] and not grid[i + 1, j]:
			neighborhood = [
				grid[i, j + 1],
				grid[i - 1, j + 1],
				grid[i - 1, j],
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
		return neighborhood

	def initialize_terrain(self):
		"""
		slope of 0.05% and
		"""
		terrain = self.terrain
		terrain[0] = np.ones(self.size)

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * 0.9995

		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.moore_neighborhood(terrain, i, j)
				print(neighbors)

		# self.terrain[:, 1] = rd.uniform(0.99, 1.01)

		self.terrain = terrain
		return

	def get_terrain(self):
		return self.terrain


if __name__ == "__main__":
	ca = CA(2)
	ca.initialize_terrain()
	# print(ca.get_terrain())
