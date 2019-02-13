from misc import parallel, timing, draw_graph
import decomposition
from decomposition import NotDecomposableError
import networkx as nx
from datetime import datetime
from tqdm import tqdm

# we generate random graphs on n vertices probability 0.7 for each edge
# our goal is to find out how number of vertices affects execution time

@timing
def check(n):
    repeats = 100

    ok = 0
    for i in range(repeats):
        G = nx.gnp_random_graph(n, 0.7)
        try:
            d = decomposition.odd_decomposition(G)
            ok += 1
        except NotDecomposableError:
            pass
    return ok

import csv

if __name__ == "__main__":
    with open('../results/timed.csv', 'w', newline='') as csvfile:
        columns = ["n", "m", "percentage", "time", "avgtime"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for i in tqdm(range(5, 1000, 10)):
            ok,  time = check(i)
            writer.writerow({"n": i, "percentage": ok, "time": time, "avgtime": time / 100})
            csvfile.flush()
