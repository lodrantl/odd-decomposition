from misc import parallel, timing
import decomposition
from decomposition import NotDecomposableError
import networkx as nx
from datetime import datetime

# we generate random graphs on n vertices with m edges
# our goal is to find out how number of edges affects decomposability

@timing
def check(n):
    repeats = 10000

    max_edges = n * (n-1) // 2

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
    ok = parallel(work, range(max_edges+1), max_edges+1)

    return ok


import csv
from matplotlib import pyplot as plt
if __name__ == "__main__":
    ok, time = check(15)
    plt.plot([i/100 for i in ok])
    plt.show()
    # with open('../results/small_graphs.csv', 'w', newline='') as csvfile:
    #     columns = ["n", "decomposable", "all", "percentage", "time"]
    #     writer = csv.DictWriter(csvfile, fieldnames=columns)
    #     writer.writeheader()
    #     for i in range(3, 9):
    #         (ok, all), time = check(i, True)
    #         writer.writerow({"n": i, "decomposable": ok, "all": all, "percentage": ok / all * 100, "time": time})
    #         csvfile.flush()
