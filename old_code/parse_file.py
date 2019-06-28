import maya
import pandas as pd
import scipy as sc
import networkx as nx
import matplotlib.pyplot as plt


def parse_data():
    year_data = {}
    with open('data/dv.txt', 'r') as txt_file:
        for line in txt_file:
            if line.startswith('USGS'):
                new_line = line.strip('\n').split('	')
                if 'P' not in new_line[-1]:
                    year = new_line[2][:4]
                    dm = new_line[2][5:7] + new_line[2][8:]
                    if '0229' not in dm and year not in ('2019', '2018', '1861', '1862'):
                        if year not in year_data:
                            year_data[year] = {}
                        year_data[year][dm] = int(new_line[3])

    df = pd.DataFrame(year_data)
    df['mmdd'] = df.index
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":

    df_cor = df.drop(columns=['mmdd']).corr(method='pearson', min_periods=1)
    network_df = nx.from_pandas_adjacency(df_cor, create_using=None)
    # nx.draw_spring(network_df)
    # plt.show()

    thresh_vals = [0.3, 0.4, 0.5, 0.6, 0.65, 0.7,0.75]
    df_cor_clean = df_cor.copy()
    df_cor_clean[df_cor_clean < 0.4] = 0

    network_df = nx.from_pandas_adjacency(df_cor_clean, create_using=None)
    # pos = nx.spring_layout(network_df,scale=2)

    # nx.draw(G,pos,font_size=8)
    # plt.show()

    # G = nx.path_graph(4)
    pos = nx.spring_layout(network_df) 
    # default to scale=1
    # nx.draw(network_df, pos)
    pos = nx.spring_layout(network_df, scale=3) 
    # pos = nx.DiGraph(network_df) # double distance between all nodes
    nx.draw(network_df, node_size=1, width=0.5)
    plt.savefig('plots/test_plot.png',dpi=300)