import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

ITER = 50
DARK = "."
LIGHT = "#"
WINDOW_SIZE = 3

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    s = s.split("\n")
    return s[0], s[2:]

def border_up(image, pixel):
    horiz_bord = [pixel * len(image[0])] * (WINDOW_SIZE - 1)
    
    image = horiz_bord + image + horiz_bord
    
    vert_bord = pixel * (WINDOW_SIZE - 1)
    
    image = list(map(lambda x: vert_bord + x + vert_bord, image))
    
    return image

def get_code(patch):
    patch = "".join(patch)
    patch = "".join("0" if pixel == DARK else "1" for pixel in patch)
    code = int(patch, 2)
    return code

def get_patch(image, x, y, size):
    patch = [image[i] for i in range(x, x + size)]
    patch = list(map(lambda line: line[y:y+size], patch))
    return patch

def enhance(image, algo):
    eimage = []
    for i in range(len(image) - WINDOW_SIZE + 1):
        line = ""
        for j in range(len(image[0]) - WINDOW_SIZE + 1):
            patch = get_patch(image, i, j, WINDOW_SIZE)
            code = get_code(patch)
            line += algo[code]
        eimage.append(line)
    return eimage

def count_pixels(image):
    c = Counter()
    for line in image:
        c.update(line)
    return c[LIGHT]

def solve1(filename):
    algo, image = get_input(filename)
    print(algo)
    print(image)
    print()
    
    for i in range(ITER):
        image = border_up(image, DARK if algo[0] == DARK or i % 2 == 0 else LIGHT)
        image = enhance(image, algo)
    count = count_pixels(image)
    print(count)

def solve2(filename):
    solve1(filename)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
5944
"""
