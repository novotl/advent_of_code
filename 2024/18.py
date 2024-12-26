from collections import defaultdict
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


NEIGHBOURS = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]


def heuristics(point, width, height) -> int:
    return width - point.c + height - point.r


def run(grid, sim_length):
    height = len(grid)
    width = len(grid[0])

    start = Point(0, 0)
    goal = Point(height - 1, width - 1)
    queue = [(heuristics(start, width, height), 0, start, None)]
    openset = {start}
    visited = {}
    history = {}

    while queue:
        h, num_steps, pos, prev = heappop(queue)
        # print(num_steps)
        if pos in visited and visited[pos] < num_steps:
            continue

        visited[pos] = num_steps
        history[pos] = prev

        # print(f"{num_steps}: {pos}")
        if pos == goal:
            print(f"Goal reached after {num_steps} steps")
            break

        for delta in NEIGHBOURS:
            new = pos + delta
            nr, nc = new

            if new in visited:
                continue
            if new in openset:
                continue

            try:
                if nr < 0 or nc < 0:
                    raise IndexError
                type_, from_ = grid[nr][nc]
                # blocked
                if type_ == "#" and from_ <= sim_length:
                    # if type_ == "#" and from_ <= num_steps + 1:
                    continue
            except IndexError:
                continue

            # not blocked
            cost = num_steps + 1
            h = heuristics(start, width, height)
            heappush(queue, (h + cost, num_steps + 1, new, pos))
            openset.add(new)
    else:
        raise ValueError

    path = []
    prev = goal
    while prev is not None:
        path.append(prev)
        prev = history[prev]

    return path


def main():
    lines = iter(stdin.read().strip().splitlines())

    grid = []

    [width, height, sim_length] = map(int, next(lines).split(","))

    grid = [list((".", 0) for _ in range(width)) for _ in range(height)]

    for i, line in enumerate(lines, start=1):
        x, y = map(int, line.split(","))
        grid[y][x] = ("#", i)

    for i in count():
        pos = sim_length + i
        try:
            run(grid, pos)
        except ValueError:
            print(pos)
            break

    # for r in range(height):
    #     for c in range(width):
    #         if Point(r, c) in path:
    #             print("O", end="")
    #         else:
    #             type_, time_ = grid[r][c]
    #             if type_ == "#" and time_ <= sim_length:
    #                 print("#", end="")
    #             else:
    #                 print(".", end="")
    #     print()

    # print()
    # print("------")
    # print()


if __name__ == "__main__":
    main()
