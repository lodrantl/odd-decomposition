from vendor.fieldmath import *
import networkx as nx
from networkx import Graph
import itertools
from collections import defaultdict
import matplotlib.pyplot as plt

bin_field = BinaryField(2)


class MonkeyGraph(nx.Graph):
    # monkey patch Graphs
    def is_odd(self):
        return all([self.degree(x) % 2 == 1 for x in self.nodes()])

    def even_nodes(self):
        return {x for x in self.nodes() if self.degree(x) % 2 == 0}

    def odd_nodes(self):
        return {x for x in self.nodes() if self.degree(x) % 2 == 1}

    def n_joining(self, U, V):
        n = 0
        for x in U:
            for y in self.neighbors(x):
                if (y in V):
                    n = n + 1
        return n


Graph.is_odd = MonkeyGraph.is_odd
Graph.even_nodes = MonkeyGraph.even_nodes
Graph.odd_nodes = MonkeyGraph.odd_nodes
Graph.n_joining = MonkeyGraph.n_joining

p = Graph()
p.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
p.add_edge(1, 5)
p.add_edge(5, 2)
p.add_edge(3, 4)
p.add_edge(4, 7)
p.add_edge(6, 7)
p.add_edge(5, 7)
p.add_edge(7, 3)

nx.draw(p)


# plt.show()
def partition(items, predicate=bool):
    a, b = itertools.tee((predicate(item), item) for item in items)
    return ([item for pred, item in a if not pred],
            [item for pred, item in b if pred])


def odd_decomposition(graph: Graph):
    odd_subgraph = graph.subgraph(graph.odd_nodes())
    even_subgraph = graph.subgraph(graph.even_nodes())

    odd_components = nx.connected_components(odd_subgraph)
    even_components = nx.connected_components(even_subgraph)

    X = list(odd_components)
    Y, Z = partition(even_components, lambda x: len(x) % 2 == 0)

    lX, lY, lZ = len(X), len(Y), len(Z)
    print("X:", X, "Y:", Y, "Z:", Z)

    sistem = Matrix(lY + lZ, lX + 1, bin_field)

    for i, Yi in enumerate(Y):
        for j, Xi in enumerate(X):
            if graph.n_joining(Xi, Yi) % 2 == 1:
                sistem.set(i, j, 1)
            else:
                sistem.set(i, j, 0)
        sistem.set(i, lX, 1)

    for i, Zi in enumerate(Z):
        for j, Xi in enumerate(X):
            if graph.n_joining(Xi, Zi) % 2 == 1:
                sistem.set(i + lY, j, 1)
            else:
                sistem.set(i + lY, j, 0)
        sistem.set(i + lY, lX, 0)

    print(sistem)
    sistem.reduced_row_echelon_form()
    print(sistem)

    red = set()

    for i in range(lY + lZ):
        val = sistem.get(i, lX)
        for j in range(lX):
            v = sistem.get(i, j)
            if v == 1:
                if val == 1:
                    red.add(j)
                break
        else:
            if val == 1:
                print("broken system")
                return False

    red_nodes = set()
    red_edges = set()

    for i in red:
        red_nodes.update(X[i])

    red_edges.update(graph.edges(nbunch=red_nodes))

    print("Edge Red:", red_edges)
    print("Node Red:", red_nodes)

    degrees = dict()
    for i in even_subgraph.nodes():
        degrees[i] = 0

    for i, j in red_edges:
        if i in degrees:
            degrees[i] += 1
        if j in degrees:
            degrees[j] += 1

    T = set()
    print(degrees)
    for i, deg in degrees.items():
        print(i, deg)
        if deg % 2 == 0:
            T.add(i)

    red_join = T_join(T, even_subgraph)
    print(red_join)
    red_edges.update(red_join)
    blue_edges = set(graph.edges()).difference(red_edges)
    print("Red:", red_edges, "Blue:", blue_edges)

    return True

def T_join(T, graph):
    edges = defaultdict(int)
    comps = nx.connected_components(graph)
    for comp in comps:
        Ti = T.intersection(comp)
        if len(Ti) % 2 == 1:
            raise ValueError("T-join does not exist for odd intersections of T")
        while Ti:
            x, y = Ti.pop(), Ti.pop()
            path = next(nx.all_simple_paths(graph, x, y))
            for i, j in zip(path[:-1], path[1:]):
                edges[(min(i, j), max(i,j))] += 1

    return {e for e, count in edges.items() if count % 2 == 1}








odd_decomposition(p)
