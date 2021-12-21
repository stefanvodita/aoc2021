import numpy as np
import pandas as pd
import sys

from collections import Counter
from math import ceil, floor
from statistics import mean

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    crabs = list(map(int, s.rstrip().split(",")))
    return crabs

def solve1(filename):
    crabs = Counter(get_input(filename))
    print(crabs)
    
    fuel = [[0, 0, 0, 0] for i in range(max(crabs.keys()) + 1)]
    
    for i in range(1, len(fuel)):
        fuel[i][0] = fuel[i - 1][0] + fuel[i - 1][1] + crabs[i - 1]
        fuel[i][1] = fuel[i - 1][1] + crabs[i - 1]
    print(fuel)
    
    for i in range(len(fuel) - 2, -1, -1):
        fuel[i][2] = fuel[i + 1][2] + fuel[i + 1][3] + crabs[i + 1]
        fuel[i][3] = fuel[i + 1][3] + crabs[i + 1]
    print(fuel)
    
    fuel = list(map(lambda x: x[0] + x[2], fuel))
    print(fuel)

    pos = np.argmin(fuel)
    min_fuel = min(fuel)
    print(min_fuel)

def solve2(filename):
    crabs = get_input(filename)
    pos = floor(mean(crabs))
    print(pos)
    
    fuel = 0
    for p, n in Counter(crabs).items():
        fuel += abs(p - pos) * (abs(p - pos) + 1) * n
    fuel /= 2
    print(fuel)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
1
317

101571337
"""
