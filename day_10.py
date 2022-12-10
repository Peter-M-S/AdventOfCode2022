from time import perf_counter as pfc
import os

def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(puzzle):
    cycle = x = 1
    sprite_position = [x-1, x, x+1]
    index = part1 = 0
    is_adding = False

    CRT = [["." for cycle in range(1, 41)] for row in range(6)]
    for r in CRT:
        print(*r)

    while index < len(puzzle):
        cmd = puzzle[index][:4]
        if cmd == "noop":
            index += 1
        else:
            if is_adding:
                x += int(puzzle[index][5:])

                is_adding = False
                index += 1
            else:
                is_adding = True

        col = (cycle - 1) % 40
        row = (cycle - 1) // 40
        CRT[row][col] = "#" if col in sprite_position else "."

        sprite_position = [x - 1, x, x + 1]
        cycle += 1


        if cycle in range(20,221,40):
            print(cycle, index, x, x*cycle)
            part1 += cycle*x

    part2 = "EHZFZHCZ"
    for r in CRT:
        print(*r)

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
