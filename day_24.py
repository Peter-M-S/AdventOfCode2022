import os
from time import perf_counter as pfc

DIRECTIONS = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def move_blizzards(blizzards, h, w):
    return [[(r + dr) % h, (c + dc) % w, dr, dc] for r, c, dr, dc in blizzards]


def next_pos(r, c, h, w, target):
    np = {(r, c)}
    for d in DIRECTIONS.values():
        nr, nc = r + d[0], c + d[1]
        if (nr, nc) == target:
            return {(nr, nc)}
        if 0 <= nr < h and 0 <= nc < w:
            np.add((nr, nc))
    return np


def bfs(start_pos, h, w, end_pos, blizzards):
    result, t = [], 0

    for target in [end_pos, start_pos, end_pos]:
        q = {start_pos} if target == end_pos else {end_pos}

        while q:
            t += 1
            np = set()
            for r, c in q:
                np |= next_pos(r, c, h, w, target)
            blizzards = move_blizzards(blizzards, h, w)
            blizzards_pos = set((r, c) for r, c, _, _ in blizzards)
            q = np - blizzards_pos
            if target in q:
                result.append(t)
                break

    return result


def solve(data):
    grid = []
    for r, row in enumerate(data[1:-1]):
        grid_row = []
        for c, item in enumerate(row[1:-1]):
            grid_row.append(item)
        grid.append(grid_row)

    h, w = len(grid), len(grid[0])
    start_pos, end_pos = (-1, 0), (h, w - 1)
    blizzards = [[r, c, *DIRECTIONS[grid[r][c]]] for r in range(h) for c in range(w) if grid[r][c] not in ".#"]

    part1, _, part2 = bfs(start_pos, h, w, end_pos, blizzards)

    return part1, part2


def main():
    file_name = os.path.basename(__file__)[:-3] + ".txt"
    start = pfc()
    # print(*solve(read_puzzle("example.txt")))
    print(*solve(read_puzzle(file_name)))
    print(pfc() - start)


if __name__ == '__main__':
    main()
