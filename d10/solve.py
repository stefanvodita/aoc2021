import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean, median

OPEN_PARENS = ["(", "[", "{", "<"]
CLOSE_PARENS = [")", "]", "}", ">"]
CORRUPTION_SCORES = [3, 57, 1197, 25137]

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    return s.split("\n")

def matches(opener, closer):
    return (opener, closer) in zip(OPEN_PARENS, CLOSE_PARENS)

def get_corruption(entry):
    stack = []
    for c in entry:
        if c in OPEN_PARENS:
            stack.append(c)
        elif not stack:
            return c
        else:
            opener = stack.pop()
            if not matches(opener, c):
                return c
    return None

def get_corruption_score(corruption):
    return CORRUPTION_SCORES[CLOSE_PARENS.index(corruption)]

def solve1(filename):
    entries = get_input(filename)

    score = 0
    for entry in entries:
        c = get_corruption(entry)
        if c is None:
            continue
        score += get_corruption_score(c)
    print(score)

def get_fill(entry):
    stack = []
    for c in entry:
        if c in OPEN_PARENS:
            stack.append(c)
        elif not stack:
            return None
        else:
            opener = stack.pop()
            if not matches(opener, c):
                return None
    return map(lambda opener: CLOSE_PARENS[OPEN_PARENS.index(opener)], reversed(stack))

def score_fill(fill):
    score = 0
    for c in fill:
        score *= 5
        score += CLOSE_PARENS.index(c) + 1
    return score

def solve2(filename):
    entries = get_input(filename)

    scores = []
    for entry in entries:
        fill = get_fill(entry)
        if fill is None:
            continue
        scores.append(score_fill(fill))
    print(median(scores))

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
