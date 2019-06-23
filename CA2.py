import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


class River:
    def __init__(self, size, n, p_branch=0.0, p_direct=0.5):
        self.n = n
        self.size = size

        self.starting_points = rd.sample(range(30, size - 30), n)

        self.grid = np.zeros((size, size))

        self.terrain = np.zeros((size, size))
        self.water = np.zeros((size, size))
        self.peat_bog = np.zeros((size, size))

        self.river_layer = 0
        self.river_end = 0

        self.p_branch = p_branch
        self.p_direct = p_direct

        self.ca = self.initiate_n_rivers(self.size, self.grid, self.n)

    def initiate_n_rivers(self, size, grid, n):
        """
		Initiate rivers

		"""
        grid[0, self.starting_points] = 1
        self.river_end = list(zip([0] * n, self.starting_points))
        return grid

    def supply_water(self):
        """
		add water to initial starting points

		"""
        pass

    def remover_water(self):
        pass

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

    def terrain_height(self):
        """
		According to the paper, the terrain is slightly inclined (the slope is 0.05%) and rough

		On plot, the height decreases approximately 5% in 100 steps

		"""
        terrain = self.terrain
        terrain[0] = np.ones(100) * rd.uniform(0.98, 1.02)

        for i in range(self.size - 1):
            for j in range(self.size - 1):
                if terrain[i, j + 1] and terrain[i, j - 1]:
                    mean = (terrain[i, j - 1] + terrain[i, j] + terrain[i, j + 1]) / 3
                    terrain[i + 1, j] = mean * rd.uniform(0.999, 1)
                if terrain[i, j + 1] and not terrain[i, j - 1]:
                    mean = (terrain[i, j] + terrain[i, j + 1]) / 2
                    terrain[i + 1, j] = mean * rd.uniform(0.999, 0.9999)
                if terrain[i, j - 1] and not terrain[i, j + 1]:
                    mean = (terrain[i, j] + terrain[i, j - 1]) / 2
                    terrain[i + 1, j] = mean * rd.uniform(0.999, 0.9999)

        self.terrain = terrain
        return self.terrain

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

    def peat_bog_height(self):
        pass

    def total_height(self):
        """
		Sum of the terrain height and water height

		"""
        total_height = np.zeros((self.size, self.size))

        for i in range(self.size):
            for j in range(self.size):
                total_height[i, j] = self.terrain[i, j] + self.water[i, j]

        return total_height

    def calculate_flow(self):
        """
		Find lower heights in Moore neighborbood to determine flow

		"""
        river = np.zeros((self.size, self.size))
        eliminate_from_calculation = set()
        include_to_calculation = set()

        h = self.total_height()
        for i in range(self.size - 1):
            for j in range(self.size - 1):

                if not h[i - 1, j]:
                    neighborhood = [
                        h[i, j - 1],
                        h[i, j + 1],
                        h[i + 1, j - 1],
                        h[i + 1, j],
                        h[i + 1, j + 1],
                    ]
                    print("hoi")
                    mean = sum(neighborhood) / len(neighborhood)
                    for n in neighborhood:
                        if n > mean:
                            eliminate_from_calculation.add(n)
                        else:
                            include_to_calculation.add(n)

                elif not h[i + 1, j]:
                    neighborhood = [
                        h[i, j - 1],
                        h[i, j + 1],
                        h[i - 1, j - 1],
                        h[i - 1, j],
                        h[i - 1, j + 1],
                    ]
                    print("hoi2")
                    mean = sum(neighborhood) / len(neighborhood)
                    for n in neighborhood:
                        if n > mean:
                            eliminate_from_calculation.add(n)
                        else:
                            include_to_calculation.add(n)


                elif not h[i, j - 1]:
                    neighborhood = [
                        h[i - 1, j],
                        h[i - 1, j + 1],
                        h[i, j + 1],
                        h[i + 1, j],
                        h[i + 1, j + 1],
                    ]
                    print("hoi3")
                    for n in neighborhood:
                        if n > mean:
                            eliminate_from_calculation.add(n)
                        else:
                            include_to_calculation.add(n)

                elif not h[i, j + 1]:
                    neighborhood = [
                        h[i - 1, j],
                        h[i - 1, j - 1],
                        h[i, j - 1],
                        h[i + 1, j],
                        h[i + 1, j - 1],
                    ]
                    print("hoi4")
                    for n in neighborhood:
                        if n > mean:
                            eliminate_from_calculation.add(n)
                        else:
                            include_to_calculation.add(n)

                else:
                    neighborhood = [
                        h[i - 1, j - 1],
                        h[i - 1, j],
                        h[i - 1, j + 1],
                        h[i, j - 1],
                        h[i, j + 1],
                        h[i + 1, j - 1],
                        h[i + 1, j],
                        h[i + 1, j + 1],
                    ]
                    print("hoi!!!!")
                    mean = sum(neighborhood) / len(neighborhood)
                    for n in neighborhood:
                        if n > mean:
                            eliminate_from_calculation.add(n)
                        else:
                            include_to_calculation.add(n)
                    for cell in include_to_calculation:
                        #TODO Update flow with local speed of cell  plus diff of avg speed and water level of cell
                        print(cell)


            return river

    def update_water(self):
	    pass

    def update_peatbog(self):
        """

		"""
        pass

    def update_terrain(self):
        """

		"""
        pass


# # draft:
# if __name__=="__main__":
# 	rv = River(100, 1)
# 	T = 100
# 	for t in T:
# 		rv.supply_water()
# 		rv.remover_water()
# 		rv.calculate_flow()
# 		rv.update_water()
#
#

if __name__ == "__main__":
    rv = River(100, 1)
    rv.calculate_flow()
    # for i in range(99):
    #     rv.generate_river()

    # terrain = rv.terrain_height()
    # water = rv.water_height()
    # total_height = rv.total_height()

    # fig, axes = plt.subplots(1, 3)
    # sns.heatmap(terrain[:, 0:99], cmap="BrBG_r", vmin=0.85, vmax=1.005, ax=axes[0])
    # sns.heatmap(water[:, 0:99], cmap="Blues", ax=axes[1])
    # sns.heatmap(total_height[:, 0:99], ax=axes[2])
    # plt.show()

    # plt.imshow(rv.grid)
    # plt.show()
