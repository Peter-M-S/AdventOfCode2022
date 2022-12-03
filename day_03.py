from time import perf_counter as pfc

def prio(a: str) -> int:
    return ord(a) - 96 if a.islower() else ord(a) - (64-26)


def read_puzzle(file):
    with open(file) as f:
        puzzle = []
        for line in f.read().split("\n"):
            n = len(line)//2
            puzzle.append((line[:n], line[n:]))
        return puzzle


def solve(puzzle):
    part1 = []
    for compartment0, compartment1 in puzzle:
        a = set([prio(a) for a in compartment0]) & set([prio(a) for a in compartment1])
        part1.append(a.pop())

    part2 = []
    for i in range(0, len(puzzle), 3):
        group = set([prio(a) for a in puzzle[i][0] + puzzle[i][1]])
        for j in range(1, 3):
             group &= set([prio(a) for a in puzzle[i+j][0] + puzzle[i+j][1]])
        part2.append(group.pop())

    return sum(part1), sum(part2)


start = pfc()
print(solve(read_puzzle('day_03.txt')))
print(pfc() - start)
