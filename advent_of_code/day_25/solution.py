from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy

Grid = list[list[str]]


@dataclass
class Puzzle(PuzzleTemplate):
    grid: Grid
    width: int
    height: int

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        grid = []
        for line in (line.strip() for line in lines):
            grid.append(list(line))

        return cls(grid=grid, width=len(grid[0]), height=len(grid))

    @staticmethod
    def show(grid: Grid) -> None:
        for row in grid:
            print("".join(row))
        print()

    def step(self, grid: Grid) -> tuple[bool, Grid]:
        copy = deepcopy(grid)
        moved = False

        # > direction
        for row in range(self.height):
            for col in range(self.width):
                if grid[row][col] == ">":
                    new_col = (col + 1) % self.width
                    if grid[row][new_col] == ".":
                        copy[row][col] = "."
                        copy[row][new_col] = ">"
                        moved = True

        grid = copy

        copy = deepcopy(grid)

        # v direction
        for row in reversed(range(self.height)):
            for col in range(self.width):
                if grid[row][col] == "v":
                    new_row = (row + 1) % self.height
                    if grid[new_row][col] == ".":
                        copy[row][col] = "."
                        copy[new_row][col] = "v"
                        moved = True

        return moved, copy

    def task_one(self) -> int:
        moved, step = True, self.grid
        step_count = 0

        while moved:
            step_count += 1
            moved, step = self.step(step)

        return step_count

    def task_two(self) -> int:
        pass
