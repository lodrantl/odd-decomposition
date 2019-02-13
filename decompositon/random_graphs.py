from misc import parallel, timing, draw_graph
import decomposition
from decomposition import NotDecomposableError
import networkx as nx
from datetime import datetime


# we generate random graphs on n vertices with m edges
# our goal is to find out how number of edges affects decomposability

@timing
def check(n):
    repeats = 500

    max_edges = n * (n - 1) // 2

    print(f"Running decomposition: N={n}")

    def work(m):
        ok = 0
        for i in range(repeats):
            G = nx.gnm_random_graph(n, m)
            try:
                d = decomposition.odd_decomposition(G)
                ok += 1
            except NotDecomposableError:
                pass
        return ok

    # compute the actual number of decomposable graphs
    # we use the helper function from misc, which uses joblib to run work in multiple threads
    # this also displays the progress bar using tqdm
    ok = parallel(work, range(max_edges + 1), max_edges + 1)

    return ok, max_edges


import csv
from matplotlib import pyplot as plt

if __name__ == "__main__":
    with open('../results/random_graphs.csv', 'w', newline='') as csvfile:
        columns = ["n", "m", "percentage", "time"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for i in [20, 21, 22, 23]:
            (ok, all), time = check(i)
            for m, k in enumerate(ok):
                writer.writerow({"n": i, "m" : m, "percentage": k, "time": time})
            csvfile.flush()
