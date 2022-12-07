from time import perf_counter as pfc


def get_dir_size(all_entries: dict, d: str):
    entries = all_entries[d]
    size = 0
    for f in entries:
        if f[0] in "1234567890":  # line with a file
            size += int(f.split()[0])
        if f[:4] == "dir ":  # line with a dir
            sub_dir = d + "/" + f[4:]
            size += get_dir_size(all_entries, sub_dir)
    return size


def get_entries(puzzle):
    entries = dict()
    current_dir = ""

    for line in puzzle:

        if line == '$ ls':
            continue

        if line == '$ cd ..':
            last_level = current_dir.rfind("/")
            current_dir = current_dir[:last_level]
        elif line == '$ cd /':
            current_dir = "/"
            entries[current_dir] = []
        elif line[:5] == '$ cd ':
            current_dir = current_dir + "/" + line[5:]
            entries[current_dir] = []

        if line[0] != '$':
            entries[current_dir].append(line)

    return entries


def read_puzzle(file):
    with open(file) as f:
        return f.read().split("\n")


def solve(puzzle):
    all_entries = get_entries(puzzle)

    dir_sizes = dict()
    for d in all_entries:
        dir_sizes[d] = get_dir_size(all_entries, d)

    part1 = 0
    for n in dir_sizes.values():
        if n <= 100_000:
            part1 += n

    min_space = 30_000_000
    free_space = 70_000_000 - dir_sizes["/"]
    part2 = 70_000_000
    for n in dir_sizes.values():
        if free_space + n >= min_space:
            part2 = min(part2, n)

    return part1, part2


start = pfc()
print(solve(read_puzzle('day_07.txt')))
print(pfc() - start)
