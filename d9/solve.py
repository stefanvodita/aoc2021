import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean

MAX_HEIGHT = 9

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")

    geography = [[0 for j in range(len(s[0]))] for i in range(len(s))]
    
    for i, line in enumerate(s):
        for j, c in enumerate(line.strip()):
            geography[i][j] = int(c)
    return geography

def in_bounds(n, m, x, y):
    return x >= 0 and y >= 0 and x < n and y < m

def is_low(geography, x, y):
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    d = list(zip(dx, dy))
    for dx, dy in d:
        nx = x + dx
        ny = y + dy
        if in_bounds(len(geography), len(geography[0]), nx, ny):
            if geography[nx][ny] <= geography[x][y]:
                return False
    return True
        

def solve1(filename):
    geography = get_input(filename)
    print(pd.DataFrame(geography))
    
    risk = 0
    for i in range(len(geography)):
        for j in range(len(geography[0])):
            if is_low(geography, i, j):
                print(i, j)
                risk += 1 + geography[i][j]
    print(risk)

def neighbours(geography, x, y):
    ns = []
    dx = [0, 1, 0, -1]
    dy = [1, 0, -1, 0]
    d = list(zip(dx, dy))
    for dx, dy in d:
        nx = x + dx
        ny = y + dy
        if in_bounds(len(geography), len(geography[0]), nx, ny):
            ns.append((nx, ny))
    return ns

def measure_basin(geography, x, y):
    size = 0
    q = [(x, y)]
    while q:
        x, y = q.pop()
        for nx, ny in neighbours(geography, x, y):
            if geography[nx][ny] < MAX_HEIGHT and geography[nx][ny] > geography[x][y] and (nx, ny) not in q:
                q.insert(0, (nx, ny))
        geography[x][y] = MAX_HEIGHT
        size += 1
    return size

def solve2(filename):
    geography = get_input(filename)
    print(pd.DataFrame(geography))
    
    lows = []
    for i in range(len(geography)):
        for j in range(len(geography[0])):
            if is_low(geography, i, j):
                lows.append((i, j))
    sizes = []
    for x, y in lows:
        sizes.append(measure_basin(geography, x, y))
    sizes.sort(reverse=True)
    print(sizes)
    print(reduce(mul, sizes[:3], 1))

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
1435
"""
