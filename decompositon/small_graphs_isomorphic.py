from misc import parallel, timing
import decomposition
from decomposition import NotDecomposableError
import networkx as nx
from datetime import datetime

# analysis of graphs on small number of vertices
# we only check each isomorphic group for odd decompose once
# data comes from http://users.cecs.anu.edu.au/~bdm/data/graphs.html

def chunk_generator(f, chunk_size, all):
    """
    We can afford to read it into ram (uses around 1gb of ram of n=10.

    We still chunk it up for faster use in parallel processing.
    """
    lines = f.read().splitlines()
    chunks = (all // chunk_size) + 1

    for i in range(chunks):
        yield lines[chunk_size*i:chunk_size*(i+1)]

@timing
def check(n, p):
    chunk_size = 10000
    fname = f"isomorphic_graphs/graph{n}.g6"
    all = 0
    with open(fname, "r") as f:
        for line in f:
            all += 1
    chunks = (all // chunk_size) + 1

    with open(fname, "r") as f:
        print(f"Running decomposition: N={n}, all={all}")

        def work(inp):
            sum = 0
            for y in inp:
                # check if it has an isolated node
                try:
                    G = nx.from_graph6_bytes(bytes(y.rstrip("\n"), "ascii"))
                    d = decomposition.odd_decomposition(G)
                    sum += 1
                except NotDecomposableError:
                    pass
            return sum

        # compute the actual number of decomposable graphs
        # we use the helper function from misc, which uses joblib to run work in multiple threads
        # this also displays the progress bar using tqdm
        ok = sum(parallel(work, chunk_generator(f, chunk_size, all), chunks))

        print(f"Results for N={n}: {ok} out of {all}, {100 * ok / all:.2f}%")
        print()
        return (ok, all)


import csv

if __name__ == "__main__":
    with open('../results/small_graphs_isomorphic.csv', 'w', newline='') as csvfile:
        columns = ["n", "decomposable", "all", "percentage", "time"]
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for i in range(2, 11):
            (ok, all), time = check(i, True)
            writer.writerow({"n": i, "decomposable": ok, "all": all, "percentage": ok / all * 100, "time": time})
            csvfile.flush()
