from typing import Iterable, NamedTuple
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy
from itertools import count, product


class Step(NamedTuple):
    grid: list[list[int]]
    flashed: int


@dataclass
class Puzzle(PuzzleTemplate):
    grid: list[list[int]]
    width: int
    height: int

    def step(self, state: list[list[int]]) -> Step:
        grid = deepcopy(state)
        will_flash = set()
        flashed = set()

        # increase all energy levels by 1, memorize all that will flash
        for h in range(self.height):
            for w in range(self.width):
                grid[h][w] += 1
                if grid[h][w] > 9:
                    will_flash.add((h, w))

        while will_flash:
            h, w = will_flash.pop()
            flashed.add((h, w))
            for dh, dw in product([-1, 0, 1], repeat=2):
                neighbout_point = h + dh, w + dw
                if self.valid(neighbout_point):
                    # this also has the point itself, but it's in flashed so it won't trigger again
                    nh, nw = neighbout_point
                    grid[nh][nw] += 1
                    if grid[nh][nw] > 9 and neighbout_point not in flashed:
                        will_flash.add(neighbout_point)

        # set all that flashed back to energy level 0
        for h, w in flashed:
            grid[h][w] = 0

        return Step(grid=grid, flashed=len(flashed))

    def valid(self, point: tuple[int, int]) -> bool:
        h, w = point
        return 0 <= h < self.height and 0 <= w < self.width

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        grid = [[int(char) for char in line.strip()] for line in lines]

        return cls(grid=grid, height=len(grid), width=len(grid[0]))

    def task_one(self) -> int:
        grid = self.grid
        total_flashes = 0
        for i in range(1, 101):
            grid, flashed = self.step(grid)
            total_flashes += flashed

            if i % 10 == 0:
                print(f"After step {i}:")
                for row in grid:
                    print("".join(map(str, row)))
                print()

        return total_flashes

    def task_two(self) -> int:
        grid = self.grid
        for i in range(10_000_000):
            grid, flashed = self.step(grid)
            if flashed == self.width * self.height:  # detect all flashed at the same time
                return i + 1  # they expect us to start counting from 1 not 0
