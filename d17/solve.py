import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    _, _, x, y = s.split(" ")
    x = x[2:-1]
    y = y[2:]
    minx, maxx = list(map(int, [x.split(".")[i] for i in [0, 2]]))
    miny, maxy = list(map(int, [y.split(".")[i] for i in [0, 2]]))
    return minx, maxx, miny, maxy

def simulate(minx, maxx, miny, maxy, vx, vy):
    dx, dy = -1, -1
    x, y, = 0, 0
    while True:
        x += vx
        y += vy
        vx += dx
        vy += dy
        
        if vx == 0:
            dx = 0
            
        if x > maxx or y < miny:
            return False
            
        if x >= minx and x <= maxx and y >= miny and y <= maxy:
           return True


def solve1(filename):
    minx, maxx, miny, maxy = get_input(filename)
    print(minx, maxx, miny, maxy)
    
    bvy = 0
    for vx in range(12, 18):
        for vy in range(0, 1000):
            is_hit = simulate(minx, maxx, miny, maxy, vx, vy)
            if is_hit:
                bvy = vy
    print(bvy)
    
    """
    x=minx..maxx
    sx = x + x - 1 + x - 2 + ... + 0    // nu neaparat pana la 0
    sx = x * (x + 1) / 2
    minx <= sx <= maxx
    minx <= 1/2 x^2 + 1/2 x <= maxx
    =>
        2x^2 + 2x - 158 >= 0
        2x^2 + 2x - 274 <= 0
        Wolfram Alpha => x in {9, 10, 11}
        
    y=miny..maxy
    sy = y + y - 1 + y - 2 + ... + b    // nu neaparat pana la 0
    sy = (y + b) * (y - b + 1) / 2
    miny <= sy <= maxy
    miny <= 1/2 y^2 + 1/2 y - 1/2 (b^2 - b) <= maxy
    =>
        2y^2 + 2y - (b^2 - b) + 352 >= 0
        2y^2 + 2y - (b^2 - b) + 234 <= 0
        Wolfram Alpha => y in {1..6}
    """

def solve2(filename):
    minx, maxx, miny, maxy = get_input(filename)
    print(minx, maxx, miny, maxy)
    
    count = 0
    for vx in range(0, 200):
        for vy in range(-300, 300):
            is_hit = simulate(minx, maxx, miny, maxy, vx, vy)
            if is_hit:
                count += 1
    print(count)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
3741
"""
