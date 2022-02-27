from random import random
from itertools import combinations

def check_if_nodes_edges(V, E):
    nodes_with_edges = [v1 for (v1,v2) in E]
    for vertex in V:
        if vertex not in nodes_with_edges:
            return False
    return True

def ER(n, p):
    V = set([v for v in range(n)])
    E = set()
    for c in combinations(V, 2):
        a = random()
        if a < p:
            E.add(c)

    return V, E

n = 8
p = 0.3
V, E = ER(n, p)
print(V)
print(E)
