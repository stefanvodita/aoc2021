import numpy as np
import pandas as pd
import sys

from collections import Counter
from functools import reduce
from math import ceil, floor
from operator import mul
from queue import PriorityQueue
from statistics import mean, median

class Packet:
    version = None
    typeid = None
    val = None
    subpackets = []
    
    def __str__(self):
        return self.val if self.val is not None else str(list(map(str, self.subpackets)))

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    # s = "9C0141080250320F1802104A08"
    s = "".join([bin(int(c, 16))[2:].zfill(4) for c in s])
    return s

def decode_literal(msg):
    print(msg)
    i = 0
    val = ""
    while msg[i] == "1":
        val += msg[i+1:i+5]
        i += 5
    val += msg[i+1:i+5]
    return val, msg[i+5:]

def decode_len_operator(msg):
    length = int(msg[:15], 2)
    
    rest_msg = msg[15+length:]
    msg = msg[15:15+length]
    
    children = []
    while msg:
        c, msg = decode(msg)
        children.append(c)
    return children, rest_msg

def decode_num_operator(msg):
    num = int(msg[:11], 2)
    
    msg = msg[11:]
    
    children = []
    for i in range(num):
        c, msg = decode(msg)
        children.append(c)
    return children, msg

def decode_operator(msg):
    if msg[0] == "0":
        return decode_len_operator(msg[1:])
    else:
        return decode_num_operator(msg[1:])

def decode(msg):
    p = Packet()
    p.version = int(msg[:3], 2)
    p.typeid = msg[3:6]
    
    if p.typeid == "100":
        p.val, msg = decode_literal(msg[6:])
    else:
        children, msg = decode_operator(msg[6:])
        p.subpackets = children
    return p, msg

def sum_versions(packet):
    sv = packet.version
    if packet.subpackets:
        for subpacket in packet.subpackets:
            sv += sum_versions(subpacket)
    return sv

def solve1(filename):
    msg = get_input(filename)
    print(msg)
    
    packet = decode(msg)[0]
    print(packet)
    
    sv = sum_versions(packet)
    print(sv)
    
def calculate(packet):
    if packet.typeid == "100":
        return int(packet.val, 2)
    elif packet.typeid == "000":
        return sum(map(calculate, packet.subpackets))
    elif packet.typeid == "001":
        return reduce(mul, map(calculate, packet.subpackets), 1)
    elif packet.typeid == "010":
        return min(map(calculate, packet.subpackets))
    elif packet.typeid == "011":
        return max(map(calculate, packet.subpackets))
    elif packet.typeid == "101":
        return 1 if calculate(packet.subpackets[0]) > calculate(packet.subpackets[1]) else 0
    elif packet.typeid == "110":
        return 1 if calculate(packet.subpackets[0]) < calculate(packet.subpackets[1]) else 0
    elif packet.typeid == "111":
        return 1 if calculate(packet.subpackets[0]) == calculate(packet.subpackets[1]) else 0 

def solve2(filename):
    msg = get_input(filename)
    print(msg)
    
    packet = decode(msg)[0]
    print(packet)
    
    val = calculate(packet)
    print(val)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""

"""
