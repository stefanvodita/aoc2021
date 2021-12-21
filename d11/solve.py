import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean, median

STEPS = 100
LIMIT = 9

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    
    s = s.split("\n")
    octopi = [[0 for i in range(len(s))] for j in range(len(s))]
    for i, line in enumerate(s):
        for j, octopus in enumerate(line.rstrip()):
            octopi[i][j] = int(octopus)
    return octopi

def in_bounds(n, x, y):
    return x >= 0 and y >= 0 and x < n and y < n

def flash(octopi, x, y):
    octopi[x][y] = 0
    count = 0
    d = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    for dx, dy in d:
        nx, ny = x + dx, y + dy
        if in_bounds(len(octopi), nx, ny) and octopi[nx][ny] != 0:
            octopi[nx][ny] += 1
            if octopi[nx][ny] > 9:
                count += 1 + flash(octopi, nx, ny)
    return count

def update(octopi):
    count = 0
    for i in range(len(octopi)):
        for j in range(len(octopi[0])):
            octopi[i][j] += 1
    for i in range(len(octopi)):
        for j in range(len(octopi[0])):
            if octopi[i][j] > 9:
                count += 1 + flash(octopi, i, j)
    return count

def solve1(filename):
    octopi = get_input(filename)
    
    flashes = 0
    for step in range(STEPS):
        flashes += update(octopi)

    print(octopi)
    print(flashes)

def solve2(filename):
    octopi = get_input(filename)
    
    flashes = 0
    step = 0
    while True:
        step += 1
        flashes = update(octopi)
        if flashes == len(octopi)**2:
            print(step)
            return

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
