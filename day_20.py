import os
from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return list(map(int, f.read().split("\n")))


def solve(data):
    L = len(data)
    idx0 = data.index(0)
    indices = list(range(L))

    for i, n in enumerate(data):
        idx = indices.index(i)
        indices.pop(idx)
        new_i = (idx + n) % (L - 1)
        indices.insert(new_i, i)

    idx0 = indices.index(idx0)
    part1 = sum(data[indices[(idx0 + n) % L]] for n in (1000, 2000, 3000))

    data = [n * 811589153 for n in data]
    idx0 = data.index(0)
    indices = list(range(L))

    print(*data)

    for _ in range(10):
        for i, n in enumerate(data):
            idx = indices.index(i)
            indices.pop(idx)
            new_i = (idx + n) % (L - 1)
            indices.insert(new_i, i)

    idx0 = indices.index(idx0)
    part2 = sum(data[indices[(idx0 + n) % L]] for n in (1000, 2000, 3000))

    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
