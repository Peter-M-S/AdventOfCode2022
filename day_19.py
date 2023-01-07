from time import perf_counter as pfc
import os
import re
from collections import deque

pattern = re.compile(r"\d+")


def quality_heuristic(state):
    mined = state[3]
    return 1000 * mined[3] + 100 * mined[2] + 10 * mined[1] + mined[0]


def bfs(blueprint, robots, max_minutes, max_q=8000):
    # returns max geodes
    max_geodes_mined = 0
    bp_id, cost_ore_robo, cost_clay_robo, cost_obsi_robo1, cost_obsi_robo2, cost_geode_robo1, cost_geode_robo2 = blueprint
    costs = [(cost_ore_robo, 0, 0, 0), (cost_clay_robo, 0, 0, 0), (cost_obsi_robo1, cost_obsi_robo2, 0, 0),
             (cost_geode_robo1, 0, cost_geode_robo2, 0)]

    # initial queue for bfs, defining time, robots, actual inventory, mined items. queue is list of states
    # queue = deque([(0, robots, (0, 0, 0, 0), (0, 0, 0, 0))])
    queue = [(0, robots, (0, 0, 0, 0), (0, 0, 0, 0))]
    depth = 0
    while queue:
        # minutes, robots, inventory, mined = queue.popleft()
        minutes, robots, inventory, mined = queue.pop(0)

        # continue only with the states of best quality
        # todo number of bests is freely chosen, but can not cover safely global maximum
        if minutes > depth:
            queue = sorted(queue, key=quality_heuristic, reverse=True)[:max_q]
            depth = minutes

        # at end of search path get next entry of queue, until queue is empty, to find and return overall max.
        if minutes == max_minutes:
            max_geodes_mined = max(max_geodes_mined, mined[3])
            continue

        # harvest of existing robots
        newly_mined = [mined[i] + robots[i] for i in range(4)]

        for i in range(4):
            cost_robo = costs[i]

            if all([inventory[j] >= cost_robo[j] for j in range(4)]):
                # always buy a robot if enough cost
                # buying too many ore robots - yes, but reduce search path by quality_heuristic
                new_robots = list(robots)
                new_robots[i] += 1
                new_inventory = [inventory[j] - cost_robo[j] + robots[j] for j in range(4)]
                queue.append((minutes + 1, new_robots, new_inventory, newly_mined))

        new_inventory = [inventory[i] + robots[i] for i in range(4)]
        queue.append((minutes + 1, robots, new_inventory, newly_mined))
    return max_geodes_mined


def read_puzzle(file):
    with open(file) as f:
        blocks = f.read().split("\n")
        blueprints = []
        for block in blocks:
            blueprints.append(list(map(int, pattern.findall(block))))
        return blueprints


def solve(data):
    part1 = 0
    robots = (1, 0, 0, 0)  # ore robo, clay robo, obsi robo, geode robo
    # why starts robots as a tuple- to start with same immutable tuple for part 2
    part1 = sum([bp[0] * bfs(bp, robots, 24) for bp in data])
    part2 = 1
    for bp in data[:3]:
        a = bfs(bp, robots, 32)
        # print(a)
        part2 *= a
    return part1, part2


file_name = os.path.basename(__file__)[:-3] + ".txt"
start = pfc()
print(*solve(read_puzzle(file_name)))
print(pfc() - start)
