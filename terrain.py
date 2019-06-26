def initialize_terrain(self):
	"""
	NEW: added "hills" to the terrain
	"""
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
		terrain[hill_coords] = terrain[hill_coords] * 1.2

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