import sys

def solve1(filename):
    x = 0
    y = 0
    with open(filename, "r") as fin:
        s = fin.read()
    cmds = s.split("\n")
    print(cmds)
    for cmd in cmds:
        direction, distance = cmd.split(" ")
        if direction == "forward":
            x += int(distance)
        elif direction == "down":
            y += int(distance)
        elif direction == "up":
            y -= int(distance)
        else:
            print("Bad direction")
    print(x)
    print(y)
    print(x*y)

def solve2(filename):
    x = 0
    y = 0
    aim = 0
    with open(filename, "r") as fin:
        s = fin.read()
    cmds = s.split("\n")
    print(cmds)
    for cmd in cmds:
        direction, distance = cmd.split(" ")
        if direction == "forward":
            x += int(distance)
            y += aim * int(distance)
        elif direction == "down":
            aim += int(distance)
        elif direction == "up":
            aim -= int(distance)
        else:
            print("Bad direction")
    print(x)
    print(y)
    print(x*y)

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")
