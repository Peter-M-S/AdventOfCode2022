from time import perf_counter as pfc

def read_puzzle(file, markersize):
    with open(file) as f:
        stream = f.read()
        i = 0
        while not len(set(stream[i:i+markersize])) == markersize:
            i += 1
    return i + markersize

def solve(puzzle):
    return puzzle

start = pfc()
print(solve(read_puzzle('day_06.txt', 4)))
print(solve(read_puzzle('day_06.txt', 14)))
print(pfc() - start)
