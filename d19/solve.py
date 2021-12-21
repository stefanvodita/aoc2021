import numpy as np
import pandas as pd
import sys

from collections import Counter
from copy import deepcopy
from functools import reduce
from itertools import combinations, product
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

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
MATCHES = 12
LOS = 1000

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

def change_axis(ps, rot, dist):
    for i in range(len(ps)):
        ps[i] = apply_rot(ps[i], rot) + dist

def intersect(scanners, a, b):
    pa = scanners[a]
    pb = scanners[b]

    mem = {}
    pts = {}

    for p1 in pa:
        for p2 in pb:
            for k, rot in enumerate(ROTS):
                p2m = apply_rot(p2, rot)
                dist = p1 - p2m
                #if comp_max_dist(dist) > 2 * LOS:
                #    continue

                memkey = (k, tuple(dist))
                mem[memkey] = mem.get(memkey, 0) + 1
                pts[memkey] = pts.get(memkey, []) + [(deepcopy(p1), deepcopy(p2))]
                if mem[memkey] >= MATCHES:
                    # change axis
                    change_axis(pb, rot, dist)
                    #tmp = sorted(mem, key=lambda x: mem[x], reverse=True)
                    #print(str(tmp[0]) + ": " + str(mem[tmp[0]]))
                    #print(str(tmp[1]) + ": " + str(mem[tmp[1]]))
                    #print(str(tmp[2]) + ": " + str(mem[tmp[2]]))
                    #print(pts[memkey])
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
        print("base is " + str(base))
        for j in range(len(scanners)):
            if j in known:
                continue
            if intersect(scanners, base, j):
                known.append(j)
                print(str(base) + " matches " + str(j))
        i += 1
        if i == len(known):
            break
    print(known)
    
    beacons = set()
    for scanner in scanners:
        for p in scanner:
            beacons.add(tuple(p))
    count = len(beacons)
    print(count)

def intersect2(scanners, a, b, scanpos):
    pa = scanners[a]
    pb = scanners[b]

    mem = {}
    pts = {}

    for p1 in pa:
        for p2 in pb:
            for k, rot in enumerate(ROTS):
                p2m = apply_rot(p2, rot)
                dist = p1 - p2m
                #if comp_max_dist(dist) > 2 * LOS:
                #    continue

                memkey = (k, tuple(dist))
                mem[memkey] = mem.get(memkey, 0) + 1
                pts[memkey] = pts.get(memkey, []) + [(deepcopy(p1), deepcopy(p2))]
                if mem[memkey] >= MATCHES:
                    # change axis
                    change_axis(pb, rot, dist)
                    # change scanpos
                    #print(a, b)
                    # scanpos[b] = scanpos[a] + dist
                    scanpos[b] = p1 - apply_rot(pts[memkey][-1][1], rot)
                    #print(scanpos[a])
                    #print(scanpos[b])
                    
                    #tmp = sorted(mem, key=lambda x: mem[x], reverse=True)
                    #print(str(tmp[0]) + ": " + str(mem[tmp[0]]))
                    #print(str(tmp[1]) + ": " + str(mem[tmp[1]]))
                    #print(str(tmp[2]) + ": " + str(mem[tmp[2]]))
                    #print(pts[memkey])
                    return True
    return False

def get_md(p1, p2):
    return sum(abs(p1 - p2))

def solve2(filename):
    global ROTS
    ROTS = np.array(list(map(np.array, ROTS)))

    scanners = get_input(filename)
    scanners = np.array(scanners)
    
    scanpos = np.array([[0, 0, 0] for _ in scanners])
    
    known = [0]
    i = 0
    while True:
        base = known[i]
        print("base is " + str(base))
        for j in range(len(scanners)):
            if j in known:
                continue
            if intersect2(scanners, base, j, scanpos):
                known.append(j)
                print(str(base) + " matches " + str(j))
        i += 1
        if i == len(known):
            break
    print(known)
    print(scanpos)
    print()
    
    hmd = 0
    for scanpos1, scanpos2 in combinations(scanpos, r=2):
        md = get_md(scanpos1, scanpos2)
        if md > hmd:
            hmd = md
    print(hmd)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
