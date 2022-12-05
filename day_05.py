import re
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        lines = f.read().split("\n")
        lines.remove("")
        levels = []
        stacks = []
        moves = []
        for line in lines:
            if "[" in line:
                levels.append("".join([line[s] for s in range(1, len(line), 4)]))
            elif "move" in line:
                moves.append(re.findall("\d+",line))
            else:
                stacks = "".join([line[s] for s in range(1, len(line), 4)])
    return levels, stacks,moves


def solve(puzzle):
    levels, stacks, moves = puzzle
    levels = list(reversed(levels))
    crates1 = dict()
    crates2 = dict()

    for stack in stacks:
        pile = "".join([level[int(stack)-1] for level in levels if int(stack) <= len(level)])
        crates1[stack] = pile.strip()
        crates2[stack] = pile.strip()

    for n, from_stack, to_stack in moves:
        crates2[to_stack] += crates2[from_stack][-int(n):]
        crates2[from_stack] = crates2[from_stack][:-int(n)]
        for i in range(int(n)):
            crates1[to_stack] += crates1[from_stack][-1]
            crates1[from_stack] = crates1[from_stack][:-1]

    part1 = "".join(p[-1] for p in crates1.values())
    part2 = "".join(p[-1] for p in crates2.values())

    return part1, part2


start = pfc()
print(solve(read_puzzle('day_05.txt')))
print(pfc() - start)
