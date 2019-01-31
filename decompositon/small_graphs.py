from misc import parallel, timing
import decomposition
from decomposition import NotDecomposableError
import networkx as nx
from datetime import datetime

# analysis of graphs on small numbe rof vertices
# we generate all possible graphs on n vertices
# and check how many are odd decomposable

def powerset(iterable, chunk_size=10000):
    """
    Builds the power set of iterable
    :param iterable: base set
    :param chunk_size: size of chunks
    :return: generator of chunk_size lists consiting of subsets of base iterable
    """
    s = list(iterable)
    n = len(s)

    for i in range(0, 2 ** n, chunk_size):
        yield [{s[k] for k, x in enumerate(reversed(bin(j)[2:])) if x == "1"} for j in
               range(i, min(2 ** n, i + chunk_size))]


def create_graph(edges, nodes):
    """
    Creates a graph from edges and nodes
    """
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G


@timing
def check(n, p):
    chunk_size = 10000

    all_edges = {(i, j) for i in range(n) for j in range(i + 1, n)}  # all possible edges on n vertices
    power = powerset(all_edges, chunk_size)

    all = 2 ** len(all_edges)  # number of elements in powerset
    chunks = (all // chunk_size) + 1  # number of chunks in the powerset

    print(f"Running decomposition: N={n}, all={all}")

    def work(inp):
        sum = 0
        inp = map(lambda x: create_graph(x, range(n)), inp)
        for y in inp:
            # check if it has an isolated node
            try:
                d = decomposition.odd_decomposition(y)
                sum += 1
            except NotDecomposableError:
                pass
        return sum

    # compute the actual number of decomposable graphs
    # we use the helper function from misc, which uses joblib to run work in multiple threads
    # this also displays the progress bar using tqdm
    ok = sum(parallel(work, power, chunks))

    print(f"Results for N={n}: {ok} out of {all}, {100 * ok / all:.2f}%")
    print()
    return (ok, all)


import csv

if __name__ == "__main__":
    with open('../results/small_graphs.csv', 'w', newline='') as csvfile:
        columns = ["n", "decomposable", "all", "percentage", "time"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for i in range(3, 9):
            (ok, all), time = check(i, True)
            writer.writerow({"n": i, "decomposable": ok, "all": all, "percentage": ok / all * 100, "time": time})
            csvfile.flush()
