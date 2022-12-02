from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return f.read()


def solve(puzzle):
    result = puzzle
    return result


start = pfc()
print(solve(read_puzzle('day_03.txt')))
print(pfc() - start)
