import itertools
from typing import Iterable, NamedTuple
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from itertools import product


class Point(NamedTuple):
    r: int
    c: int

    def __repr__(self) -> str:
        return f"({self.r}, {self.c})"


@dataclass
class Puzzle(PuzzleTemplate):
    string: list[bool]
    lit: set[Point]
    right_bottom: Point

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        it = iter(lines)

        string = list(True if char == "#" else False for char in next(it).strip())
        assert string[0] is not string[-1]
        next(it)  # skip blank line

        lit = set()
        row = 0
        for line in (line.strip() for line in it):
            col = 0
            for char in line:
                if char == "#":  # store only lit squares
                    lit.add(Point(row, col))
                col += 1
            row += 1

        return cls(string=string, lit=lit, right_bottom=Point(row - 1, col - 1))

    def iter(
        self, lit: set[Point], left_top: Point, right_bottom: Point, polarity: bool
    ) -> dict[Point, str]:
        new_lit = set()
        new_left_top = Point(left_top.r - 1, left_top.c - 1)
        new_right_bottom = Point(right_bottom.r + 1, right_bottom.c + 1)

        new_polarity = not polarity if self.string[0] else polarity

        for row in range(new_left_top.r, new_right_bottom.r + 1):
            for col in range(new_left_top.c, new_right_bottom.c + 1):
                binary = "".join(
                    str(int(polarity))
                    if Point(row + dr, col + dc) in lit
                    else str(int(not polarity))
                    for dr in [-1, 0, 1]
                    for dc in [-1, 0, 1]
                )
                index = int(binary, base=2)
                # print(f"{Point(row, col)}: {binary} -> {index}")
                new_value = self.string[index]
                if new_value == new_polarity:
                    new_lit.add(Point(row, col))

        return (new_lit, new_left_top, new_right_bottom, new_polarity)

    @staticmethod
    def show(lit: set[Point], left_top: Point, right_bottom: Point) -> None:
        for row in range(left_top.r, right_bottom.r + 1):
            line = "".join(
                "#" if Point(row, col) in lit else "."
                for col in range(left_top.c, right_bottom.c + 1)
            )
            print(line)

    def task_one(self, iterations: int = 2) -> int:
        left_top = Point(0, 0)
        right_bottom = self.right_bottom
        lit = self.lit
        polarity = True

        for _ in range(iterations):
            lit, left_top, right_bottom, polarity = self.iter(lit, left_top, right_bottom, polarity)

        self.show(lit, left_top, right_bottom)
        return len(lit)

    def task_two(self) -> int:
        return self.task_one(iterations=50)
