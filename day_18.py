from collections import deque
from time import perf_counter as pfc
import os

def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(data):
    cubes = set()
    for line in data:
        x, y, z = map(int, line.split(","))
        cubes.add((x,y,z))

    # sides are between coordinates
    offsets = [(0, 0, .5), (0, .5, 0), (.5, 0, 0),(0, 0, -.5), (0, -.5, 0), (-.5, 0, 0)]
    neighbors = [(0, 0, 1), (0, 1, 0), (1, 0, 0),(0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    mx = my = mz = float("inf")
    Mx = My = Mz = -float("inf")

    sides = {}
    for x, y, z in cubes:
        mx, my, mz = min(mx, x), min(my, y), min(mz, z)
        Mx, My, Mz = max(Mx, x), max(My, y), max(Mz, z)
        for dx, dy, dz in offsets:   # loop through all sides of x,y,z
            side  = (x+dx, y+dy, z+dz)
            if side not in sides:   # add new side to dict
                sides[side] = 0
            sides[side] += 1    # increase for each occurrence (if == 2 then this side belongs to two cubes = not open)
    part1 = sum(s for s in sides.values() if s == 1)

    # Part 2
    # define box just greater then cubes
    pos0 = (mx-1, my-1, mz-1)
    pos1 = (Mx+1, My+1, Mz+1)

    outside = {pos0}    # collect all grid points outside of cubes
    q = deque([pos0])   # queue for breadth first search

    while q:
        x, y, z = q.popleft()

        for dx, dy, dz in neighbors:
            nx, ny, nz = k  = (x+dx, y+dy, z+dz)
            if not(pos0[0] <= nx <= pos1[0] and pos0[1] <= ny <= pos1[1] and pos0[2] <= nz <= pos1[2]):
                # out of box
                continue
            if k in cubes or k in outside:
                # position is already visited or blocked by cube
                continue
            outside.add(k)
            q.append(k)     # keep as candidate for next level neighbors

    outside_sides = set()   # get all sides of outside grid points
    for  x, y, z in outside:
        for dx, dy, dz in offsets:
            outside_sides.add((x+dx, y+dy, z+dz))

    part2 = len(outside_sides & set(sides))  # intersection of all outside sides and cube sides

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
