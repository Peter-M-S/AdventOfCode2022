import os
import re
from time import perf_counter as pfc

'''
needed external hint to use product of all divisors to reduce items to smaller numbers which will follow the same path 
'''


class Monkey:
    all_divisors = 1

    def __init__(self, *args):
        self.id = args[0][0]
        self.items = args[1]
        self.operator = args[2][:2]
        self.operand = int(args[2][2:])
        self.divisor = args[3][0]
        self.to_false_true = (args[5][0], args[4][0])
        self.inspections = []

    def operation(self, n, part1):
        if self.operator == "* ":
            result = n * self.operand
        elif self.operator == "+ ":
            result = n + self.operand
        elif self.operator == "**":
            result = n ** 2
        else:
            result = 0
        return result // 3 if part1 else result


    def test(self, n):
        return not n % self.divisor

    def turn(self, monkeys, part1):
        for i in self.items[:]:
            self.inspections.append(i)
            self.items.remove(i)
            ##### this one line was hint from external
            i = i % self.all_divisors
            #####
            n = self.operation(i, part1)
            next_monkey = self.to_false_true[self.test(n)]
            monkeys[next_monkey].items.append(n)
        return monkeys


def read_puzzle(file):
    with open(file) as f:
        puzzle = []
        blocks = [block.split("\n") for block in f.read().split("\n\n")]
        for block in blocks:
            new_block = []
            for line in block:
                if "Operation" not in line:
                    new_block.append([int(s) for s in re.findall("\d+", line.strip())])
                else:
                    new_block.append((line[23:]))
            puzzle.append(new_block)
        return puzzle


def init_monkeys(puzzle):
    monkeys = []
    for block in puzzle:
        if "old" in block[2]:
            block[2] = "**0"
        monkeys.append(Monkey(*block))
    for m in monkeys:
        Monkey.all_divisors *= m.divisor
    return monkeys


def simulation(monkeys, part1, rounds):
    for r in range(1, rounds + 1):
        for m in monkeys:
            monkeys = m.turn(monkeys, part1)
        if not r % 1000:
            print(r)
            for m in monkeys:
                print(f"monkey {m.id}: {len(m.inspections)}")
    print()
    monkey_business = sorted([len(m.inspections) for m in monkeys])[-2:]
    monkey_business = monkey_business[-1] * monkey_business[-2]
    return monkey_business


def solve(file_name):
    puzzle = read_puzzle(file_name)
    monkeys = init_monkeys(puzzle)
    monkey_business_1 = simulation(monkeys, True, 20)

    puzzle = read_puzzle(file_name)
    monkeys = init_monkeys(puzzle)
    monkey_business_2 = simulation(monkeys, False, 10_000)

    return monkey_business_1, monkey_business_2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()

print(*solve(file_name))
print(pfc() - start)
