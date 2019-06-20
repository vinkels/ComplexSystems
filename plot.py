import pandas as pd
import geopandas as gdp
import matplotlib.pyplot as plt
import networkx as nx

shape = gdp.read_file('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp')
shape.plot()
plt.show()
#
# G=nx.read_shp('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp')
# nx.draw(G, with_labels=False)
# plt.show()
