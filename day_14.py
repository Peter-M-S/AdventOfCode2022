from time import perf_counter as pfc
import os

def read_puzzle(file):
    with open(file) as f:
        scans = [scan.split(" -> ") for scan in f.read().split("\n")]
        lines =[[eval(p) for p in scan] for scan in scans]
        return lines

def solve(data, is_part1):
    top = 0
    left  = min([min([a[0] for a in line]) for line in data])
    right = max([max([a[0] for a in line]) for line in data])
    bottom = max([max([a[1] for a in line]) for line in data])
    grid = dict([((x, y), ".") for x in range(left, right+1) for y in range(top, bottom+1)])

    if not is_part1:
        bottom += 2
        for x in range(left, right + 1):
            grid[(x, bottom - 1)] = "."
            grid[(x, bottom)] = "#"

    start = (500, 0)
    grid[start] = "+"

    # find line_points
    line_points = set()
    for line in data:
        for idx, (x0, y0) in enumerate(line[:-1]):
            x1, y1 = line[idx + 1]
            if x0 > x1:
                x0, x1 = x1, x0
            if y0 > y1:
                y0, y1 = y1, y0
            for i in range(x0, x1 + 1):
                for j in range(y0, y1 + 1):
                    line_points.add((i, j))

    # add lines into grid
    for p in line_points:
        grid[p] = "*"

    # draw grid
    for y in range(top, bottom+1):
        for x in range(left, right+1):
            print(grid[(x, y)], end="")
        print(end="\n")

    part1 = last_part1 = 0
    while True:
        x, y = start
        is_moving = True
        while is_moving and y < bottom:
            if (x-1,top) not in grid:
                for _y in range(top, bottom):
                    grid[(x-1, _y)] = "."
                grid[(x-1, bottom)] = "#"
                left -= 1
            if (x+1,top) not in grid:
                for _y in range(top, bottom):
                    grid[(x+1, _y)] = "."
                grid[(x+1, bottom)] = "#"
                right += 1
            if grid[(x, y + 1)] == ".":
                y += 1
            elif grid[(x - 1, y + 1)] == ".":
                x -= 1
                y += 1
            elif grid[(x + 1, y + 1)] == ".":
                x += 1
                y += 1
            else:
                grid[(x, y)] = "o"
                is_moving = False
                part1 += 1
                # if not part1 % 5_000:
                #     print(part1)

        if last_part1 == part1 or (not is_part1 and (x,y) == start):
            break
        last_part1 = part1

    # draw grid
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            print(grid[(x, y)], end="")
        print(end="\n")

    return part1

file_name = os.path.basename(__file__)[:-3] + ".txt"
start_time = pfc()
print(solve(read_puzzle(file_name), True))
print(solve(read_puzzle(file_name), False))
print(pfc() - start_time)
