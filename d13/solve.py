import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean, median

def build_mat(points):
    maxx = max(points, key=lambda x: x[0])[0]
    maxy = max(points, key=lambda x: x[1])[1]
    
    mat = [[False for i in range(maxx + 1)] for j in range(maxy + 1)]
    for x, y in points:
        mat[y][x] = True
    return mat

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    
    points = []
    folds = []
    doing_folds = False
    for line in s.split("\n"):
        if not doing_folds:
            if line == "":
                doing_folds = True
                continue
            x, y = line.split(",")
            points.append((int(x), int(y)))
        else:
            d, v = line.split("=")
            d = d[-1]
            folds.append((d, int(v)))
    
    mat = build_mat(points)
    return mat, folds
    
def fold_vert(mat, val):
    n, m = len(mat), len(mat[0])
    if val < m // 2:
        print("Folded side is larger")
    
    nmat = [[mat[j][i] for i in range(val)] for j in range(n)]
    #print(pd.DataFrame(nmat))

    for i in range(n):
        for j in range(val + 1, m):
            nmat[i][2 * val - j] = nmat[i][2 * val - j] or mat[i][j]
    return nmat

def fold_hori(mat, val):
    n, m = len(mat), len(mat[0])
    if val < n // 2:
        print("Folded side is larger")
    
    nmat = [[mat[j][i] for i in range(m)] for j in range(val)]
    #print(pd.DataFrame(nmat))

    for i in range(val + 1, n):
        for j in range(m):
            nmat[2 * val - i][j] = nmat[2 * val - i][j] or mat[i][j]
    return nmat

def fold(mat, fold):
    if fold[0] == "x":
        return fold_vert(mat, fold[1])
    elif fold[0] == "y":
        return fold_hori(mat, fold[1])
    else:
        print("Wrong fold")

def solve1(filename):
    mat, folds = get_input(filename)
    print(pd.DataFrame(mat))
    
    mat = fold(mat, folds[0])
    print(pd.DataFrame(mat))
    
    #mat = fold(mat, folds[1])
    #print(pd.DataFrame(mat))
    
    count = 0
    for line in mat:
        for dot in line:
            if dot:
                count += 1
    print(count)

def solve2(filename):
    mat, folds = get_input(filename)
    print(pd.DataFrame(mat))
    
    for f in folds:
        mat = fold(mat, f)
    print(pd.DataFrame(mat))
    
    with open("mat.txt", "w") as fout:
        for line in mat:
            for dot in line:
                fout.write("1" if dot else "0")
            fout.write("\n")

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
