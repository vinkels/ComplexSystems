import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


D = nx.DiGraph(name="river_network")
# pos = nx.spring_layout(D)
# pos = {
#  '1': (75, 10),
#  '2': (80, 13),
#  '3': (85, 20),
#  '4': (95, 23),
#  '5': (86, 51),
#  '6': (89, 58),
#  '7': (91, 75),
#  '8': (85, 81),
#  '9': (71, 18),
#  '10': (74, 24),
#  '11': (71, 55),
#  '12': (66, 62),
#  '13': (60, 30),
#  '14': (58, 51),
#  '15': (50, 22),
#  '16': (40, 45),
#  '17': (35, 30),
#  '18': (25, 55),
#  '19': (15, 60),
# }

D.add_nodes_from(range(1, 20))
D.add_edges_from(
    [
        (1, 9),
        (2, 9),
        (3, 10),
        (4, 10),
        (9, 13),
        (10, 13),
        (13, 16),
        (15, 16),
        (16, 18),
        (17, 18),
        (5, 11),
        (6, 11),
        (7, 12),
        (8, 12),
        (11, 14),
        (12, 14),
        (14, 19),
        (18, 19),
    ]
)
labels = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "11",
    12: "12",
    13: "13",
    14: "14",
    15: "15",
    16: "16",
    17: "17",
    18: "18",
    19: "19",
}

nx.draw_spring(D, with_labels=labels, color='blue')
plt.show()


def plot_degree_dist(graph):
    degrees = [graph.degree(n) for n in graph.nodes()]
    plt.hist(degrees)
    plt.show()


plot_degree_dist(D)
