def initialize_terrain(self):
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
		(0, int(self.size / 2)),
		(5, 12),
		(7, 40),
		(1, 60),
		(1, 135),
		(5, 150),
		(5, 170),
		(7, 185),
		(1, 195),
		(28, 150),
		(33, 115),
		(20, 70),
		(45, 80),
		(60, 110),
	]
	for hill_coord in hill_coords:
		terrain[hill_coord] = terrain[hill_coord] * 1.04  # rd.uniform(1.01, 1.04)

	for _ in range(2):

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