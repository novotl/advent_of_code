from collections import Counter, defaultdict
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt, truediv
from typing import Iterable
from PIL import Image
import numpy as np
from tqdm import tqdm
from heapq import heappush, heappop


@dataclass(frozen=True)
class Point:
    r: int
    c: int

    def __add__(self, p):
        return self.__class__(self.r + p.r, self.c + p.c)

    def __sub__(self, p):
        return self.__class__(self.r - p.r, self.c - p.c)

    def __mul__(self, coef):
        return self.__class__(self.r * coef, self.c * coef)

    def __lt__(self, other):
        return (self.r, self.c) < (other.r, other.c)

    def mod(self, x, y):
        return self.__class__(self.r % x, self.c % y)

    def __str__(self):
        return f"({self.r}, {self.c})"

    def __iter__(self):
        return iter((self.r, self.c))

    def rotate_right(self):
        return Point(self.c, -self.r)

    def rotate_left(self):
        return Point(-self.c, self.r)

    def manhattan(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


NEIGHBOURS = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]


def initialize(lines):
    grid = [list(line) for line in lines]
    rows = len(grid)
    cols = len(grid[0])

    start = None
    goal = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = Point(r, c)
            elif grid[r][c] == "E":
                goal = Point(r, c)

    return rows, cols, grid, start, goal


def run(grid, start: Point, goal: Point):
    height = len(grid)
    width = len(grid[0])

    # Heuristics, cost, point, prev
    queue = [(start.manhattan(goal), 0, start, None)]
    openset = {start}
    visited = {}
    history = {}

    while queue:
        h, cost, pos, prev = heappop(queue)
        if pos in visited and visited[pos] < cost:
            continue

        visited[pos] = cost
        history[pos] = prev

        if pos == goal:
            print(f"Goal reached with cost {cost}")
            break

        for delta in NEIGHBOURS:
            new_pos = pos + delta
            nr, nc = new_pos

            if new_pos in visited:
                continue
            if new_pos in openset:
                continue

            try:
                if nr < 0 or nc < 0:
                    raise IndexError
                if grid[nr][nc] == "#":
                    # blocked
                    continue
            except IndexError:
                continue

            # not blocked
            h = new_pos.manhattan(goal)
            heappush(queue, (h + cost, cost + 1, new_pos, pos))
            openset.add(new_pos)
    else:
        raise ValueError

    path = []
    prev = goal
    while prev is not None:
        path.append(prev)
        prev = history[prev]

    return list(reversed(path))


def main():
    lines = iter(stdin.read().strip().splitlines())
    cheat_threshold = 20
    savings_threshold = 100
    rows, cols, grid, start, goal = initialize(lines)

    path = run(grid, start, goal)

    # for r in range(rows):
    #     for c in range(cols):
    #         if Point(r, c) in path:
    #             print("O", end="")
    #         else:
    #             print(grid[r][c], end="")
    #     print("")

    # print(f"Start: {start}")
    # print(f"Goal: {goal}")
    # print(path)

    savings = Counter()

    path_len = len(path)
    for start_i in range(path_len):
        for end_i in range(start_i + 1, path_len):
            start = path[start_i]
            end = path[end_i]

            dist = start.manhattan(end)
            if 2 <= dist <= cheat_threshold:
                saving = end_i - start_i - dist
                # print(f"{start} -> {end}: {saving}")
                if saving:
                    savings[saving] += 1

    pprint(sorted(savings.items()))

    print(sum(num for saving, num in savings.items() if saving >= savings_threshold))


if __name__ == "__main__":
    main()
