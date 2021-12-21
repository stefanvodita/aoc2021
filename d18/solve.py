import numpy as np
import pandas as pd
import sys

from collections import Counter
from copy import deepcopy
from functools import reduce
from itertools import product
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

class SnailfishNum:
    l = None
    r = None
    v = None
    p = None

    def __str__(self):
        if self.v is None:
            return "[" + str(self.l) + "," + str(self.r) + "]"
        else:
            return str(self.v)

    def _str_depth(self, depth):
        if self.v is None:
            return "[" + self.l._str_depth(depth + 1) + "," + self.r._str_depth(depth + 1) + "]"
        else:
            return str(depth)
        
    def str_depth(self):
        return self._str_depth(0)

    def print_tree(self):
        x = self
        while x.p is not None:
            x = x.p
        print(str(x))
        # print("Depths")
        # print(x.str_depth())

def str2snail(s):
    num = SnailfishNum()
    if s[0] != "[":
        num.v = int(s[0])
    else:
        num.l, s = str2snail(s[1:])
        num.r, s = str2snail(s[1:])
        num.l.p = num
        num.r.p = num
    return num, s[1:]

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    nums = []
    for line in s.split("\n"):
        nums.append(str2snail(line)[0])
    return nums

def get_depth(x):
    depth = 0
    while x.p:
        x = x.p
        depth += 1
    return depth

def left_add(x, v):
    while x.p is not None and x.p.l == x:
        x = x.p
    if x.p is None:
        return
    x = x.p.l
    while x.r is not None:
        x = x.r
    x.v += v

def right_add(x, v):
    while x.p is not None and x.p.r == x:
        x = x.p
    if x.p is None:
        return
    x = x.p.r
    while x.l is not None:
        x = x.l
    x.v += v

def snail_explode(x, depth):
    if x.v is not None:
        return x
    if depth != 0:
        num = SnailfishNum()
        num.l = snail_explode(x.l, depth - 1)
        num.r = snail_explode(x.r, depth - 1)
        num.l.p = num
        num.r.p = num
        return num
    # print("Exploding " + str(x))
    left_add(x, x.l.v)
    right_add(x, x.r.v)
    x.l = None
    x.r = None
    x.v = 0
    #print("exploded:", end ="")
    #x.print_tree()
    return x

"""
def snail_split(x):
    if x.v is None:
        num = SnailfishNum()
        num.l = snail_split(x.l)
        num.r = snail_split(x.r)
        num.l.p = num
        num.r.p = num
        return num
    if x.v < 10:
        return x
    # print("Splitting " + str(x))
    x.l = SnailfishNum()
    x.r = SnailfishNum()
    x.l.v = floor(x.v / 2)
    x.r.v = ceil(x.v / 2)
    x.l.p = x
    x.r.p = x
    x.v = None
    print("splitted:", end="")
    x.print_tree()
    # x = snail_explode(x, 4 - get_depth(x))
    return x
"""

def snail_split(x):
    if x.v is None:
        return snail_split(x.l) or snail_split(x.r)
    if x.v < 10:
        return False
    # print("Splitting " + str(x))
    x.l = SnailfishNum()
    x.r = SnailfishNum()
    x.l.v = floor(x.v / 2)
    x.r.v = ceil(x.v / 2)
    x.l.p = x
    x.r.p = x
    x.v = None
    #print("splitted:", end="")
    #x.print_tree()
    return True

def snail_reduce(x):
    init = str(x)
    #print("reducing:", end="")
    #x.print_tree()
    x = snail_explode(x, 4)
    if not snail_split(x):
        return x
    return snail_reduce(x)

def snail_add(x, y):
    res = SnailfishNum()
    res.l = x
    res.r = y
    x.p = res
    y.p = res
    res = snail_reduce(res)
    return res

def get_magnitude(x):
    if x.v is not None:
        return x.v
    return 3 * get_magnitude(x.l) + 2 * get_magnitude(x.r)

def solve1(filename):
    nums = get_input(filename)

    for num in nums:
        print(num)
    print()
    
    s = nums[0]
    for num in nums[1:]:
        s = snail_add(s, num)
    print(str(s))
    
    mag = get_magnitude(s)
    print(mag)

def solve2(filename):
    nums = get_input(filename)
    
    maxmag = -float("inf")
    for x, y in product(nums, repeat=2):
        #x = deepcopy(x)
        #y = deepcopy(y)
        if x == y:
            continue
        mag = get_magnitude(snail_add(x, y))
        if mag > maxmag:
            maxmag = mag
    # maxmag = max(map(get_magnitude, map(lambda x: snail_add(x[0], x[1]), filter(lambda x: x[0] != x[1], product(nums, repeat=2)))))
    print(maxmag)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
4453
4615
"""
