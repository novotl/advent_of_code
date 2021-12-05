from collections import Counter
from typing import Iterable, NamedTuple
from dataclasses import dataclass, field

from advent_of_code.runner import PuzzleTemplate


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def from_str(cls, string: str) -> "Point":
        return cls(*(int(num) for num in string.split(",")))

    def __add__(self, other: "Point") -> "Point":
        """
        >>> Point(-4, 8) + Point(4, -8)
        Point(0, 0)
        """
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        """
        >>> Point(4, 8) - Point(4, 8)
        Point(0, 0)
        """
        return self.__class__(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def to_unit(self) -> "Point":
        """
        Converts Point to unit vector.

        >>> Point(-4, 8).to_unit()
        Point(-1, 1)

        """
        nx = self.x / abs(self.x) if self.x else 0
        ny = self.y / abs(self.y) if self.y else 0
        return self.__class__(int(nx), int(ny))


@dataclass
class Segment:
    start: Point
    end: Point

    @classmethod
    def from_str(cls, string: str) -> "Segment":
        start, end = (Point.from_str(point) for point in string.split("->"))
        return cls(start=start, end=end)

    @property
    def direction(self) -> Point:
        """
        >>> Segment.from_str("0,9 -> 5,9").direction
        Point(1, 0)
        >>> Segment.from_str("8,0 -> 0,8").direction
        Point(-1, 1)
        """
        return (self.end - self.start).to_unit()

    def is_diagonal(self) -> bool:
        """
        Returns whether the segment is horizontal or vertical.

            >>> Segment.from_str("0,9 -> 5,9").is_diagonal()
            False

            >>> Segment.from_str("8,0 -> 0,8").is_diagonal()
            True
        """
        x, y = self.direction
        return x != 0 and y != 0

    def segment_points(self) -> Iterable[Point]:
        """
        Returns all integer points this segment crosses.

            >>> list(Segment.from_str("0,9 -> 5,9").segment_points())
            [Point(0, 9), Point(1, 9), Point(2, 9), Point(3, 9), Point(4, 9), Point(5, 9)]

            >>> list(Segment.from_str("6,4 -> 2,0").segment_points())
            [Point(6, 4), Point(5, 3), Point(4, 2), Point(3, 1), Point(2, 0)]
        """
        direction = self.direction
        current = self.start
        yield current

        while current != self.end:
            current = current + direction
            yield current


@dataclass
class Puzzle(PuzzleTemplate):
    segments: list[tuple[Point, Point]]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(segments=[Segment.from_str(line) for line in lines])

    def task_one(self) -> int:
        counter = Counter()
        for segment in self.segments:
            if not segment.is_diagonal():
                counter.update(segment.segment_points())

        return sum(1 for v in counter.values() if v > 1)

    def task_two(self) -> int:
        counter = Counter()
        for segment in self.segments:
            counter.update(segment.segment_points())

        return sum(1 for v in counter.values() if v > 1)
