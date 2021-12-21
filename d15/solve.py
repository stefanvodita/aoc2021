import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

MIN_RISK = 1
MAX_RISK = 9

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    
    riskmap = [[0 for i in range(len(s[0]))] for j in range(len(s))]
    for i, line in enumerate(s):
        for j, risk in enumerate(line):
            riskmap[i][j] = int(risk)

    return riskmap

def in_bounds(riskmap, x, y):
    return x >= 0 and y >= 0 and x < len(riskmap[0]) and y < len(riskmap)

def get_neighbours(riskmap, x, y):
    d = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    neighbours = []
    for dx, dy in d:
        nx, ny = x + dx, y + dy
        if in_bounds(riskmap, nx, ny):
            neighbours.append((nx, ny))
    return neighbours

def estimate_risk_ahead(riskmap, x, y):
    endx, endy = len(riskmap[0]) - 1, len(riskmap) - 1
    return endx - x + endy - y

def astar(riskmap):
    endx, endy = len(riskmap[0]) - 1, len(riskmap) - 1

    q = PriorityQueue()
    v = set()

    q.put((0, (0, 0)))  # (heuristic, risk, (x, y))
    # q.put((estimate_risk_ahead(riskmap, 0, 0), 0, (0, 0)))
    v.add((0, 0))
    
    while not q.empty():
        risk, coords = q.get()
        # _, risk, coords = q.get()
        x, y = coords
        
        if x == endx and y == endy:
            return risk
        
        for nx, ny in get_neighbours(riskmap, x, y):
            if (nx, ny) not in v:
                q.put((risk + riskmap[nx][ny], (nx, ny)))
                # q.put((risk + riskmap[nx][ny] + estimate_risk_ahead(riskmap, nx, ny), risk + riskmap[nx][ny], (nx, ny)))
                v.add((nx, ny))

    return float("inf")

def solve1(filename):
    riskmap = get_input(filename)
    print(riskmap)
    
    risk = astar(riskmap)
    print(risk)

def increase_risk(x):
    x += 1
    return x if x < MAX_RISK else MIN_RISK

def enlarge(riskmap):
    riskmap = np.array(riskmap)
    riskmap = np.hstack((
        riskmap,
        riskmap % MAX_RISK + MIN_RISK,
        (riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
        ((riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
        (((riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
    ))
    riskmap = np.vstack((
        riskmap,
        riskmap % MAX_RISK + MIN_RISK,
        (riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
        ((riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
        (((riskmap % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK) % MAX_RISK + MIN_RISK,
    ))
    return riskmap

def solve2(filename):
    riskmap = get_input(filename)
    riskmap = enlarge(riskmap)
    print(riskmap)
    
    risk = astar(riskmap)
    print(risk)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
