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

    def mod(self, x, y):
        return self.__class__(self.r % x, self.c % y)

    def __str__(self):
        return f"({self.r}, {self.c})"

    def __iter__(self):
        return iter((self.r, self.c))

    def rotate_right(self):
        return Point(self.c, -self.r)


MOVES = {">": Point(0, 1), "<": Point(0, -1), "v": Point(1, 0), "^": Point(-1, 0)}


# def step(grid, player, move) -> bool:
#     nr, nc = player + move
#     if grid[nr][nc] == "#":
#         # wall, cannot move
#         return False

#     if grid[nr][nc] == ".":
#         # empty, can move
#         r, c = player
#         grid[nr][nc] = grid[r][c]
#         grid[r][c] = "."
#         return True

#     # box -> attempt move box
#     if grid[nr][nc] == "O":
#         if step(grid, Point(nr, nc), move):
#             # box was moved
#             r, c = player
#             grid[nr][nc] = grid[r][c]
#             grid[r][c] = "."
#             return True
#         else:
#             # box was not moved
#             return False
#     assert False


def main():
    lines = iter(stdin.read().strip().splitlines())

    grid = []
    for line in lines:
        if not line:
            break
        grid.append(list(line))
    moves = list(chain(*lines))

    rows = len(grid)
    cols = len(grid[0])

    player = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                player = Point(r, c)
                break

    for str_move in moves:
        print(f"Move: {str_move}")
        move = MOVES[str_move]
        if step(grid, player, move):
            player += move

        # for row in grid:
        #     print(row)
        # print("----")

    res = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "O":
                res += 100 * r + c

    print(res)


def new_map(grid):
    new_grid = []
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        new_grid.append([])
        for c in range(cols):
            cell = grid[r][c]
            if cell == "#":
                new_grid[-1].append("#")
                new_grid[-1].append("#")
            if cell == "O":
                new_grid[-1].append("[")
                new_grid[-1].append("]")
            if cell == ".":
                new_grid[-1].append(".")
                new_grid[-1].append(".")
            if cell == "@":
                new_grid[-1].append("@")
                new_grid[-1].append(".")

    return new_grid


def swap(grid, player, move) -> bool:
    nr, nc = player + move
    r, c = player
    if grid[nr][nc] == ".":
        grid[nr][nc] = grid[r][c]
        grid[r][c] = "."
    elif move in [MOVES["<"], MOVES[">"]] and grid[nr][nc] in ["[", "]"]:
        swap(grid, Point(nr, nc), move)
        grid[nr][nc] = grid[r][c]
        grid[r][c] = "."
    elif move in [MOVES["^"], MOVES["v"]] and grid[nr][nc] in ["["]:
        swap(grid, Point(nr, nc), move)
        swap(grid, Point(nr, nc + 1), move)
        # swap(grid, Point(r, c + 1), move)
        grid[nr][nc] = grid[r][c]
        grid[r][c] = "."
    elif move in [MOVES["^"], MOVES["v"]] and grid[nr][nc] in ["]"]:
        swap(grid, Point(nr, nc), move)
        swap(grid, Point(nr, nc - 1), move)
        # swap(grid, Point(r, c - 1), move)
        grid[nr][nc] = grid[r][c]
        grid[r][c] = "."
    else:
        assert False


def step2(grid, player, move) -> bool:
    nr, nc = player + move
    if grid[nr][nc] == "#":
        # wall, cannot move
        return False

    if grid[nr][nc] == ".":
        # empty, can move
        return True

    # box -> attempt move box
    if move in [MOVES["<"], MOVES[">"]] and grid[nr][nc] in ["[", "]"]:
        # move left & right
        if step2(grid, Point(nr, nc), move):
            # box was moved
            return True
        else:
            # box was not moved
            return False

    if move in [MOVES["^"], MOVES["v"]] and grid[nr][nc] in ["["]:
        if step2(grid, Point(nr, nc), move) and step2(grid, Point(nr, nc + 1), move):
            # box was moved
            return True
        else:
            # box was not moved
            return False

    if move in [MOVES["^"], MOVES["v"]] and grid[nr][nc] in ["]"]:
        if step2(grid, Point(nr, nc), move) and step2(grid, Point(nr, nc - 1), move):
            # box was moved
            return True
        else:
            # box was not moved
            return False

    assert False


def main2():
    lines = iter(stdin.read().strip().splitlines())

    grid = []
    for line in lines:
        if not line:
            break
        grid.append(list(line))
    moves = list(chain(*lines))

    grid = new_map(grid)

    rows = len(grid)
    cols = len(grid[0])

    player = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                player = Point(r, c)
                break

    for str_move in moves:
        print(f"Move: {str_move}")
        move = MOVES[str_move]
        if step2(grid, player, move):
            swap(grid, player, move)
            player += move

        # for row in grid:
        #     print(row)
        # print("----")

    res = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "[":
                res += 100 * r + c

    print(res)


if __name__ == "__main__":
    main2()
