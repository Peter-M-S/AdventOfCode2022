import os
import re
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        grid, instructions = f.read().split("\n\n")
        grid = [line for line in grid.split("\n")]
        return grid, instructions


def print_grid(grid):
    for line in grid:
        print(line)


def get_block(r, c, cube):
    for i, b in enumerate(cube):
        if (r, c) in b:
            return i


def solve(data):
    grid, instructions = data
    max_col = max(len(r) for r in grid)
    # fill all rows until max-col
    for i, r in enumerate(grid):
        while len(grid[i]) < max_col:
            grid[i] = grid[i] + " "

    # print_grid(grid)

    # edges dicts: key= row/col, value(top/left edge pos, right/bottom pos)
    row_edges = dict((i, [0, len(r) - 1]) for i, r in enumerate(grid))
    for ri, r in enumerate(grid):
        left = False
        for ci, s in enumerate(r):
            if s == " ":
                continue
            if not left:
                row_edges[ri][0] = ci
                left = True
            row_edges[ri][1] = ci

    col_edges = dict((j, [0, len(grid) - 1]) for j in range(max_col))
    for ci in range(max_col):
        top = False
        for ri in range(len(grid)):
            if grid[ri][ci] == " ":
                continue
            if not top:
                col_edges[ci][0] = ri
                top = True
            col_edges[ci][1] = ri

    facing = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}

    # part1
    r = 0
    c = grid[r].index(".")
    dr, dc = 0, 1

    for steps, turn in re.findall(r"(\d+)([RL]?)", instructions):
        for s in range(int(steps)):
            nr = r + dr
            nc = c + dc
            if dc:
                if nc > row_edges[nr][1]:
                    nc = row_edges[nr][0]
                elif nc < row_edges[nr][0]:
                    nc = row_edges[nr][1]
            if dr:
                if nr > col_edges[nc][1]:
                    nr = col_edges[nc][0]
                elif nr < col_edges[nc][0]:
                    nr = col_edges[nc][1]

            if grid[nr][nc] == "#":
                break
            else:
                r, c = nr, nc

        if turn == "R":
            dr, dc = dc, -dr
        if turn == "L":
            dr, dc = -dc, dr

    part1 = (r + 1) * 1000 + (c + 1) * 4 + facing[(dr, dc)]

    # part2
    r = 0
    c = grid[r].index(".")
    dr, dc = 0, 1
    for steps, turn in re.findall(r"(\d+)([RL]?)", instructions):
        steps = int(steps)
        for s in range(steps):
            cdr, cdc = dr, dc
            nr = r + dr
            nc = c + dc
            # edge 1
            if 50 <= nr < 100 and nc == 49 and dc == -1:
                dr, dc = 1, 0
                nr, nc = 100, nr - 50
            elif nr == 99 and 0 <= nc < 50 and dr == -1:
                dr, dc = 0, 1
                nr, nc = 50 + nc, 50
            # edge 2
            elif 0 <= nr < 50 and nc == 49 and dc == -1:
                dr, dc = 0, 1
                nr, nc = 149 - nr, 0
            elif 100 <= nr < 150 and nc == -1 and dc == -1:
                dr, dc = 0, 1
                nr, nc = 149 - nr, 50
            # edge 3
            elif nr == 50 and 100 <= nc < 150 and dr == 1:
                dr, dc = 0, -1
                nr, nc = nc - 50, 99
            elif 50 <= nr < 100 and nc == 100 and dc == 1:
                dr, dc = -1, 0
                nr, nc = 49, nr + 50
            # edge 4
            elif nr == 150 and 50 <= nc < 100 and dr == 1:
                dr, dc = 0, -1
                nr, nc = nc + 100, 49
            elif 150 <= nr < 200 and nc == 50 and dc == 1:
                dr, dc = -1, 0
                nr, nc = 149, nr - 100
            # edge 5
            elif 0 <= nr < 50 and nc == 150 and dc == 1:
                dr, dc = 0, -1
                nr, nc = 149 - nr, 99
            elif 100 <= nr < 150 and nc == 100 and dc == 1:
                dr, dc = 0, -1
                nr, nc = 149 - nr, 149
            # edge 6
            elif nr == -1 and 100 <= nc < 150 and dr == -1:
                dr, dc = -1, 0
                nr, nc = 199, nc - 100
            elif nr == 200 and 0 <= nc < 50 and dr == 1:
                dr, dc = 1, 0
                nr, nc = 0, nc + 100
            # edge 7
            elif nr == -1 and 50 <= nc < 100 and dr == -1:
                dr, dc = 0, 1
                nr, nc = nc + 100, 0
            elif 150 <= nr < 200 and nc == -1 and dc == -1:
                dr, dc = 1, 0
                nr, nc = 0, nr - 100

            if grid[nr][nc] == "#":
                dr, dc = cdr, cdc
                break
            r, c = nr, nc

        if turn == "R":
            dr, dc = dc, -dr
        if turn == "L":
            dr, dc = -dc, dr

    part2 = (r + 1) * 1000 + (c + 1) * 4 + facing[(dr, dc)]

    return part1, part2


def main():
    file_name = os.path.basename(__file__)[:-3] + ".txt"
    start = pfc()
    print(*solve(read_puzzle(file_name)))
    print(pfc() - start)


if __name__ == '__main__':
    main()
