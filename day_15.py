import os
import re
from time import perf_counter as pfc


def read_data(file_name):
    pattern = re.compile(r"-?\d+")
    with open(file_name) as f:
        return [[eval(s) for s in pattern.findall(line)] for line in f.readlines()]


def solve_part1(data, target):
    sensor_ranges = dict()
    beacons = set()
    sensor_lx_hx = []
    for sx, sy, bx, by in data:
        d = abs(sx - bx) + abs(sy - by)
        sensor_ranges[(sx, sy)] = d
        beacons.add((bx, by))
        dy = d - abs(sy - target)
        if dy >= 0:
            sensor_lx_hx.append((sx - dy, sx + dy))

    sensor_lx_hx.sort()

    merge_intervals = []

    for lo, hi in sensor_lx_hx:
        if not merge_intervals:
            merge_intervals.append([lo, hi])  # this adds first interval (= most left lo)
            continue
        merge_lo, merge_hi = merge_intervals[-1]  # get last interval
        if lo > merge_hi + 1:  # new interval not overlapping or touching last interval
            merge_intervals.append([lo, hi])
            continue
        merge_intervals[-1][1] = max(merge_hi, hi)

    exclusions = 0  # counter for positions in non-overlapping intervals
    for lo, hi in merge_intervals:
        exclusions += hi + 1 - lo

    beacons_at_target = sum([1 for b in beacons if b[1] == target])  # counter of beacons on target line
    part1 = exclusions - beacons_at_target

    return part1


def solve_part2(data):
    sensor_ranges = dict()
    beacons = set()
    for sx, sy, bx, by in data:
        d = abs(sx - bx) + abs(sy - by)
        sensor_ranges[(sx, sy)] = d
        beacons.add((bx, by))

    for target in range(0, 4_000_001):
        sensor_lx_hx = []
        for (sx, sy), d in sensor_ranges.items():
            dy = d - abs(sy - target)
            if dy >= 0:
                sensor_lx_hx.append((sx - dy, sx + dy))
        sensor_lx_hx.sort()

        merge_intervals = []

        for lo, hi in sensor_lx_hx:
            if not merge_intervals:
                merge_intervals.append([lo, hi])  # this adds first interval (= most left lo)
                continue
            merge_lo, merge_hi = merge_intervals[-1]  # get last interval
            if lo > merge_hi + 1:  # new interval not overlapping or touching last interval
                merge_intervals.append([lo, hi])
                continue
            merge_intervals[-1][1] = max(merge_hi, hi)

        if len(merge_intervals) > 1:    # merged interval does not cover the entire line
            x = merge_intervals[0][1]+1
            part2 = x * 4_000_000 + target
            return part2

    return "not found"


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(solve_part1(read_data(file_name), 2_000_000))
print(solve_part2(read_data(file_name)))
print(pfc() - start)
