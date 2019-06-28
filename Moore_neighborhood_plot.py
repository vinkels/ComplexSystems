import numpy as np
import random as rd
import seaborn as sns
import matplotlib.pyplot as plt


def moore_neighborhood(size, grid, i, j):
    if i == 0 and j == 0:
        neighborhood = [grid[i + 1, j + 1], grid[i, j + 1], grid[i + 1, j]]
        locations = [[i + 1, j + 1], [i, j + 1], [i + 1, j]]

    elif i == 0 and j == (size - 1):
        neighborhood = [grid[i, j - 1], grid[i + 1, j - 1], grid[i + 1, j]]
        locations = [[i, j - 1], [i + 1, j - 1], [i + 1, j]]

    elif i == 0 and 0 < j < (size - 1):
        neighborhood = [
            grid[i, j - 1],
            grid[i, j + 1],
            grid[i + 1, j - 1],
            grid[i + 1, j],
            grid[i + 1, j + 1],
        ]
        locations = [[i, j - 1], [i, j + 1], [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]

    elif i == (size - 1) and j == 0:
        neighborhood = [grid[i, j + 1], grid[i - 1, j + 1], grid[i - 1, j]]
        locations = [[i, j + 1], [i - 1, j + 1], [i - 1, j]]

    elif i == (size - 1) and j == (size - 1):
        neighborhood = [grid[i - 1, j - 1], grid[i, j - 1], grid[i - 1, j]]
        locations = [[i - 1, j - 1], [i, j - 1], [i - 1, j]]

    elif i == (size - 1) and 0 < j < (size - 1):
        neighborhood = [
            grid[i, j - 1],
            grid[i, j + 1],
            grid[i - 1, j - 1],
            grid[i - 1, j],
            grid[i - 1, j + 1],
        ]
        locations = [[i, j - 1], [i, j + 1], [i - 1, j - 1], [i - 1, j], [i - 1, j + 1]]

    elif 0 < i < (size - 1) and j == 0:
        neighborhood = [
            grid[i - 1, j],
            grid[i - 1, j + 1],
            grid[i, j + 1],
            grid[i + 1, j],
            grid[i + 1, j + 1],
        ]
        locations = [[i - 1, j], [i - 1, j + 1], [i, j + 1], [i + 1, j], [i + 1, j + 1]]

    elif 0 < i < (size - 1) and j == (size - 1):
        neighborhood = [
            grid[i - 1, j],
            grid[i - 1, j - 1],
            grid[i, j - 1],
            grid[i + 1, j],
            grid[i + 1, j - 1],
        ]
        locations = [[i - 1, j], [i - 1, j - 1], [i, j - 1], [i + 1, j], [i + 1, j - 1]]

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


matrix = np.zeros((7, 7))
neighborhood, locations = moore_neighborhood(7, matrix, 3, 3)

for location in locations:
    location = tuple(location)
    matrix[location] = 1

matrix[3, 3] = 2

sns.heatmap(matrix, linewidths=.5, cmap="YlGnBu_r")
plt.savefig(f'Moore_neighborhood.png', dpi=300)
plt.show()
