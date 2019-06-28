import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
test_tree = nx.generators.trees.random_tree(100)
nx.draw(test_tree)
plt.show()
