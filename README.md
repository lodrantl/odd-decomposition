Odd decomposition
-----------------

We call a graph odd, if all its vertices have an odd degree. Some graphs can be decomposed
into two odd subgraphs. In this module we have implemented
a polnomyial algorithm to check if such a decomposition exists.

#### Layout:
* decomposition/
    * decomposition.py - main decomposition algorithm, patches nx.Graph
    * misc.py - misc functions used in other scripts
    * small_graphs.py - analysis of small graphs
    * vendor/
        * fieldmath.py - Gauss-Jordan elimination over any field
* report/ - LaTex report of this project
* requirements.txt - required Python 3 libraries

#### Usage:

    from decomposition.decomposition import MonkeyGraph
    G = MonkeyGraph()
    G.add_nodes_from(range(5))
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    G.add_edge(0, 3)
    G.add_edge(3, 4)
    G.add_edge(3, 5)
    G.add_edge(3, 6)
    G.add_edge(5, 6)
    red, blue = G.odd_decomposition()
    