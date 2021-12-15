from typing import Iterable, NamedTuple
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from operator import attrgetter


class Dot(NamedTuple):
    x: int  # left to right
    y: int  # top to bottom

    @classmethod
    def from_line(cls, line: str) -> "Dot":
        x, y = map(int, line.split(","))
        return cls(x=x, y=y)


@dataclass
class Fold:
    axis: str
    value: str

    @classmethod
    def from_line(cls, line: str) -> "Fold":
        """
        >>> Fold.from_line("fold along y=7")
        Fold(axis='y', value=7)

        >>> Fold.from_line("fold along x=554")
        Fold(axis='x', value=554)
        """
        assert line.startswith("fold along ")
        axis, value = line[11:].split("=")

        return cls(axis=axis, value=int(value))


@dataclass
class Puzzle(PuzzleTemplate):
    dots: set[Dot]
    folds: list[Fold]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        dots = set()
        it = iter(lines)
        while (line := next(it).strip()) and line:
            dots.add(Dot.from_line(line))

        folds = [Fold.from_line(line.strip()) for line in it]

        return cls(dots=dots, folds=folds)

    @staticmethod
    def fold(dots: set[Dot], fold: Fold) -> set[Dot]:
        # set get's rid of any duplicate dots (that overlap after a fold)
        new_dots = set()

        for dot in dots:
            new_dot = dot

            if fold.axis == "y" and dot.y > fold.value:
                new_y = fold.value - (dot.y - fold.value)
                new_dot = dot._replace(y=new_y)

            elif fold.axis == "x" and dot.x > fold.value:
                new_x = fold.value - (dot.x - fold.value)
                new_dot = dot._replace(x=new_x)

            new_dots.add(new_dot)

        return new_dots

    @staticmethod
    def show(dots: list[Dot]) -> str:
        width = max(dots, key=lambda dot: dot.x).x + 1
        height = max(dots, key=lambda dot: dot.y).y + 1

        lines = []

        for row in range(height):
            line = ["."] * width
            for col in range(width):
                if Dot(col, row) in dots:
                    line[col] = "#"
            lines.append("".join(line))

        return "\n".join(lines)

    def task_one(self) -> int:
        dots = self.fold(self.dots, self.folds[0])
        return len(dots)

    def task_two(self) -> str:
        dots = self.dots
        for fold in self.folds:
            dots = self.fold(dots, fold)

        return self.show(dots)
