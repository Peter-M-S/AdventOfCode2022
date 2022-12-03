from time import perf_counter as pfc

WIN, DRAW, LOST = 6, 3, 0
ROCK, PAPER, SCISSORS = 1, 2, 3

# 0=draw, 1=first player wins, 2=second player wins
#  \ 2. R P S
# 1.
#  R    0 2 1
#  P    1 0 2
#  S    2 1 0
def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(puzzle):
    part1 = {"A X": ROCK + DRAW,
             "A Y": PAPER + WIN,
             "A Z": SCISSORS + LOST,
             "B X": ROCK + LOST,
             "B Y": PAPER + DRAW,
             "B Z": SCISSORS + WIN,
             "C X": ROCK + WIN,
             "C Y": PAPER + LOST,
             "C Z": SCISSORS + DRAW
             }
    part2 = {"A X": LOST + SCISSORS,
             "A Y": DRAW + ROCK,
             "A Z": WIN + PAPER,
             "B X": LOST + ROCK,
             "B Y": DRAW + PAPER,
             "B Z": WIN + SCISSORS,
             "C X": LOST + PAPER,
             "C Y": DRAW + SCISSORS,
             "C Z": WIN + ROCK
             }

    result = sum([part1[game] for game in puzzle]), sum([part2[game] for game in puzzle])
    return result


start = pfc()
print(solve(read_puzzle('day_02.txt')))
print(pfc() - start)
