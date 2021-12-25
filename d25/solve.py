import numpy as np
import pandas as pd
import sys

from collections import Counter
from copy import deepcopy
from functools import lru_cache, reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    m = [["." for i in range(len(s[0]))] for j in range(len(s))]
    for i, line in enumerate(s):
        for j, c in enumerate(line):
            m[i][j] = c
    return m

def get_next(m, x, y):
    if m[x][y] == ">":
        return x, (y + 1) % len(m[0])
    elif m[x][y] == "v":
        return (x + 1) % len(m), y

def move(m, x, y, moved):
    if m[x][y] == ".":
        return False
    nx, ny = get_next(m, x, y)
    #if m[nx][ny] != "." or nm[nx][ny] != ".":
    if m[nx][ny] != "." or (nx, ny) in moved:
        #nm[x][y] = m[x][y]
        return False
    #print(m[x][y], x, y, nx, ny)
    m[nx][ny] = m[x][y]
    m[x][y] = "."
    #moved[nx][ny] = True
    #nm[nx][ny] = m[nx][ny]
    moved.add((x, y))
    moved.add((nx, ny))
    return True

def solve1(filename):
    m = get_input(filename)
    print(np.array(m))
    
    step = 0
    is_moving = True
    while is_moving:
        is_moving = False
        #moved = [[False for i in range(len(m[0]))] for j in range(len(m))]
        #nm = [["." for i in range(len(m[0]))] for j in range(len(m))]
        moved = set()
        for i in range(len(m)):
            for j in range(len(m[0])):
                if (i, j) not in moved and m[i][j] == ">" and move(m, i, j, moved):
                    is_moving = True
        #print(np.array(m))
        moved = set()
        for i in range(len(m)):
            for j in range(len(m[0])):
                if (i, j) not in moved and m[i][j] == "v" and move(m, i, j, moved):
                    is_moving = True
        step += 1
        #m = nm
        #print(np.array(m))
    print(step)

def solve2(filename):
    pass

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
