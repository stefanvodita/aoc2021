import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import lru_cache, reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

BOARD_SIZE = 10
DIE_SIDES = 100
MAX_SCORE = 1000
ROLLS = 3

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    return int(s[0][-1]), int(s[1][-1])

def increase_die(die):
    if die == DIE_SIDES:
        return 1
    return die + 1

def increase_tile(tile, die):
    tile += die
    if tile % 10 == 0:
        return 10
    return tile % 10

def solve1(filename):
    tile1, tile2 = get_input(filename)
    print(tile1, tile2)
    
    score1, score2 = 0, 0
    dierolls = 0
    
    player = 1
    die = 1
    while True:
        if score1 >= MAX_SCORE:
            print(score2)
            print(dierolls)
            score2 *= dierolls
            print(score2)
            return
        if score2 >= MAX_SCORE:
            print(score1)
            print(dierolls)
            score1 *= dierolls
            print(score1)
            return
        
        roll = 0
        for _ in range(ROLLS):
            roll += die
            die = increase_die(die)
        
        if player == 1:
            tile1 = increase_tile(tile1, roll)
            score1 += tile1
        else:
            tile2 = increase_tile(tile2, roll)
            score2 += tile2
            
        player *= -1
        dierolls += 3

"""
1, 1, 1 = 3
1, 1, 2 = 4
1, 1, 3 = 5
1, 2, 1 = 4
1, 2, 2 = 5
1, 2, 3 = 6
1, 3, 1 = 5
1, 3, 2 = 6
1, 3, 3 = 7

3: 1     = 1
4: 2 1   = 3
5: 3 2 1 = 6
6: 2 3 2 = 7
7: 1 2 3 = 6
8:   1 2 = 3
9:     1 = 1
"""

rolls3 = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

@lru_cache(maxsize=None)
def get_wins(tile1, tile2, score1, score2, player):
    if score1 >= MAX_SCORE:
        return 1, 0
    if score2 >= MAX_SCORE:
        return 0, 1
     
    
    wins1, wins2 = 0, 0
    if player == 1:
        for roll, chance in rolls3.items():
            ntile = increase_tile(tile1, roll)
            nwins1, nwins2 = get_wins(ntile, tile2, score1 + ntile, score2, 2)
            wins1 += chance * nwins1
            wins2 += chance * nwins2
    else:
        for roll, chance in rolls3.items():
            ntile = increase_tile(tile2, roll)
            nwins1, nwins2 = get_wins(tile1, ntile, score1, score2 + ntile, 1)
            wins1 += chance * nwins1
            wins2 += chance * nwins2
    return wins1, wins2

def solve2(filename):
    global DIE_SIDES
    global MAX_SCORE
    
    DIE_SIDES = 3
    MAX_SCORE = 21
    
    tile1, tile2 = get_input(filename)
    wins1, wins2 = get_wins(tile1, tile2, 0, 0, 1)
    print(wins1)
    print(wins2)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
5944
"""
