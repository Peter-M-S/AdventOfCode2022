from time import perf_counter as pfc


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(puzzle):
    a = {"A X": 4,
         "A Y": 8,
         "A Z": 3,
         "B X": 1,
         "B Y": 5,
         "B Z": 9,
         "C X": 7,
         "C Y": 2,
         "C Z": 6,
         }
    b = {"A X": 3,
         "A Y": 4,
         "A Z": 8,
         "B X": 1,
         "B Y": 5,
         "B Z": 9,
         "C X": 2,
         "C Y": 6,
         "C Z": 7,
         }

    result = sum([a[game] for game in puzzle]), sum([b[game] for game in puzzle])
    return result


start = pfc()
# print(read_puzzle('day_02.txt'))
print(solve(read_puzzle('day_02.txt')))
print(pfc() - start)
