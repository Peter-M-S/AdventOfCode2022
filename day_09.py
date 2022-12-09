import os
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return [tuple([line.split()[0], int(line.split()[1])]) for line in f.readlines()]


def up(r, c): return r - 1, c


def down(r, c): return r + 1, c


def left(r, c): return r, c - 1


def right(r, c): return r, c + 1


MOVES = {"R": right, "U": up, "D": down, "L": left}


def move_tail(pos, pos_head):
    r, c = pos
    rh, ch = pos_head
    dr, dc = rh - r, ch - c
    # not moving
    if dr in [-1, 0, 1] and dc in [-1, 0, 1]:
        return pos

    # moving orthogonal
    if dr == 0:
        return (r, c + 1) if dc > 0 else (r, c - 1)
    if dc == 0:
        return (r + 1, c) if dr > 0 else (r - 1, c)

    # moving diagonal
    r = r + 1 if dr > 0 else r - 1
    c = c + 1 if dc > 0 else c - 1
    return r, c


def simulation(knots, puzzle):
    pos_knots = [(0, 0) for _ in range(knots)]
    tail_positions = {pos_knots[-1]}
    for RUDL, l in puzzle:
        for i in range(l):
            pos_knots[0] = MOVES[RUDL](*pos_knots[0])
            for k in range(1, knots):
                pos_knots[k] = move_tail(pos_knots[k], pos_knots[k - 1])
            tail_positions.add(pos_knots[-1])
    return len(tail_positions)


def solve(puzzle):
    return simulation(2, puzzle), simulation(10, puzzle)


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
