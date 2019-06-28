import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import networkx as nx
import heapq
from collections import OrderedDict

def read_in_data(path='data/data_complex_systems/pickles/'):

    slopes = [0.0001,0.0002,0.0004,0.0006,0.0008,0.001]
    dict_of_split= {}
    dict_of_segment = {}
    for i in range(1,31):
        count = 0
        for s in slopes:
            count += 1
            name_split = ('splits_slope_' + str(s) +'version' + str(i) +'.p')
            name_segm = ('segements_slope_' + str(s) +'version' + str(i) +'.p')
            with open(path+name_split, 'rb') as f:
                data_split = pkl.load(f)
                dict_of_split[str(count)] = data_split
            with open(path+name_segm, 'rb') as g:
                data_segment = pkl.load(g)
                dict_of_segment[str(count)] = data_segment
    return dict_of_split, dict_of_segment



data_split = pkl.load(open('data/data_complex_systems/pickles/splits_slope_0.0001_version_1.p', 'rb'))

data_segment = pkl.load(open('data/data_complex_systems/pickles/segments_slope_0.0001_version_1.p', 'rb'))

def process_data(split, segment, labelling= False):

    if labelling:
        labels = OrderedDict()
        values = range(len(segment))
        for e, i in enumerate(values):
            labels[str(e)] = i
        return labels

    for k, v in segment.items():
        segment[k] = len(v)
    split_dict = {}
    for k, v in split.items():
        split_dict[int(k)] = (int(v[0]), int(v[1]))

    return split_dict, segment

def create_network(split, segment):

    g= nx.DiGraph(split)
    edgie = g.edges()
    for k, v in split_dict.items():
        for ed in edgie:
            if k == ed[0]:
                g[k][ed[1]]['weights'] = data_segment[k] * 1/len(segment)
    return g

def visualise_network(graph, it, labels, save =False):
    plt.figure()
    nx.draw(graph, with_labels=labels)
    if save:
        plt.savefig('network_'+str(it)+'.png', dpi=300)
    plt.show()


def calc_order_array(D):

    if nx.is_directed_acyclic_graph(D) == False:
        raise('Input should be a directed acyclic graph sukkel')

    order_array = np.zeros(nx.number_of_nodes(D))

    for i in range(nx.number_of_nodes(D)-1,-1,-1):
        if len(nx.descendants(D,i)) == 0 or len(nx.descendants(D,i)) == 1:
            order_array[i] = 1
        else:
            des_list = list(D.successors(i))
            des_list = [int(h) for h in des_list]
            max_orders = heapq.nlargest(2, order_array[des_list])

            if len(max_orders) == 1:
                order_array[i] = max_orders[0]

            else:

                if max_orders[0] == max_orders[1]:
                    order_array[i] = max_orders[0] + 1
                else:
                    order_array[i] = max_orders[0]
    return order_array


def calc_bifcation_ratio(order_arr):

    if len(order_arr) < 1.0:
        R_b = 0
    else:
        R_i = int(max(order_arr) - 1)
        R_b = np.zeros(R_i)

        for i in range(R_i):
#             print("Test ",i , " ", order_arr == i + 1)
            R_b[i] = sum(order_arr == i + 1)/sum(order_arr == i + 2)
    return R_b



def calc_len_ratio(order_arr, segm_dict):

    length_node_list = segm_dict.values()
    length_order_set_list = list(zip(order_arr, length_node_list))

    R_l = []
    avg_len_path_dict = {}

    for order, length in length_order_set_list:
        if order not in avg_len_path_dict:
            avg_len_path_dict[order] = [length]
        else:
            avg_len_path_dict[order].append(length)

    for key, value in avg_len_path_dict.items():
        avg_len_path_dict[key] = sum(value)/len(value)

    for i in range(1, len(avg_len_path_dict)):
        R_l.append(avg_len_path_dict[i + 1]/avg_len_path_dict[i])
    return R_l



def calc_fractal_dim(ratio_bifcation, ratio_length):
    return sum(np.log(ratio_bifcation)/np.log(ratio_length))

o_array = calc_order_array(g)
r_b = calc_bifcation_ratio(o_array)
r_l = calc_len_ratio(o_array, data_segment)
print(calc_fractal_dim(r_b, r_l))

# slopes = [0.0001,0.0002,0.0004,0.0006,0.0008,0.001]
# rb=np.zeros(30,3)
# for i in range(1,31):
#     count = 0
#     for s in slopes:
#         count += 1
#         name = ('splits_slope_' + str(s) +'version' + str(i) +'.p')
#         data_split = pkl.load(open(name, 'rb'))
#         Graph = nx.DiGraph(data_split)
#         ##rb[count] = calc_Rb(Graph)[0]

def stats_bifurcation_ratio():
    pass

def stats_path_length_ratio():
    pass

def stats_fractal_dim():
    pass


