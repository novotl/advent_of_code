from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from sys import stdin
import re
from dataclasses import dataclass

FREE = "."
OBSTACLE = "#"
GUARD_UP = "^"


class LoopException(ValueError): ...


@dataclass(frozen=True)
class Point:
    r: int
    c: int

    def __add__(self, p):
        return self.__class__(self.r + p.r, self.c + p.c)

    def __str__(self):
        return f"({self.r}, {self.c})"

    def rotate_right(self):
        return Point(self.c, -self.r)


class Grid:
    def __init__(self, grid: list[list[str]]):
        self.grid = deepcopy(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.visited = defaultdict(int)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == GUARD_UP:
                    self.guard_pos = Point(r, c)
                    self.guard_dir = Point(-1, 0)
                    self.initial_guard_pos = self.guard_pos
                    self.initial_guard_dir = self.guard_dir
                    self.grid[r][c] = FREE

    def get(self, p: Point):
        if p.r < 0 or p.c < 0:
            raise IndexError
        return self.grid[p.r][p.c]

    def check_loop(self):
        if self.visited[self.guard_pos] > 2:
            raise LoopException()

    def walk(self):
        while True:
            self.visited[self.guard_pos] += 1
            # print(self.guard_pos)

            next_ = self.guard_pos + self.guard_dir

            try:
                infront = self.get(next_)
                if infront == OBSTACLE:
                    self.guard_dir = self.guard_dir.rotate_right()
                    self.check_loop()
                    continue

                self.guard_pos = next_
                self.check_loop()

            except IndexError:
                return

    def print(self):
        for row in self.grid:
            print(row)

        print(f"Visited: {self.visited}")


def main():
    lines = stdin.read().strip().splitlines()

    raw_grid = []
    for line in lines:
        raw_grid.append(list(line.strip()))

    grid = Grid(raw_grid)
    grid.walk()

    loops = 0
    checked = set()
    for point in grid.visited.keys():
        dirs = [Point(0, 0), Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
        for dir_ in dirs:
            p = point + dir_
            if p in checked:
                continue

            try:
                grid.get(p)
                print(p)
                if raw_grid[p.r][p.c] == FREE:
                    raw_grid[p.r][p.c] = OBSTACLE
                    grid = Grid(raw_grid)
                    try:
                        grid.walk()
                    except LoopException:
                        loops += 1
                    raw_grid[p.r][p.c] = FREE
            except IndexError:
                continue
            finally:
                checked.add(p)
            
    # raw_grid[6][3] = OBSTACLE

    # grid = Grid(raw_grid)

    # grid.walk()
    # grid.print()
    # print(len(grid.visited))
    print(loops)

if __name__ == "__main__":
    main()
