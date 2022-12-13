from time import perf_counter as pfc
import os
import json

def read_puzzle(file):
    with open(file) as f:
        return [pair.split() for pair in f.read().split("\n\n")]


def is_left_lower_right(left, right) -> bool:
    if type(left) == int == type(right):
        return left < right
    if type(left) == list and type(right) == int:
        return is_left_lower_right(left, [right])
    if type(left) == int and type(right) == list:
        return is_left_lower_right([left], right)

    for i, l in enumerate(left):
        if i < len(right):
            r = right[i]
        else:
            return False
        if l == r:
            continue
        return is_left_lower_right(l, r)

    return True


def bubblesort(nlist):
    for j in range(len(nlist) - 1, 0, -1):
        for i in range(j):
            if is_left_lower_right(nlist[i], nlist[i + 1]):
                nlist[i], nlist[i + 1]  = nlist[i + 1], nlist[i]


def solve(data_raw):
    data = [[json.loads(left), json.loads(right)] for left, right in data_raw]

    # part1
    correct_pairs = []
    for p, (left, right) in enumerate(data):
        pair=p+1
        correct_pairs.append(is_left_lower_right(left, right) * pair)
    part1 = sum(correct_pairs)

    # part2
    dividers = [ [[2]], [[6]] ]
    all_packets = dividers[:]
    for p0, p1 in data:
        all_packets.append(p0)
        all_packets.append(p1)
    bubblesort(all_packets)
    all_packets = list(reversed(all_packets))
    part2 = (all_packets.index(dividers[0])+1) * (all_packets.index(dividers[1])+1)

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
