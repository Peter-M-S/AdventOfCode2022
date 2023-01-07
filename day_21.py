from time import perf_counter as pfc
import os
import sympy


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def get_number(name, monkeys):
    if isinstance(monkeys[name], sympy.Symbol):
        return monkeys[name]
    if type(monkeys[name]) == int:
        return monkeys[name]
    n0, op, n1 = monkeys[name]
    return eval(f"get_number(n0, monkeys) {op} get_number(n1, monkeys)")


def solve(data):
    monkeys = {}
    for line in data:
        name, value = line.split(": ")
        if value.isdigit():
            monkeys[name] = int(value)
        else:
            a = value.strip()
            monkeys[name] = (a.split())

    part1 = int(get_number("root", monkeys))

    # check if const. slope - nope!
    # sympy install

    monkeys["humn"] = sympy.Symbol("x")
    left, op, right = monkeys["root"]
    part2 = sympy.solve((get_number(left, monkeys) - get_number(right, monkeys)), sympy.Symbol("x"))

    return part1, int(part2[0])


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
