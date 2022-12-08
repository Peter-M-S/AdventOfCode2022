from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def is_visible(p, pT, r, c):
    left = max(p[r][:c]) < p[r][c]
    right = max(p[r][c + 1:]) < p[r][c]
    top = max(pT[c][:r]) < p[r][c]
    bottom = max(pT[c][r + 1:]) < p[r][c]
    return any([left, right, top, bottom])


def scenic_score(puzzle, puzzleT, r, c):
    bench_mark = int(puzzle[r][c])
    to_top = max_distance(puzzleT[c][:r][::-1], bench_mark)  # reversed list to look against running r
    to_left = max_distance(puzzle[r][:c][::-1], bench_mark)  # reversed list to look against running c
    to_right = max_distance(puzzle[r][c + 1:], bench_mark)
    to_bottom = max_distance(puzzleT[c][r + 1:], bench_mark)
    return to_left * to_right * to_top * to_bottom


def max_distance(heights: list[str], bench_mark: int) -> int:
    distance = 0
    while distance < len(heights):
        distance += 1
        if int(heights[distance - 1]) >= bench_mark:
            break
    return distance


def solve(puzzle):
    puzzleT = list(zip(*puzzle))        # transpose 2D list to easier look-up row slices

    part1 = 2 * (len(puzzle) - 1 + len(puzzle[0]) - 1)      # trees at the edges
    for r in range(1, len(puzzle) - 1):                     # loop thru inside trees only
        for c in range(1, len(puzzle[0]) - 1):
            part1 += is_visible(puzzle, puzzleT, r, c)

    part2 = []
    for r in range(1, len(puzzle) - 1):                     # loop thru inside trees only
        for c in range(1, len(puzzle[0]) - 1):
            part2.append(scenic_score(puzzle, puzzleT, r, c))

    return part1, max(part2)


start = pfc()
print(*solve(read_puzzle('day_08.txt')))
print(pfc() - start)
