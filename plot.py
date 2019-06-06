import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


world = gpd.read_file('data/as_dir_15s_grid/as_dir_15s/as_dir_15s/as_riv_15s.shp')
print('read done')
print(list(world))
# world.plot()

# plt.savefig('world_map.png', dpi=300)