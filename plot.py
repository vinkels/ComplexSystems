import pandas as pd
import geopandas as gdp
import matplotlib.pyplot as plt

shape = gdp.read_file('/Users/DennisK/Desktop/as_riv_15s/as_riv_15s.shp')
shape.plot()
plt.show()
