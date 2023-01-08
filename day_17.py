import os
from time import perf_counter as pfc

# positions of rock particles (r, c). rows counting upwards
rocks = [
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(2, 1), (1, 0), (1, 1), (1, 2), (0, 1)},
    {(2, 2), (1, 2), (0, 0), (0, 1), (0, 2)},
    {(3, 0), (2, 0), (1, 0), (0, 0)},
    {(1, 0), (1, 1), (0, 0), (0, 1)}
]

T = 1000000000000

LEFT, RIGHT, DOWN = (0, -1), (0, 1), (-1, 0)


def read_puzzle(file):
    with open(file) as f:
        return f.read().strip()


def show_chamber(fixed_rocks, rock, rock_top):
    for row in range(rock_top, 0, -1):
        print("|", end="")
        for col in range(7):
            if (row, col) in rock:
                s = "@"
            elif (row, col) in fixed_rocks:
                s = "#"
            else:
                s = "."
            print(s, end="")
        print("|")
    print("+-------+")
    print()


def move_rock(rock, move):
    rock = {(r + move[0], c + move[1]) for r, c in rock}
    left = min(c for _, c in rock)
    right = max(c for _, c in rock)
    bottom = min(r for r, _ in rock)
    top = max(r for r, _ in rock)
    return rock, left, right, bottom, top


def get_profile(fixed_rocks, height, depth=10):
    profile = [0] * 7
    profile_range = set((r, c) for r in range(height - depth, height + 1) for c in range(0, 7))
    top_rocks = profile_range & fixed_rocks
    for col in range(7):
        profile[col] = max([r[0] - (height - depth) for r in top_rocks if r[1] == col] + [profile[col]])
    return tuple(profile)


def solve(data, part1=False, part2=False):
    L = len(data)
    height = jet_count = rock_count = offset = 0
    fixed_rocks = set()

    states = {}  # key = (rock_index, jet_index, top_rocks profile) : value = (rock_count, height)

    while rock_count < T:
        rock_idx = rock_count % 5
        rock = rocks[rock_idx]

        origin = (height + 4, 2)
        rock, rock_left, rock_right, rock_bottom, rock_top = move_rock(rock, origin)

        # show_chamber(fixed_rocks, rock, rock_top)

        is_falling = True

        while is_falling:
            # step 1: jet
            jet_idx = jet_count % L
            jet = LEFT if data[jet_idx] == "<" else RIGHT
            test_rock, t_l, t_r, t_b, t_t = move_rock(rock, jet)
            if not (fixed_rocks & test_rock) and t_l >= 0 and t_r <= 6:
                rock, rock_left, rock_right, rock_bottom, rock_top = test_rock, t_l, t_r, t_b, t_t
            jet_count += 1

            # step 2: falling
            test_rock, t_l, t_r, t_b, t_t = move_rock(rock, DOWN)
            if not (fixed_rocks & test_rock) and t_b > 0:
                rock, rock_left, rock_right, rock_bottom, rock_top = test_rock, t_l, t_r, t_b, t_t
            else:
                is_falling = False
                fixed_rocks |= rock
                height = max(height, rock_top)
                key = (rock_idx, jet_idx, get_profile(fixed_rocks, height, 10))
                if key in states and not part2:
                    last_n, last_height = states[key]
                    rem_rocks = T - rock_count
                    repeats = rem_rocks // (rock_count - last_n)
                    offset = repeats * (height - last_height)
                    rock_count += repeats * (rock_count - last_n)
                    states = {}
                    part2 = True
                if not part2:
                    states[key] = (rock_count, height)
                rock_count += 1

        if rock_count == 2021:
            part1 = height

    part2 = height + offset
    return part1, part2


def main():
    file_name = os.path.basename(__file__)[:-3] + ".txt"
    start = pfc()
    print(*solve(read_puzzle(file_name)))
    print(pfc() - start)


if __name__ == '__main__':
    main()
