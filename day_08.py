from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        lines = f.read().split("\n")
        return [[int(s) for s in line] for line in lines]


def is_visible(r, c):
    bench_mark = puzzle[r][c]
    left = max(puzzle[r][:c]) < bench_mark
    right = max(puzzle[r][c + 1:]) < bench_mark
    top = max(puzzleT[c][:r]) < bench_mark
    bottom = max(puzzleT[c][r + 1:]) < bench_mark
    return any([left, right, top, bottom])


def scenic_score(r, c):
    bench_mark = puzzle[r][c]
    to_top = max_distance(puzzleT[c][:r][::-1], bench_mark)  # reversed list to look against running r
    to_left = max_distance(puzzle[r][:c][::-1], bench_mark)  # reversed list to look against running c
    to_right = max_distance(puzzle[r][c + 1:], bench_mark)
    to_bottom = max_distance(puzzleT[c][r + 1:], bench_mark)
    return to_left * to_right * to_top * to_bottom


def max_distance(heights: list, bench_mark: int) -> int:
    distance = 0
    while distance < len(heights):
        distance += 1
        if heights[distance - 1] >= bench_mark:
            break
    return distance


def solve(puzzle):
    ROWS, COLS = len(puzzle), len(puzzleT)
    part1 = 2 * (ROWS - 1 + COLS - 1)  # trees at the edges are all visible   # loop through inside trees only
    part1 += sum([is_visible(r, c) for r in range(1, ROWS - 1) for c in range(1, COLS - 1)])
    part2 = max([scenic_score(r, c) for r in range(1, ROWS - 1) for c in range(1, COLS - 1)])
    # todo optimize by looping through inside trees only once for both parts?
    return part1, part2


start = pfc()
puzzle = read_puzzle('day_08.txt')
puzzleT = list(zip(*puzzle))  # transpose 2D list to easier look-up row slices
print(*solve(puzzle))
print(pfc() - start)
