import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class River:
	"""
	class following the Topa paper

	"""
	def __init__(self, size, n, p_branch=0.0, p_direct=0.5):
		self.n = n
		self.size = size

		# source cell, cell to which the water is supplied
		self.starting_points = rd.sample(range(45, size - 45), n)

		self.grid = np.zeros((size, size))

		self.terrain = np.zeros((size, size))
		self.water = np.zeros((size, size))
		self.peat_bog = np.zeros((size, size))
		self.nutrients = np.zeros((size, size))

		self.flow = 0

		self.river_layer = 0
		self.river_end = 0

		self.p_branch = p_branch
		self.p_direct = p_direct

		self.mu = 0.01          # viscosity
		self.gamma = 0.01       # gradient of nutrients concentration
		self.rho = 0.01         # proportionality coefficient

	def terrain_height(self):
		"""
		According to the paper, the terrain is slightly inclined (the slope is 0.05%) and rough
		p. 1443: "we start from a flat and slanted landscape"
		"""
		terrain = self.terrain
		terrain[0] = np.ones(100)

		for i in range(self.size - 1):
			terrain[i + 1] = terrain[i] * rd.uniform(0.999, 0.9999)

		self.terrain = terrain
		return self.terrain

	def initiate_river(self):
		"""
		Initiate river in the middle of the grid
		"""
		river = np.zeros((100, 100))

		for i in range(self.size):
			river[i, 50] = 1

		return river

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

	def supply_water(self):
		"""
		add water to initial starting points and fill up at each iteration
		"""

		pass

	def remove_water(self):
		"""
		remove water from the outlet
		"""

		pass

	def calculate_flow(self):

		return self.flow

	def update_water(self):

		for i in range(self.size):
			for j in range(self.size):
				self.water = self.water + self.flow

		return self.water

	def distribute_nutrients(self):

		for i in range(self.size):
			for j in range(self.size):
				nutrients_neighbors = self.moore_neighborhood(self.nutrients, i, j)
				if self.water[i, j] > 0:
					self.nutrients[i, j] = 1.0
				elif self.nutrients[i, j] < max(nutrients_neighbors):
					self.nutrients = self.gamma * max(nutrients_neighbors)

		return self.nutrients

	def update_peatbog(self):

		for i in range(self.size):
			for j in range(self.size):
				if self.water[i, j] == 0:
					self.peat_bog[i, j] = self.peat_bog[i, j] + self.rho * self.nutrients[i, j]

		return self.peat_bog

	def update_terrain(self):

		for i in range(self.size):
			for j in range(self.size):
				if self.water[i, j] > 0:
					self.terrain[i, j] = self.terrain[i, j] + self.mu * self.water[i, j]

		return self.terrain

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

	def water_height(self):
		"""
		Similar approach as above, but water height increases
		"""
		water = self.water
		water[0] = np.ones(100) * rd.uniform(0.08, 0.12)

		for i in range(self.size - 1):
			for j in range(self.size - 1):
				if water[i, j + 1] and water[i, j - 1]:
					mean = (water[i, j - 1] + water[i, j] + water[i, j + 1]) / 3
					water[i + 1, j] = mean * rd.uniform(1.001, 1.005)
				if water[i, j + 1] and not water[i, j - 1]:
					mean = (water[i, j] + water[i, j + 1]) / 2
					water[i + 1, j] = mean * rd.uniform(1.001, 1.005)
				if water[i, j - 1] and not water[i, j + 1]:
					mean = (water[i, j] + water[i, j - 1]) / 2
					water[i + 1, j] = mean * rd.uniform(1.001, 1.005)

		self.water = water
		return self.water

	def total_height(self):
		"""
		Sum of the terrain height and water height
		"""
		total_height = np.zeros((self.size, self.size))

		for i in range(self.size):
			for j in range(self.size):
				total_height[i, j] = self.terrain[i, j] + self.water[i, j]

		return total_height


if __name__ == "__main__":
	rv = River(100, 1)
	rv.calculate_flow()
	for i in range(99):
		rv.generate_river()

	terrain = rv.terrain_height()
	water = rv.water_height()

	fig, axes = plt.subplots(1, 3)
	sns.heatmap(terrain[:, 0:99], cmap="BrBG_r", vmin=0.85, vmax=1.005, ax=axes[0])
	sns.heatmap(water[:, 0:99], cmap="Blues", ax=axes[1])
	plt.show()



	# plt.imshow(rv.grid)
	# plt.show()
