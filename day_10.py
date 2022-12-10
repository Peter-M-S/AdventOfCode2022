import os
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f: return f.read().split("\n")


def solve(puzzle):
    index = part1 = adding_completed = 0
    cycle = x = 1
    sprite_position = [x - 1, x, x + 1]

    CRT = [["." for cycle in range(1, 41)] for row in range(6)]

    while index < len(puzzle):
        if puzzle[index][:4] == "noop": index += 1
        else:
            if adding_completed:
                x += int(puzzle[index][5:])
                adding_completed = False
                index += 1
            else: adding_completed = True

        row, col = (cycle - 1) // 40, (cycle - 1) % 40
        CRT[row][col] = "#" if col in sprite_position else "."

        sprite_position = [x - 1, x, x + 1]
        cycle += 1

        if cycle in range(20, 221, 40): part1 += x * cycle

    for r in CRT: print(*r)

    part2 = "EHZFZHCZ"  # manual reading form screen, no character recognition

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
