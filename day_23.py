from time import perf_counter as pfc
import os

N, S, W, E = -1, 1, -1, 1

NORTH = [(N, E), (N, 0), (N, W)]
SOUTH = [(S, E), (S, 0), (S, W)]
WEST = [(N, W), (0, W), (S, W)]
EAST = [(N, E), (0, E), (S, E)]
COMPASS = set(NORTH + SOUTH + WEST + EAST)

STRATEGY = [NORTH, SOUTH, WEST, EAST]


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def print_index(elves, mr, mc, Mr, Mc):
    for r in range(mr, Mr + 1):
        for c in range(mc, Mc + 1):
            s = str(elves.index((r, c))).center(4) if (r, c) in elves else " .. "
            print(s, end="")
        print(end="\n")


def print_grid(elves, mr, mc, Mr, Mc):
    for r in range(mr - 2, Mr + 3):
        for c in range(mc - 3, Mc + 3):
            s = "#" if (r, c) in elves else "."
            print(s, end="")
        print(end="\n")


def min_max_elves(elves):
    mr = mc = float("inf")
    Mr = Mc = -float("inf")
    for r, c in elves:
        mr, mc = min(mr, r), min(mc, c)
        Mr, Mc = max(Mr, r), max(Mc, c)
    return mr, mc, Mr, Mc


def solve(data):
    elves = []
    for r, line in enumerate(data):
        for c, s in enumerate(line):
            if s == "#":
                elves.append((r, c))
    elves_n = len(elves)
    strategy = STRATEGY
    # print_grid(elves, *min_max_elves(elves))
    part1 = part2 = turn = 0

    while True:
        turn += 1
        prop = []
        for r, c in elves:
            if all((r + dr, c + dc) not in elves for dr, dc in COMPASS):
                prop.append((r, c))
                continue

            for strat in strategy:
                if any((r + dr, c + dc) in elves for dr, dc in strat):
                    continue
                dr, dc = strat[1]
                prop.append((r + dr, c + dc))
                break
            else:
                prop.append((r, c))

        # print(prop)
        # print(len(prop))

        new_elves = []
        for i, p in enumerate(prop):
            if prop.count(p) > 1:
                new_elves.append(elves[i])
            else:
                new_elves.append(p)

        if elves == new_elves:
            part2 = turn
            break

        elves = new_elves[:]
        strategy = strategy[1:] + strategy[:1]

        # print(f"\nafter round {turn}:")
        # print_grid(elves, *min_max_elves(elves))

        if turn == 10:
            mr, mc, Mr, Mc = min_max_elves(elves)
            part1 = ((Mc + 1 - mc) * (Mr + 1 - mr)) - elves_n

        if turn > 1000:
            break

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"

start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
