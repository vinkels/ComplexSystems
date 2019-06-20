import numpy as np
import matplotlib.pyplot as plt
import random as rd

class river:
    def __init__(self, ca_size, n):
        self.ca_size = ca_size
        self.n = n
        self.ca = self.make_rivers(self.ca_size, self.n)
        self.river_layer = 0

    def make_rivers(self, ca_size, n):

        ca = np.zeros((ca_size, ca_size))
        river_starts = rd.sample(range(0, ca_size - 1), n)
        ca[0, river_starts] = 1
        self.river_end = list(zip([0]*n, river_starts))
        return ca


    def build_river(self):
        
        new_river_end = []
        self.river_layer += 1
        for val in self.river_end:
            if val[1] == self.ca_size - 1:
                direct = rd.randint(-1,0)
            elif val[1] == 0:
                direct = rd.randint(0,1)
            else:
                direct = rd.randint(-1, 1)
            x, y = self.river_layer, (val[1] + direct)
            self.ca[(x, y)] = 1
            new_river_end.append((x, y))
        self.river_end = new_river_end
        return new_river_end

if __name__ == "__main__":
    rv = river(100, 4)
    for i in range(99):
        rv.build_river()

    plt.imshow(rv.ca)
    plt.savefig('testyyy.png')
