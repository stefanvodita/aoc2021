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

OPERATION_NAME_LEN = 3
MODEL_DIGITS = 14
MAXZ = float("inf")

# patrat
VAR1 = [11, 13, 11, 10, -3, -4, 12, -8, -3, -12, 14, -6, 11, -12]
# triunghi
VAR2 = [1, 1, 1, 1, 26, 26, 1, 26, 26, 26, 1, 26, 1, 26]
# cerc
VAR3 = [14, 8, 4, 10, 14, 10, 4, 14, 1, 6, 0, 9, 13, 12]

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    return s.split("\n")

def run(program, inp):
    cursor = 0
    var = {v: 0 for v in "wxyz"}
    for line in program:
        operation = line[:OPERATION_NAME_LEN]
        if operation == "inp":
            where = line[-1]
            var[where] = inp[cursor]
            cursor += 1
            continue
        op1, op2 = line[OPERATION_NAME_LEN+1:].split(" ")
        res = op1
        op1 = var[op1]
        op2 = var[op2] if op2 in var else int(op2)
        if operation == "add":
            var[res] = op1 + op2
        elif operation == "mul":
            var[res] = op1 * op2
        elif operation == "div":
            #fres = op1 / op2
            #var[res] = ceil(fres) if fres < 0 else floor(fres)
            var[res] = op1 // op2
        elif operation == "mod":
            var[res] = op1 % op2
        elif operation == "eql":
            var[res] = 1 if op1 == op2 else 0
    return var["z"]

def calc_exp(idx, w, z):
    x = 1 if (z % 26 + VAR1[idx]) != w else 0
    return (z // VAR2[idx]) * (25 * x + 1) + (w + VAR3[idx]) * x
"""
def guess_model(monad):
    inp = int("9" * MODEL_DIGITS)
    while True:
        if inp % 1000000:
            print(inp)
        ret = run(monad, list(map(int, str(inp))))
        if ret == 0:
            return inp
        inp -= 1
"""

def get_best(mem, idx, nz, z, w):
    if nz not in mem[idx]:
        return (z, w)
    if mem[idx][nz][1] != w:
        return (z, w) if w > mem[idx][nz][1] else mem[idx][nz]

    z1 = z
    z2 = mem[idx][nz][0]
    i = idx - 1
    #print(mem[i], i, nz, z1, z2)
    while mem[i][z1][1] == mem[i][z2][1]:
        z1 = mem[i][z1][0]
        z2 = mem[i][z2][0]
        i -= 1
    return (z, w) if mem[i][z1][1] > mem[i][z2][1] else mem[idx][nz]
    
def get_worst(mem, idx, nz, z, w):
    if nz not in mem[idx]:
        return (z, w)
    if mem[idx][nz][1] != w:
        return (z, w) if w < mem[idx][nz][1] else mem[idx][nz]

    z1 = z
    z2 = mem[idx][nz][0]
    i = idx - 1
    #print(mem[i], i, nz, z1, z2)
    while mem[i][z1][1] == mem[i][z2][1]:
        z1 = mem[i][z1][0]
        z2 = mem[i][z2][0]
        i -= 1
    return (z, w) if mem[i][z1][1] < mem[i][z2][1] else mem[idx][nz]

def get_model(mem):
    model = []
    z = 0
    for i in range(MODEL_DIGITS - 1, -1, -1):
        z, w = mem[i][z]
        model.append(w)
    return "".join(map(str, reversed(model)))

def guess_model(high=True):
    get = get_best if high else get_worst
    mem = [{} for _ in range(MODEL_DIGITS)]
    for i in range(MODEL_DIGITS):
        print(i)
        for w in range(1, 10):
            for z in mem[i - 1] if i > 0 else [0]:
                nz = calc_exp(i, w, z)
                if nz > MAXZ:
                    continue
                mem[i][nz] = get(mem, i, nz, z, w)
    return get_model(mem)

def solve1(filename):
    program = get_input(filename)
    
    model = guess_model()
    print(model)

def solve2(filename):
    program = get_input(filename)
    
    model = guess_model(high=False)
    print(model)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
