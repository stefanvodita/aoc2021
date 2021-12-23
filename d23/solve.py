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

HALL_SPACES = [(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)]
XMAX = 2

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")[2:-1]
    amphipod = []
    for i, line in enumerate(s):
        for j, c in enumerate(line):
            if c in "ABCD":
                a = (c, "START", i + 1, j - 1)
                amphipod.append(a)
    return amphipod

@lru_cache(maxsize=None)
def is_blocked(amphipod, x, y):
    for a in amphipod:
        if a[2] == x and a[3] == y:
            return True
    return False

def is_color(amphipod, x, y, color):
    for a in amphipod:
        if a[0] == color and a[2] == x and a[3] == y:
            return True
    return False

def is_win(state):
    for a in state:
        if a[1] != "STOP":
            return False
    return True

def get_home_y(a):
    return ("ABCD".index(a[0]) + 1) * 2

def get_home_x(state, a, y):
    for x in range(XMAX, 0, -1):
        if not is_blocked(state, x, y):
            return x
        if not is_color(state, x, y, a[0]):
            return None
    return None

def make_new_pos(a, x, y):
    return (a[0], "HALL" if a[1] == "START" else "STOP", x, y)

def get_stop_move(state, a):
    y = get_home_y(a)
    x = get_home_x(state, a, y)
    if x is None:
        return None
    b = make_new_pos(a, x, y)
    return (a, b)
    
def get_start_moves(state, a):
    return [(a, make_new_pos(a, x, y)) for x, y in HALL_SPACES if not is_blocked(state, x, y)]

def sign(x):
    return -1 if x < 0 else 0 if x == 0 else 1

@lru_cache(maxsize=None)
def is_legal(state, move):
    if move is None:
        return False

    a, b = move

    """
    sw = False
    if state == (('B', 'HALL', 0, 3), ('A', 'HALL', 0, 5), ('C', 'START', 1, 8), ('A', 'STOP', 2, 2), ('C', 'START', 2, 4), ('B', 'START', 2, 8)) and \
       a == ('A', 'HALL', 0, 5) and \
       b == ('A', 'STOP', 1, 2):
       sw = True
    """

    xs, ys = a[2], a[3]
    xe, ye = b[2], b[3]
    fs, fe = (xs, xe) if a[1] == "START" else (ys, ye)
    ss, se = (ys, ye) if a[1] == "START" else (xs, xe)
    while fs != fe:
        fs += sign(fe - fs)
        if is_blocked(state, fs if a[1] == "START" else ss, ss if a[1] == "START" else fs):
            return False
    while ss != se:
        ss += sign(se - ss)
        if is_blocked(state, fs if a[1] == "START" else ss, ss if a[1] == "START" else fs):
            return False
    return True

@lru_cache(maxsize=None)
def get_legal_moves(state):
    moves = []
    for a in state:
        if a[1] == "STOP":
            continue
        elif a[1] == "HALL":
            move = get_stop_move(state, a)
            if is_legal(state, move):
                moves.append(move)
        elif a[1] == "START":
            nmoves = get_start_moves(state, a)
            for move in nmoves:
                if is_legal(state, move):
                    moves.append(move)         
    return moves

@lru_cache(maxsize=None)
def apply_move(state, move):
    a, b = move
    nstate = [x if x != a else b for x in state]
    cost = (abs(a[2] - b[2]) + abs(a[3] - b[3])) * 10**("ABCD".index(a[0]))
    return tuple(nstate), cost

@lru_cache(maxsize=None)
def heuristic(state):
    score = 0
    for a in state:
        if a[1] == "STOP":
            continue
        y = get_home_y(a[0])
        score += (a[2] + 1 + abs(y - a[3])) * 10**("ABCD".index(a[0]))
    return score

def arrange(state):
    c = heuristic(state)
    q = PriorityQueue()
    q.put((c, 0, state))
    v = {state: c}
    #r = {state: [state]}
    
    while not q.empty():
        ct, cr, s = q.get()
        #print(ct, cr, s)
        if is_win(s):
            #for st in r[s]:
            #    print(st)
            print(ct, cr, s)
            return
        for move in get_legal_moves(s):
            ns, nc = apply_move(s, move)
            ch = heuristic(ns)
            if v.get(ns, float("inf")) <= cr + nc + ch:
                continue
            q.put((cr + nc + ch, cr + nc, ns))
            v[ns] = cr + nc + ch
            #r[ns] = r[s] + [ns]

def mark_already_home(amphipod):
    state = []
    for a in amphipod:
        y = get_home_y(a)
        if a[3] != y:
            state.append(a)
            continue
        for x in range(XMAX, a[2] - 1, -1):
            if not is_color(amphipod, x, y, a[0]):
                break
        else:
            state.append((a[0], "STOP", a[2], a[3]))
            continue
        state.append(a)
    return state        

def solve1(filename):
    amphipod = get_input(filename)
    print(amphipod)
    
    amphipod = mark_already_home(amphipod)
    print(amphipod)
    
    print()
    amphipod = tuple(amphipod)
    arrange(amphipod)

def solve2(filename):
    global XMAX
    XMAX = 4
    solve1(filename)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
