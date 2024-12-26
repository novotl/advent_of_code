from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass

from operator import add, mul
from typing import Iterable


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

    def __str__(self):
        return f"({self.r}, {self.c})"

    def rotate_right(self):
        return Point(self.c, -self.r)


def project(a, b) -> list[Point]:
    return [
        (a + (a - b)),
        (b + (b - a)),
    ]


def project_part2(a, b, rows: int, cols: int) -> Iterable[Point]:
    for coeff in count(start=1):
        direction = a - b
        n = a + (direction * coeff)
        if n.r < 0 or n.r >= rows or n.c < 0 or n.c >= cols:
            return

        yield n


def main():
    lines = stdin.read().strip().splitlines()

    anthenas = defaultdict(list)

    rows = len(lines)
    cols = len(lines[0])

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != ".":
                anthenas[char].append(Point(r, c))

    antinodes = set()

    for freq, positions in anthenas.items():
        for a, b in combinations(positions, 2):
            # for antinode in project(a, b):
            #     if antinode.r < 0 or antinode.c < 0:
            #         continue
            #     if antinode.r >= rows or antinode.c >= cols:
            #         continue

            #     antinodes.add(antinode)
            # for antidote in :
            antinodes.update(project_part2(a, b, rows, cols))
            antinodes.update(project_part2(b, a, rows, cols))

    # for r, line in enumerate(lines):
    #     for c, char in enumerate(line):
    #         if char == ".":
    #             if Point(r, c) in antinodes:
    #                 print("#", end="")
    #             else:
    #                 print(".", end="")
    #         else:
    #             print(char, end="")
    #     print()

    for locations in anthenas.values():
        for loc in locations:
            antinodes.add(loc)

    print(len(antinodes))


if __name__ == "__main__":
    main()
