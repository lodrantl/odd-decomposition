from vendor.fieldmath import BinaryField, Matrix

import networkx as nx
import itertools
from collections import defaultdict
from typing import Set, List, Tuple, Iterable, Callable

bin_field = BinaryField(2)


class NotDecomposableError(ValueError):
    pass


def partition(items: Iterable, predicate: Callable) -> Tuple[List, List]:
    """
    :param items: iterable of items to split
    :param predicate: predicate to split by
    :return: a tuple of lists, first list does not satisfy the predicate, second list does
    """
    a, b = itertools.tee((predicate(item), item) for item in items)
    return ([item for pred, item in a if not pred],
            [item for pred, item in b if pred])


def is_odd(G) -> bool:
    """
    :return: true if all nodes in the graph have odd degree
    """
    return all([G.degree(x) % 2 == 1 for x in G.nodes()])


def even_nodes(G) -> Set:
    """
    :return: set of all even degree nodes in the graph
    """
    return {x for x in G.nodes() if G.degree(x) % 2 == 0}


def odd_nodes(G) -> Set:
    """
    :return: set of all even degree nodes in the graph
    """
    return {x for x in G.nodes() if G.degree(x) % 2 == 1}


def n_joining(G, U: Set[int], V: Set[int]) -> int:
    """
    :param U: first set of vertices
    :param V: second set vertices
    :return: number of edges between the sets
    """
    return sum([1 for x in U for u, v in G.edges(x) if v in V])


def T_join(G, T: Set[int]) -> Set[Tuple[int, int]]:
    """
    Computes a T-join for graph if it exists
    Throws a ValueError if such T-join does not exist
    :param T: set of vertices
    :param graph: graph on which to find the join
    :return: set of edges which are part of the join
    """
    edge_count = defaultdict(int)
    components = nx.connected_components(G)

    # analyse every connected component on its own
    for c in components:
        Ti = T.intersection(c)

        # required and sufficient condition for existence of the T-join
        if len(Ti) % 2 == 1:
            raise ValueError("T-join does not exist for odd intersections of T")

        while Ti:
            # pop vertices 2 by 2 and find a simple path between them
            x, y = Ti.pop(), Ti.pop()
            path = next(nx.all_simple_paths(G, x, y))
            # count how many times each edge is used
            for i, j in zip(path[:-1], path[1:]):
                edge_count[(min(i, j), max(i, j), 0)] += 1

    return {e for e, count in edge_count.items() if count % 2 == 1}


def odd_decomposition(G) -> Tuple[Set[int], Set[int]]:
    """
    Try to decompose a graph into two subgraphs of odd degree.

    Throws NotDecomposableError if the graph is not odd decomposable

    :param graph: graph to decompose
    :return: a tuple of lists, each consisting of edges of the subgraphs
    """
    multi = isinstance(G, nx.MultiGraph)

    # create a MultiGraph copy of G
    G = nx.MultiGraph(G)

    # remove isolated nodes from the graph, since they are irrelevant
    G.remove_nodes_from(list(nx.isolates(G)))

    # if the base graph is already odd
    if is_odd(G):
        return (set(G.edges(keys=multi)), set())

    odd_subgraph = G.subgraph(odd_nodes(G))
    even_subgraph = G.subgraph(even_nodes(G))

    odd_components = nx.connected_components(odd_subgraph)
    even_components = nx.connected_components(even_subgraph)

    # use the same notation as in our source paper
    X = list(odd_components)
    Y, Z = partition(even_components, lambda x: len(x) % 2 == 0)

    lX, lY, lZ = len(X), len(Y), len(Z)
    linear_system = Matrix(lY + lZ, lX + 1, bin_field)

    # create a linear system over GF(2) as described in our source paper
    for i, Yi in enumerate(Y):
        for j, Xi in enumerate(X):
            if n_joining(G, Xi, Yi) % 2 == 1:
                linear_system.set(i, j, 1)
            else:
                linear_system.set(i, j, 0)
        linear_system.set(i, lX, 1)

    for i, Zi in enumerate(Z):
        for j, Xi in enumerate(X):
            if n_joining(G, Xi, Zi) % 2 == 1:
                linear_system.set(i + lY, j, 1)
            else:
                linear_system.set(i + lY, j, 0)
        linear_system.set(i + lY, lX, 0)

    # transform the system into RREF
    linear_system.reduced_row_echelon_form()
    red = set()

    # we only need one solution
    # every non pivot is set to 0 (meaning blue)
    # while every pivot matches the augmented value
    # only create the red set since this is the only one we need

    for i in range(lY + lZ):
        val = linear_system.get(i, lX)
        # don't cross the last column (augmented part)
        for j in range(lX):
            v = linear_system.get(i, j)
            if v == 1:
                if val == 1:
                    red.add(j)
                break
        else:
            if val == 1:
                # if any of the lines has no pivot and 1 as the augmented value this system is not solvable
                raise NotDecomposableError("The graph is not decomposable due to unsolvable system")
            else:
                # this is a zero row ane there are no pivots after this row
                break

    red_nodes = set.union(*[X[i] for i in red]) if red else set()
    # edges adjacent to red nodes
    red_edges = set(G.edges(nbunch=red_nodes, keys=True))
    # calculate the red degree for every even node
    degrees = dict()
    for i in even_subgraph.nodes():
        degrees[i] = 0

    for i, j, k in red_edges:
        if i in degrees:
            degrees[i] += 1
        if j in degrees:
            degrees[j] += 1

    # T set is the set of all nodes of even red degree
    T = {i for i, deg in degrees.items() if deg % 2 == 0}

    # compute the T-join and mark the nodes as red/blue
    red_join = T_join(even_subgraph, T)

    red_edges.update(red_join)
    blue_edges = set(G.edges(keys=True)).difference(red_edges)

    if not multi:
        red_edges = {(i, j) for i, j, k in red_edges}
        blue_edges = {(i, j) for i, j, k in blue_edges}

    return (red_edges, blue_edges)
