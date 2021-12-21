import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean, median

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    
    g = {}
    for line in s.split("\n"):
        x, y = line.split("-")
        g[x] = g.get(x, []) + [y]
        g[y] = g.get(y, []) + [x]
    return g

def dfs(g, n, visited):
    if n == "end":
        return 1
    if n.islower():
        visited.add(n)
    count = 0
    for neighbour in g[n]:
        if neighbour not in visited:
            count += dfs(g, neighbour, visited)
    visited.discard(n)
    return count

def solve1(filename):
    g = get_input(filename)
    print(g)
    
    count = dfs(g, "start", set())
    print(count)

def dfs_mod(g, n, visited, exception, path):
    npath = path.copy()
    npath.append(n)
    if n == "end":
        #print(npath)
        return 1
    if n.islower():
        visited[n] += 1
    count = 0
    for neighbour in g[n]:
        if visited[neighbour] == 0:
            count += dfs_mod(g, neighbour, visited, exception, npath)
        elif not exception and neighbour != "start":
            count += dfs_mod(g, neighbour, visited, True, npath)
    if n.islower():
        visited[n] -= 1
    return count

def solve2(filename):
    g = get_input(filename)
    print(g)
    
    count = dfs_mod(g, "start", {k : 0 for k in g}, False, [])
    print(count)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
