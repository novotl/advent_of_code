from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass

from operator import add, mul


def part_1(start, grid):
    queue = [start]
    tops_reached = set()
    while queue:
        r, c = queue.pop()
        print((r, c))
        if grid[r][c] == 9:
            tops_reached.add((r, c))
            continue

        for neighbour in [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c)]:
            rn, cn = neighbour
            try:
                if rn < 0 or cn < 0:
                    raise IndexError
                if grid[r][c] + 1 == grid[rn][cn]:
                    queue.append((rn, cn))
            except IndexError:
                continue

    return len(tops_reached)


def part_2(start, grid):
    queue = [start]
    tops_reached = list()
    while queue:
        r, c = queue.pop()
        print((r, c))
        if grid[r][c] == 9:
            tops_reached.append((r, c))
            continue

        for neighbour in [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c)]:
            rn, cn = neighbour
            try:
                if rn < 0 or cn < 0:
                    raise IndexError
                if grid[r][c] + 1 == grid[rn][cn]:
                    queue.append((rn, cn))
            except IndexError:
                continue

    return len(tops_reached)


def main():
    lines = stdin.read().strip().splitlines()

    grid = []
    for line in lines:
        grid.append(list(map(int, line.strip())))

    res = 0
    for r, row in enumerate(grid):
        for c, level in enumerate(row):
            if level == 0:
                print((r, c))
                # res += part_1((r, c), grid)
                res += part_2((r, c), grid)

    for r in grid:
        print(r)

    print(res)


if __name__ == "__main__":
    main()
