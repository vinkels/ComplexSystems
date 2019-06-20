import pandas as pd
import geopandas as gdp
import matplotlib.pyplot as plt
import networkx as nx
# import pysal

shape = gdp.read_file('NLD_wat/NLD_water_lines_dcw.shp')
shape.plot()
plt.savefig('water.png',dpi=300)

# # G=nx.read_shp('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp') 
# # nx.draw(G, with_labels=False)
# # plt.savefig('rivers.png')

# #build contiguity matrix - uses rook contiguity - queen is available
# # path_to_shp = r'bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp'
# # my_keys = 'name_of_id_for_your_features'
# # # contig_matrix = pysal.weights.Rook.from_shapefile(path_to_shp,idVariable = my_keys)
# # contig_matrix = pysal.weights.Rook.from_shapefile(path_to_shp)

# # #build list of edges - this will create edges going both ways from connected nodes, so you might need to remove duplicates
# # nodes = contig_matrix.weights.keys() # to get dict of keys, alternatively use contig_matrix.id2i.keys()
# # edges = [(node,neighbour) for node in nodes for neighbour in contig_matrix[node]]
# # my_graph = nx.Graph(edges)

# import fiona
# from shapely.geometry import shape
# import networkx as nx

# # Converts a shapefile located at indir/infile to a networkx graph.
# # If draw_graph is set to True, the graph is drawn using matplotlib.
# # def create_graph(infile, draw_shapefile=False, draw_graph=False):
# #     G = nx.Graph()
# #     i = 1

# # #   with cd(indir):
# #     with fiona.open(infile) as blocks:
# #         for shp in blocks:
# #             # the geometry property here may be specific to my shapefile
# #             block = shape(shp['geometry'])

# #             G.add_node(i)
# #             i += 1

# #     for n in G.nodes(data=True):
# #         state = n[1]['block']
# #         for o in G.nodes(data=True):
# #             other = o[1]['block']
# #             if state is not other and state.touches(other):
# #                 G.add_edge(n[0], o[0])

# #     return G

# # create_graph('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp', draw_graph=True)

# from shapely.geometry import shape
# from shapely.ops import unary_union
# import fiona
# import itertools
# # create a Graph
# import networkx as nx

# # geoms =[shape(feature['geometry']) for feature in fiona.open('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp')]
# geoms = []
# geo_count = 0
# for feature in fiona.open('bgd_hyd_rivers_lged/bgd_hyd_rivers_lged.shp'):
#     geoms.append(shape(feature['geometry']))
#     geo_count += 1
#     if geo_count % 100 == 0:
#         print(geo_count)


# # G = nx.Graph()
# # for line in geoms:
# #    for seg_start, seg_end in itertools.izip(list(line.coords),list(line.coords)[1:]):
# #     G.add_edge(seg_start, seg_end)

    
# res = unary_union(geoms)
# print('kom ik hier')
# G = nx.Graph()
# print('en hier')
# n_edges = 0
# for line in res:
#     for seg_start, seg_end in itertools.izip(list(line.coords),list(line.coords)[1:]):
#         G.add_edge(seg_start, seg_end) 
#         n_edges += 1
#         if n_edges % 100 == 0:
#             print(n_edges)


# nx.draw(G)
# plt.show()