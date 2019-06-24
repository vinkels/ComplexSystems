import numpy as np
import matplotlib.pyplot as plt
import random as rd


class River:
	def __init__(self, ca_size, n, p_branch=0.0, p_direct=0.5):
		self.ca_size = ca_size
		self.n = n
		self.river_layer = 0
		self.ca = self.make_rivers(self.ca_size, self.n)
		self.p_branch = p_branch
		self.p_direct = p_direct

	def make_rivers(self, ca_size, n):

		ca = np.zeros((ca_size + 1, ca_size + 1))
		river_starts = rd.sample(
			range(int(ca_size * 0.2), ca_size - int(ca_size * 0.2)), n
		)
		ca[0, river_starts] = 1
		river_list = list(zip([0] * n, river_starts))
		self.river_end = {key: rd.choice([-1, 1]) for key in river_list}
		print(self.river_end)
		return ca

	def build_directions(self):

		direct = [-1, 1]
		self.river_layer += 1
		new_ends, new_directs = [], []
		for end in self.river_end:

			print("end", end)
			if rd.random() < self.p_branch:
				print("kom ik hier")
				# self.ca[self.river_layer, [(end[1] - 1), (end[1] + 1)]] = 1
				new_ends += [
					(self.river_layer, end[1] - 1),
					(self.river_layer, end[1] + 1),
				]
				new_directs += [-1, 1]
			else:
				new_x = self.river_end[end]
				if rd.random() < self.p_direct:
					new_x = -new_x

				# self.ca[(self.river_layer, end[1] + new_x)] = 1
				new_ends += [(self.river_layer, end[1] + new_x)]
				new_directs += [new_x]
			print("new ends", new_ends)

		new_river_ends = {
			end: new_directs[i]
			for i, end in enumerate(new_ends)
			if 0 < end[1] < self.ca_size - 1
		}
		for coor in new_river_ends:
			self.ca[coor] = 1
		self.river_end = new_river_ends
		return new_river_ends

	def build_river(self):
		new_river_end = []
		self.river_layer += 1
		for val in self.river_end:
			branch = 1
			if rd.random() < self.p_branch:
				self.p_branch -= 0.01
				branch = 2
			if val[1] >= self.ca_size - 1:
				direct = rd.sample([-1, 0], branch)
			elif val[1] <= 0:
				direct = rd.sample([0, 1], branch)
			else:
				direct = rd.sample([-1, 1], branch)
			for coor in direct:
				x, y = self.river_layer, (val[1] + coor)
				self.ca[(x, y)] = 1
				new_river_end.append((x, y))
		self.river_end = new_river_end
		return new_river_end


if __name__ == "__main__":
	rv = River(100, 1, 0.2, 0.3)
	for i in range(99):
		rv.build_directions()
	plt.imshow(rv.ca)
	plt.show()
	# plt.savefig('testyyy.png', dpi=1000)
