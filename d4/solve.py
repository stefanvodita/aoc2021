import sys

"""
{num: [(board, row, col)]}
rows[board][row]
cols[board][col]
"""

BOARD_SIZE = 5

def read_board(lines, board, hits, bags):
    for i, line in enumerate(lines):
        nums = list(map(int, filter(None, line.split(" "))))
        for j, num in enumerate(nums):
            t = (board, i, j)
            if num in hits:
                hits[num].append(t)
            else:
                hits[num] = [t]
            
            bags[board].add(num)

def get_input(filename):
    with open(filename, "r") as fin:
        s = fin.read()
    lines = s.split("\n")
    draw = list(map(int, lines[0].split(",")))
    
    hits = {}
    bags = []
    board = 0
    for i in range(2, len(lines) - 1, BOARD_SIZE + 1):
        bags.append(set())
        read_board(lines[i : i + BOARD_SIZE], board, hits, bags)
        board += 1

    print(hits)
    print(bags)
    return draw, hits, bags

def get_score(board, bags):
    score = 0
    for num in bags[board]:
        score += num
    return score

def solve1(filename):
    draw, hits, bags = get_input(filename)
    
    rows = [[0 for j in range(BOARD_SIZE)] for i in range(len(bags))]
    cols = [[0 for j in range(BOARD_SIZE)] for i in range(len(bags))]
    for num in draw:
        if num not in hits:
            continue
        for board, row, col in hits[num]:
            bags[board].remove(num)
            rows[board][row] += 1
            cols[board][col] += 1
            if rows[board][row] == BOARD_SIZE or cols[board][col] == BOARD_SIZE:
                score = get_score(board, bags) * num
                print(score)
                return

def solve2(filename):
    draw, hits, bags = get_input(filename)
    
    winers = [False for i in range(len(bags))]
    n_wins = 0
    rows = [[0 for j in range(BOARD_SIZE)] for i in range(len(bags))]
    cols = [[0 for j in range(BOARD_SIZE)] for i in range(len(bags))]
    for num in draw:
        if num not in hits:
            continue
        for board, row, col in hits[num]:
            if winers[board]:
                continue
            bags[board].remove(num)
            rows[board][row] += 1
            cols[board][col] += 1
            if rows[board][row] == BOARD_SIZE or cols[board][col] == BOARD_SIZE:
                winers[board] = True
                n_wins += 1
                if n_wins == len(bags):
                    score = get_score(board, bags) * num
                    print(score)
                    return

if __name__ == "__main__":
    if sys.argv[1] == "1":
        solve1(sys.argv[2])
    elif sys.argv[1] == "2":
        solve2(sys.argv[2])
    else:
        print("Bad command")

"""
<35217
<12341
8580
"""
