import pandas as pd
import sys

from collections import Counter
from math import ceil

DAYS_TOTAL = 256
DAYS_BREAK = 7
DAYS_BOOT = 2

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    fishes = list(map(int, s.rstrip().split(",")))
    return fishes

"""
def breed(fish, days_total):
    if fish > days_total:
        return 0
    n_fish = 0
    base = ceil((days_total - fish) / DAYS_BREAK)
    for i in range(base):
        n_fish += breed(DAYS_BREAK + DAYS_BOOT, days_total - fish - i * DAYS_BREAK)
    return n_fish + base

def solve1(filename):
    fishes = get_input(filename)
    n_fish = len(fishes)
    
    for fish in fishes:
        n_fish += breed(fish, DAYS_TOTAL)
    print(n_fish)
"""

"""
def solve1(filename):
    fishes = get_input(filename)
    n_fish = len(fishes)
    
    breed = [[0 for i in range(DAYS_BREAK + DAYS_BOOT)] for j in range(DAYS_TOTAL + 1)]
    for i in range(1, DAYS_TOTAL + 1):
        for j in range(DAYS_BREAK + DAYS_BOOT):
            if j > i:
                continue
            base = ceil((i - j) / DAYS_BREAK)
            n_fish = 0
            for k in range(base):
                if i - j - k * DAYS_BREAK - 1 <= 0:
                    continue
                n_fish += breed[i - j - k * DAYS_BREAK - 1][DAYS_BREAK + DAYS_BOOT - 1]
            breed[i][j] = base + n_fish
            
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(pd.DataFrame(breed))
    
    c = Counter(fishes)
    for fish, num in c.items():
        n_fish += num * (breed[DAYS_TOTAL][fish] + 1)
    print(n_fish)
"""

def solve1(filename):
    fishes = get_input(filename)
    n_fish = len(fishes)
    
    c = Counter(fishes)
    for day in range(DAYS_TOTAL):
        breeders = c[0]
        for i in range(DAYS_BREAK + DAYS_BOOT):
            c[i] = c[i + 1]
        c[DAYS_BREAK - 1] += breeders
        c[DAYS_BREAK + DAYS_BOOT - 1] = breeders
    print(sum(c.values()))

def solve2(filename):
    solve1(filename)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
        #n = breed(1, 9)
        #print(n)
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
