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


def main():
    lines = stdin.read().strip().splitlines()

    grid = []
    for line in lines:
        grid.append(list(line))

    rows = len(grid)
    cols = len(grid[0])

    for row in grid:
        print(row)

    visited = set()

    area = []
    perimeter = []
    sides = []

    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited:
                continue

            print(f"{(row, col)}: {grid[row][col]}")
            area.append(0)
            perimeter.append(0)
            sides.append(defaultdict(list))
            queue = [(row, col)]

            while queue:
                r, c = queue.pop()
                if ((r, c)) in visited:
                    continue

                print(f"\t{(r, c)}")
                area[-1] += 1
                visited.add((r, c))

                for neighbour in [
                    (r, c - 1, "VL"),
                    (r, c + 1, "VR"),
                    (r - 1, c, "HB"),
                    (r + 1, c, "HT"),
                ]:
                    nr, nc, d = neighbour
                    try:
                        if nr < 0 or nc < 0:
                            raise IndexError
                        if grid[r][c] == grid[nr][nc]:
                            queue.append((nr, nc))
                        else:
                            perimeter[-1] += 1
                            sides[-1][d].append((nr, nc))

                    except IndexError:
                        perimeter[-1] += 1
                        sides[-1][d].append((nr, nc))

    # print(area)
    # print(perimeter)
    # print(sides)
    total_sizes = []

    for s in sides:
        print("SIDES COMPUTATION:")
        s["VL"].sort(key=lambda x: (x[1], x[0]))
        s["VR"].sort(key=lambda x: (x[1], x[0]))
        s["HT"].sort()
        s["HB"].sort()


        total_sides = 0

        print(s["VL"])
        prev = None
        for r, c in s["VL"]:
            if prev is None:
                prev = (r, c)
                print(f"\tVL + 1")
                total_sides += 1
                continue
            pr, pc = prev
            if pc == c and abs(r - pr) == 1:
                ...
            else:
                total_sides += 1
                print(f"\tVL + 1")
            prev = (r, c)

        
        print(s["VR"])
        prev = None
        for r, c in s["VR"]:
            if prev is None:
                prev = (r, c)
                print(f"\tVR + 1")
                total_sides += 1
                continue
            pr, pc = prev
            if pc == c and abs(r - pr) == 1:
                ...
            else:
                total_sides += 1
                print(f"\tVR + 1")
            prev = (r, c)

        print(s["HT"])
        prev = None
        for r, c in s["HT"]:
            if prev is None:
                prev = (r, c)
                total_sides += 1
                print(f"\t{(r, c)} HT + 1")
                continue
            pr, pc = prev
            if pr == r and abs(c - pc) == 1:
                ...
            else:
                total_sides += 1
                print(f"\t{(r, c)} HT + 1")
            prev = (r, c)

        print(s["HB"])
        prev = None
        for r, c in s["HB"]:
            if prev is None:
                prev = (r, c)
                total_sides += 1
                print(f"\t{(r, c)} HB + 1")
                continue
            pr, pc = prev
            if pr == r and abs(c - pc) == 1:
                ...
            else:
                total_sides += 1
                print(f"\t{(r, c)} HB + 1")
            prev = (r, c)

        print(f"\t{total_sides}")
        total_sizes.append(total_sides)
    
    # print(sides)
    # print(sum(a * p for a, p in zip(area, perimeter)))
    for a, s in zip(area, total_sizes):
        print(f"{a} * {s} = {a * s}")

    print(sum(a * s for a, s in zip(area, total_sizes)))


if __name__ == "__main__":
    main()
