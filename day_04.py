from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return [[[int(s) for s in elf.split("-")] for elf in pair.split(",")] for pair in f.read().split("\n")]


def solve(puzzle):
    part1 = part2 = 0
    for e0, e1 in puzzle:
        s0 = set(range(e0[0], e0[1]+1))
        s1 = set(range(e1[0], e1[1]+1))
        if s0.issubset(s1) or s1.issubset(s0):
            part1 += 1
        if s0 & s1:
            part2 += 1
    return part1, part2


start = pfc()

print(solve(read_puzzle('day_04.txt')))

print(pfc() - start)
