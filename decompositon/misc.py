from joblib import Parallel, delayed
from tqdm import tqdm
import time
from typing import Iterable
import networkx as nx
import matplotlib.pyplot as plt


def parallel(function, input: Iterable, total: int, cores: int = 4):
    """
    Helper  function
    :param function: funkcija, ki jo bomo izvajali
    :param input: iterable kosov na katerih bomo izvajali funkcijo
    :param total: dolžina input
    :param cores: število fork procesov
    :return:
    """
    if cores > 0:
        p = Parallel(n_jobs=cores)(delayed(function)(x) for x in tqdm(input, total=total))
    else:
        p = [function(x) for x in tqdm(input, total=total)]
    return p


def timing(f):
    """
    Decorator za funkcije. Ob koncu izvajanja izpiše kako dolgo je funkcija trajala
    """

    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))

        return ret, time2 - time1

    return wrap


def draw_graph(G, red, blue, pos = None):
    G = nx.MultiGraph(G)

    if pos == None:
        pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_color='black')

    # edges
    nx.draw_networkx_edges(G, pos,
                           edgelist=red,
                           width=8, alpha=0.5, edge_color='r')
    nx.draw_networkx_edges(G, pos,
                           edgelist=blue,
                           width=8, alpha=0.5, edge_color='b')

    plt.axis('off')
    #plt.savefig("labels_and_colors.png")  # save as png
    plt.show()  # display
