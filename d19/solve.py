import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

MATCHES = 12
LOS = 1000

ROTS = [
    [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [0, 1, 0],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 1, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [0, 1, 0],
     [1, 0, 0]],
    [[0, -1, 0],
     [1, 0, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]],
    [[0, 1, 0],
     [1, 0, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [1, 0, 0],
     [0, -1, 0]],
    [[0, 1, 0],
     [-1, 0, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [-1, 0, 0],
     [0, -1, 0]],
    [[0, -1, 0],
     [-1, 0, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [-1, 0, 0],
     [0, 1, 0]],
    [[1, 0, 0],
     [0, 0, -1],
     [0, 1, 0]],
    [[0, 1, 0],
     [0, 0, -1],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 0, -1],
     [0, -1, 0]],
    [[0, -1, 0],
     [0, 0, -1],
     [1, 0, 0]],
    [[1, 0, 0],
     [0, -1, 0],
     [0, 0, -1]],
    [[0, 0, -1],
     [0, -1, 0],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, -1, 0],
     [0, 0, 1]],
    [[0, 0, 1],
     [0, -1, 0],
     [1, 0, 0]],
    [[1, 0, 0],
     [0, 0, 1],
     [0, -1, 0]],
    [[0, -1, 0],
     [0, 0, 1],
     [-1, 0, 0]],
    [[-1, 0, 0],
     [0, 0, 1],
     [0, 1, 0]],
    [[0, 1, 0],
     [0, 0, 1],
     [1, 0, 0]],
]

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    i = 0
    scanners = []
    while i < len(s):
        if s[i][:3] == "---":
            i += 1
            beacons = []
            while i < len(s) and s[i] != "":
                beacon = np.array(list(map(int, s[i].split(","))))
                beacons.append(beacon)
                i += 1
            scanners.append(np.array(beacons))
        i += 1
    return scanners

def apply_rot(p, rot):
    res = np.matmul(rot, p)
    res = np.transpose(res)
    return res

def comp_max_dist(dist):
    return np.amax(dist)

def matches(p1, p2, rot, dist):
    res = np.all(p1 == apply_rot(p2, rot) + dist)
    return res

def enough_match(pa, pb, rot, dist):
    counter = 0
    for p1 in pa:
        for p2 in pb:
            if matches(p1, p2, rot, dist):
                counter += 1
            if counter >= MATCHES:
                return True
    return False

def intersect(scanners, a, b):
    pa = scanners[a]
    pb = scanners[b]
    
    for p1 in pa:
        for p2 in pb:
            for rot in ROTS:
                p2 = apply_rot(p2, rot)
                dist = p1 - p2
                if comp_max_dist(dist) > 2 * LOS:
                    continue
                if enough_match(pa, pb, rot, dist):
                    # change axis
                    return True
    return False

def solve1(filename):
    global ROTS
    ROTS = np.array(list(map(np.array, ROTS)))

    scanners = get_input(filename)
    scanners = np.array(scanners)
    print(scanners)
    
    known = [0]
    i = 0
    while True:
        base = known[i]
        for j in range(len(scanners)):
            if j in known:
                continue
            if intersect(scanners, base, j):
                known.append(j)
        i += 1
        if i == len(known):
            break
        break
    print(known)
    #print(scanners)

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
