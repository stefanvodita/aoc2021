import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import lru_cache, reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

INIT_AREA_LOW = -50
INIT_AREA_HIGH = 50

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    cmds = []
    for line in s:
        cmd, coords = line.split(" ")
        cmd = cmd == "on"
        coords = list(map(lambda x: list(map(int, x[2:].split(".."))), coords.split(",")))
        cmds.append((cmd, coords))
    return cmds

def fit2init(x):
    if x[0] > INIT_AREA_HIGH or x[1] < INIT_AREA_LOW:
        return False
    return [max(x[0], INIT_AREA_LOW), min(x[1], INIT_AREA_HIGH)]

def solve1(filename):
    cmds = get_input(filename)
    print(cmds)
    
    size = INIT_AREA_HIGH - INIT_AREA_LOW + 1
    cubes = np.zeros((size, size, size), dtype=bool)
    
    translation = INIT_AREA_HIGH
    for cmd in cmds:
        print(cmd)
        on, coords = cmd
        coords = list(map(fit2init, coords))
        if not all(coords):
            continue
        coords = list(map(lambda x: [x[0] + translation, x[1] + translation], coords))
        x, y, z = coords
        print(x, y, z)
        cubes[x[0]:x[1]+1, y[0]:y[1]+1, z[0]:z[1]+1] = on
    count = np.count_nonzero(cubes)
    print(count)

def unpack_coord(coord):
    l, h = coord
    xl, yl, zl = l
    xh, yh, zh = h
    return xl, yl, zl, xh, yh, zh

"""
@ret pieces of cube1 not in cube2
"""
def intersect(cube1, cube2):
    xl1, yl1, zl1, xh1, yh1, zh1 = unpack_coord(cube1)
    xl2, yl2, zl2, xh2, yh2, zh2 = unpack_coord(cube2)
    if xl2 > xh1 and yl2 > yh1 and zl2 > zh1 or \
       xh2 < xl1 and yh2 < yl1 and zh2 < zl1:
        return [cube1]

    xli = max(xl1, xl2)
    yli = max(yl1, yl2)
    zli = max(zl1, zl2)
    xhi = min(xh1, xh2)
    yhi = min(yh1, yh2)
    zhi = min(zh1, zh2)
    
    ncubes = [
        [(xl1, yl1, zl1), (xli, yh1, zh1)],
        
        
        [(xli, yl1, zl1), (xhi, yli, zh1)],
        
        [(xli, yli, zl1), (xhi, yhi, zli)],
        # [(xli, yli, zli), (xhi, yhi, zhi)],
        [(xli, yli, zhi), (xhi, yhi, zh1)],
        
        [(xli, yhi, zl1), (xhi, yh1, zh1)],
        
        
        [(xhi, yl1, zl1), (xh1, yh1, zh1)],
    ]
    
    ncubes = list(filter(lambda cube: all(np.array(cube[0]) != np.array(cube[1])), ncubes))
    return ncubes

def turn_on(ocubes, ncubes):
    for cube1 in ocubes:
        for cube2 in ncubes:
            nncubes = intersect(cube2, cube1)    # ret pieces of cube2 outside cube1
            if not nncubes:
                return []
            if nncubes[0] != cube2:
                break
        ncubes.remove(cube2)
        ncubes += nncubes
    return ncubes

def turn_off(cubes, coord):
    rcubes = []
    for cube in cubes:
        rcubes += intersect(cube, coord)        # ret pieces of cube1 outside cube2
    return rcubes

def count_on(cubes):
    count = 0
    for cube in cubes:
        xl, yl, zl, xh, yh, zh = unpack_coord(cube)
        count += (xh - xl + 1) * (yh - yl + 1) * (zh - zl + 1)
    return count

def solve2(filename):
    cmds = get_input(filename)
    cmds = list(map(lambda cmd: (cmd[0], list(zip(*cmd[1]))), cmds))
    
    cubes = []
    for cmd in cmds[:2]:
        on, coords = cmd
        if on:
            ncubes = turn_on(cubes, [coords])   # add new cubes
            cubes += ncubes
        else:
            rcubes = turn_off(cubes, coords)    # replace cubes
            cubes = rcubes
    print(cubes)
    
    count = count_on(cubes)
    print(count)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""

"""
    ncubes = [
        [(xl1, yl1, zl1), (xli, yli, zli)],
        [(xl1, yl1, zli), (xli, yli, zhi)],
        [(xl1, yl1, zhi), (xli, yli, zh1)],
        
        [(xl1, yli, zl1), (xli, yhi, zli)],
        [(xl1, yli, zli), (xli, yhi, zhi)],
        [(xl1, yli, zhi), (xli, yhi, zh1)],
        
        [(xl1, yhi, zl1), (xli, yh1, zli)],
        [(xl1, yhi, zli), (xli, yh1, zhi)],
        [(xl1, yhi, zhi), (xli, yh1, zh1)],
        
        
        [(xli, yl1, zl1), (xhi, yli, zli)],
        [(xli, yl1, zli), (xhi, yli, zhi)],
        [(xli, yl1, zhi), (xhi, yli, zh1)],
        
        [(xli, yli, zl1), (xhi, yhi, zli)],
        # [(xli, yli, zli), (xhi, yhi, zhi)],
        [(xli, yli, zhi), (xhi, yhi, zh1)],
        
        [(xli, yhi, zl1), (xhi, yh1, zli)],
        [(xli, yhi, zli), (xhi, yh1, zhi)],
        [(xli, yhi, zhi), (xhi, yh1, zh1)],
        
        
        [(xhi, yl1, zl1), (xh1, yli, zli)],
        [(xhi, yl1, zli), (xh1, yli, zhi)],
        [(xhi, yl1, zhi), (xl1, yli, zh1)],
        
        [(xhi, yli, zl1), (xh1, yhi, zli)],
        [(xhi, yli, zli), (xh1, yhi, zhi)],
        [(xhi, yli, zhi), (xh1, yhi, zh1)],
        
        [(xhi, yhi, zl1), (xh1, yh1, zli)],
        [(xhi, yhi, zli), (xh1, yh1, zhi)],
        [(xhi, yhi, zhi), (xh1, yh1, zh1)],
    ]
"""
