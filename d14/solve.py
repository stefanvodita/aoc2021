import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from statistics import mean, median

STEPS = 40

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    
    polymer = s[0]
    reacts = {}
    for line in s[2:]:
        k, _, v = line.split(" ")
        reacts[k] = v

    return polymer, reacts

def zip_chem(polymer, inserts):
    return "".join([polymer[i] + inserts[i] for i in range(len(inserts))] + [polymer[-1]])

def do_react(polymer, reacts):
    inserts = []
    for i in range(len(polymer) - 1):
        inserts.append(reacts.get(polymer[i:i+2], ""))
    return zip_chem(polymer, inserts)

def solve1(filename):
    polymer, reacts = get_input(filename)
    print(polymer)
    print(reacts)
    
    for _ in range(STEPS):
        polymer = do_react(polymer, reacts)
        #print(polymer)
    
    c = Counter(polymer)
    res = max(c.values()) - min(c.values())
    print(res)

def break_up(polymer):
    res = {}
    for i in range(len(polymer) - 1):
        res[polymer[i:i+2]] = res.get(polymer[i:i+2], 0) + 1
    return res

def do_react_efficient(polymer, reacts):
    nmer = {}
    for pair in polymer:
        if pair not in reacts:
            nmer[pair] = polymer[pair]
        else:
            nmer[pair[0] + reacts[pair]] = nmer.get(pair[0] + reacts[pair], 0) + polymer[pair]
            nmer[reacts[pair] + pair[1]] = nmer.get(reacts[pair] + pair[1], 0) + polymer[pair]
    return nmer

def count_elems(polymer):
    c = {}
    for pair in polymer:
        c[pair[0]] = c.get(pair[0], 0) + polymer[pair]
    return c

def solve2(filename):
    polymer, reacts = get_input(filename)
    last = polymer[-1]
    polymer = break_up(polymer)
    print(polymer)
    print(reacts)
    
    for _ in range(STEPS):
        polymer = do_react_efficient(polymer, reacts)
        print(polymer)
    
    c = count_elems(polymer)
    c[last] = c.get(last, 0) + 1
    print(c)
    
    res = max(c.values()) - min(c.values())
    print(res)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
