from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt
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


def positions(grid):
    rows = len(grid)
    cols = len(grid[0])

    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = Point(r, c)
            elif grid[r][c] == "E":
                end = Point(r, c)
    return start, end


def main():
    lines = iter(stdin.read().strip().splitlines())

    grid = []
    for line in lines:
        if not line:
            break
        grid.append(list(line))

    start, goal = positions(grid)
    direction = Point(0, 1)

    queue = [(0, start, direction, None)]
    history = defaultdict(set)
    visited = dict()
    best_seats = set()
    best_cost = None
    while queue:
        # print(queue)
        cost, position, direction, previous = heappop(queue)

        if visited.get((position, direction), float("inf")) < cost:
            # print(f"Skipping {position}, {direction}")
            continue

        # print(f"Cost: {cost}, Position: {position}, Direction: {direction}")
        if best_cost and cost > best_cost:
            break

        visited[(position, direction)] = cost
        history[(position, direction)].add(previous)

        if position == goal:
            print(f"Found solution! {cost}")
            best_cost = cost

            foo = [(position, direction)]
            while foo:
                prev = foo.pop()
                if prev is None:
                    continue
                best_seats.add(prev[0])
                next_ = history[prev]
                if next_:
                    foo.extend(next_)

        r, c = position + direction
        try:
            if r < 0 or c < 0:
                raise IndexError
            if grid[r][c] in (".", "E", "S"):
                heappush(
                    queue,
                    (cost + 1, Point(r, c), direction, (position, direction)),
                )
        except IndexError:
            continue

        heappush(
            queue,
            (
                cost + 1000,
                position,
                direction.rotate_left(),
                (position, direction),
            ),
        )
        heappush(
            queue,
            (
                cost + 1000,
                position,
                direction.rotate_right(),
                (position, direction),
            ),
        )

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if Point(r, c) in best_seats:
                print("O", end="")
            else:
                print(grid[r][c], end="")
        print()

    print(f"Best seats: {len(best_seats)}")


if __name__ == "__main__":
    main()
