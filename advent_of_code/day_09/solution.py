from typing import Iterable, NamedTuple
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from itertools import chain
from functools import reduce
import operator


class Point(NamedTuple):
    row: int
    col: int


@dataclass
class Puzzle(PuzzleTemplate):
    map: list[list[int]]
    num_columns: int
    num_rows: int

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        map_ = [[int(height) for height in line.strip()] for line in lines]

        return cls(map=map_, num_rows=len(map_), num_columns=len(map_[0]))

    def is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self.num_rows and 0 <= col < self.num_columns

    def all_neighbors(self, row: int, col: int) -> Iterable[Point]:
        for d_row, d_col in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            new_row, new_col = row + d_row, col + d_col
            if self.is_valid(row=new_row, col=new_col):
                yield Point(new_row, new_col)

    def all_neighbors_higher(self, row: int, col: int) -> bool:
        height = self.map[row][col]
        for n_row, n_col in self.all_neighbors(row, col):
            if self.map[n_row][n_col] <= height:
                return False

        return True

    def mark_points(self, points: Iterable[Point]):
        points_ = set(points)

        print()
        for row in range(self.num_rows):
            print(
                "".join(
                    str(self.map[row][col]) if Point(row, col) in points_ else "."
                    for col in range(self.num_columns)
                )
            )
        print()

    def low_points(self) -> Iterable[Point]:
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                if self.all_neighbors_higher(row, col):
                    yield Point(row=row, col=col)

    def find_basin(self, row: int, col: int) -> Iterable[Point]:
        open_list = {Point(row, col)}
        closed_list = set()

        while open_list:
            point = open_list.pop()
            closed_list.add(point)
            yield point

            height = self.map[point.row][point.col]
            for neighbor in self.all_neighbors(point.row, point.col):
                if (
                    neighbor not in open_list
                    and neighbor not in closed_list
                    and height < self.map[neighbor.row][neighbor.col] < 9
                ):
                    open_list.add(neighbor)

    def task_one(self) -> int:
        low_points = list(self.low_points())
        self.mark_points(low_points)
        return sum(self.map[row][col] + 1 for row, col in low_points)

    def task_two(self) -> int:
        low_points = list(self.low_points())
        basins = [list(self.find_basin(row, col)) for row, col in low_points]

        self.mark_points(chain(*basins))

        sizes = sorted([len(basin) for basin in basins])

        return reduce(operator.mul, sizes[-3:])
