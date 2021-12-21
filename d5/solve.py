import sys

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    lines = s.split("\n")
    
    vents = []
    sizex = 0
    sizey = 0
    for line in lines:
        p1, _, p2 = line.split(" ")
        y1, x1 = list(map(int, p1.split(",")))
        y2, x2 = list(map(int, p2.rstrip().split(",")))
        vents.append((x1, y1, x2, y2))
        
        if x1 > sizex:
            sizex = x1
        if x2 > sizex:
            sizex = x2
        if y1 > sizey:
            sizey = y1
        if y2 > sizey:
            sizey = y2
    return vents, sizex + 1, sizey + 1

def put1(field, x1, y1, x2, y2):
    if x1 == x2:
        x = x1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            field[x][y] += 1
    elif y1 == y2:
        y = y1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            field[x][y] += 1
    else:
        pass

def put2(field, x1, y1, x2, y2):
    if x1 == x2:
        x = x1
        for y in range(min(y1, y2), max(y1, y2) + 1):
            field[x][y] += 1
    elif y1 == y2:
        y = y1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            field[x][y] += 1
    else:
        x = x1
        y = y1
        ix = 1 if x1 < x2 else -1
        iy = 1 if y1 < y2 else -1
        for _ in range(min(x1, x2), max(x1, x2) + 1):
            field[x][y] += 1
            x += ix
            y += iy

def solve1(filename):
    vents, sizex, sizey = get_input(filename)
    
    field = [[0 for i in range(sizey)] for j in range(sizex)]
    for x1, y1, x2, y2 in vents:
        put1(field, x1, y1, x2, y2)
    
    n_vents = 0
    for i in range(sizex):
        for j in range(sizey):
            if field[i][j] > 1:
                n_vents += 1
    print(n_vents)

def solve2(filename):
    vents, sizex, sizey = get_input(filename)
    
    field = [[0 for i in range(sizey)] for j in range(sizex)]
    for x1, y1, x2, y2 in vents:
        put2(field, x1, y1, x2, y2)
    print(field)
    
    n_vents = 0
    for i in range(sizex):
        for j in range(sizey):
            if field[i][j] > 1:
                n_vents += 1
    print(n_vents)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
6283
"""
