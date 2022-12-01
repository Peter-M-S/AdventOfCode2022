from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(puzzle):
    result = []
    count = 0
    for n in puzzle:
        if n:
            count += int(n)
        else:
            result.append(count)
            count = 0
    result = sorted(result, reverse=True)
    return result[0], sum(result[:3])


start = pfc()
print(*solve(read_puzzle('day_01.txt')))
print(pfc() - start)
