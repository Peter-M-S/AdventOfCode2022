import os
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return [line.strip() for line in f.readlines()]


def height(i: int) -> int:
    if i == START:
        return ord("a")
    if i == END:
        return ord("z")
    if i in range(GRID_L):
        return ord(GRID[i])
    return ord("{")  # ASCII after "z" as out-of-grid marker


def breadth_first_search(start, end, is_part1) -> int:
    paths = [[start]]
    path_idx, visited = 0, {start}

    while path_idx < len(paths):
        actual_path = paths[path_idx]
        last_pos = actual_path[-1]
        for n in [R, U, D, L]:
            new_pos = last_pos + n
            if new_pos not in range(GRID_L): continue
            if (n == L and last_pos in LEFT_EDGE) or (n == R and last_pos in RIGHT_EDGE): continue
            if new_pos in visited: continue
            if is_part1 and (height(new_pos) - height(last_pos) > 1): continue
            if not is_part1 and (height(new_pos) - height(last_pos) < -1): continue
            if is_part1 and new_pos == end:
                return len(actual_path)
            # different condition for height diff for part 2
            if not is_part1 and height(new_pos) == ord("a"):
                return len(actual_path)
            paths.append((actual_path.copy() + [new_pos]))
            visited.add(new_pos)
        path_idx += 1
    return 10_000_000


file_name = os.path.basename(__file__)[:-3] + ".txt"
start_time = pfc()
data = read_puzzle(file_name)

# constants
GRID = "".join(data)
GRID_W = len(data[0])
GRID_L = len(GRID)
R, L = 1, -1
D, U = GRID_W, -GRID_W
START = GRID.index("S")
END = GRID.index("E")
LEFT_EDGE = [p for p in range(0, GRID_L, GRID_W)]
RIGHT_EDGE = [p for p in range(GRID_W - 1, GRID_L, GRID_W)]

part1 = breadth_first_search(START, END, True)
part2 = breadth_first_search(END, 1, False)

print(part1, part2)

print(pfc() - start_time)
