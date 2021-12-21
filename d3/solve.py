import sys

from collections import Counter

def bin2dec(bi):
    return int("".join(bi), 2)

def inverse(bi):
    return ["0" if b == "1" else "1" for b in bi]

def solve1(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    bins = s.split("\n")
    print(bins)
    bins = list(zip(*bins))
    print(bins)
    
    counts = [Counter(b) for b in bins]
    print(counts)
    
    gamma = ["0" if c["0"] > c["1"] else "1" for c in counts]
    print(gamma)
    
    epsilon = inverse(gamma)
    print(epsilon)
    
    gamma = bin2dec(gamma)
    epsilon = bin2dec(epsilon)
    print(gamma)
    print(epsilon)
    
    print(gamma * epsilon)

def get_gas(which, bins):
    indices = [i for i in range(len(bins[0]))]
    for i in range(len(bins)):
        bi = bins[i]
        c = Counter(bi)
        if which == "o2":
            indices = [i for i in range(len(bi)) if bi[i] == ("0" if c["0"] > c["1"] else "1")]
        else:
            indices = [i for i in range(len(bi)) if bi[i] == ("0" if c["0"] <= c["1"] else "1")]
        print(indices)
        bins = [[bi[i] for i in indices] for bi in bins]
        print(bins)
        if len(bins[0]) == 1:
            break
    print(list(zip(*bins)))
    return "".join(list(zip(*bins))[0])
    

def solve2(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    bins = s.split("\n")
    bins = list(zip(*bins))
    print(bins)
    
    o2 = get_gas("o2", bins)
    o2 = bin2dec(o2)
    print(o2)
    
    co2 = get_gas("co2", bins)
    co2 = bin2dec(co2)
    print(co2)
    
    print(o2 * co2)
    

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
10110
    2^1+2^2+2^4

01001
    2^0+2^3
"""