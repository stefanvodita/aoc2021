import numpy as np
import pandas as pd
import sys

from collections import Counter
from math import ceil, floor
from statistics import mean

UNIQUE_LENS = [2, 3, 4, 7]
SEVEN_SEGMENT_MAPPING = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    data = []
    for line in s.split("\n"):
        signals, outputs = line.split("|")
        signals = signals.strip().split(" ")
        outputs = outputs.strip().split(" ")
        data.append((signals, outputs))
    return data

def count_unique_lens(data):
    n = 0
    for _, outputs in data:
        for output in outputs:
            if len(output) in UNIQUE_LENS:
                n += 1
    return n

def solve1(filename):
    data = get_input(filename)
    
    n = count_unique_lens(data)
    print(n)

def count_symbols(signals):
    c = Counter()
    for signal in signals:
        c.update(signal)
    return c

def get4(signals):
    for signal in signals:
        if len(signal) == 4:
            return signal

def in4(symbol, signals):
    return symbol in get4(signals)

def get7(signals):
    for signal in signals:
        if len(signal) == 3:
            return signal

def in7(symbol, signals):
    return symbol in get7(signals)

def get1(signals):
    for signal in signals:
        if len(signal) == 2:
            return signal

def in1(symbol, signals):
    return symbol in get1(signals)

def translate(signal, symbol_map):
    translation = ""
    for s in signal:
        translation += symbol_map[s]
    translation = "".join(sorted(translation))
    return SEVEN_SEGMENT_MAPPING[translation]

def sum_outs(signals, symbol_map):
    return int("".join(map(lambda signal: str(translate(signal, symbol_map)), signals)))

def solve2(filename):
    data = get_input(filename)
    ans = 0
    
    for signals, outputs in data:
        symbol_counts = count_symbols(signals)
        symbol_map = {}
        for symbol, count in symbol_counts.items():
            if count == 4:
                symbol_map[symbol] = "e"
            elif count == 6:
                symbol_map[symbol] = "b"
            elif count == 7:
                if in4(symbol, signals):
                    symbol_map[symbol] = "d"
                else:
                    symbol_map[symbol] = "g"
            elif count == 8:
                if in7(symbol, signals) and not in1(symbol, signals):
                    symbol_map[symbol] = "a"
                else:
                    symbol_map[symbol] = "c"
            elif count == 9:
                symbol_map[symbol] = "f"
        print(symbol_counts)
        print(symbol_map)
        
        ans += sum_outs(outputs, symbol_map)
    print(ans)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
1
317

101571337
"""
