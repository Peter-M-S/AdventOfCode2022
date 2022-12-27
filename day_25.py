from time import perf_counter as pfc
import os


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


digits = {'2': 2,
          '1': 1,
          '0': 0,
          '-': -1,
          '=': -2}


def snafu2int(n5):
    n10 = 0
    for i, x in enumerate(n5[::-1]):
        n10 += digits[x] * 5 ** i
    return n10


def int2snafu(n10):
    n5 = ""
    while n10:
        remainder = n10 % 5
        n10 //= 5

        if remainder <= 2:
            n5 = str(remainder) + n5
        else:  # carry over to next digit
            n5 = "   =-"[remainder] + n5
            n10 += 1
    return n5


def solve(data):
    part1 = 0
    for line in data:
        part1 += snafu2int(line)

    part1 = int2snafu(part1)
    return part1


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(solve(read_puzzle(file_name)))
print(pfc() - start)
