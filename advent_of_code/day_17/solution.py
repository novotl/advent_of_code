from typing import Iterable, Optional
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate

from math import ceil, sqrt


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        """
        >>> a, b = Point(1, 2), Point(3, 4)
        >>> a + b
        Point(x=4, y=6)
        """
        return self.__class__(self.x + other.x, self.y + other.y)


@dataclass
class Area:
    top_left: Point
    bottom_right: Point

    def is_inside(self, point: Point) -> bool:
        """
        >>> area = Area(top_left=Point(20, -5), bottom_right=Point(30, -10))

        >>> area.is_inside(Point(20, -5))
        True
        >>> area.is_inside(Point(30, -5))
        True
        >>> area.is_inside(Point(20, -10))
        True
        >>> area.is_inside(Point(30, -10))
        True
        >>> area.is_inside(Point(25, -8))
        True
        >>> area.is_inside(Point(31, -11))
        False
        """
        return (
            self.top_left.x <= point.x <= self.bottom_right.x
            and self.bottom_right.y <= point.y <= self.top_left.y
        )

    def is_under(self, point: Point) -> bool:
        """
        >>> area = Area(top_left=Point(20, -5), bottom_right=Point(30, -10))

        >>> area.is_under(Point(0, 100))
        False
        >>> area.is_under(Point(0, -11))
        True
        """
        return point.y < self.bottom_right.y

    def is_right(self, point: Point) -> bool:
        """
        >>> area = Area(top_left=Point(20, -5), bottom_right=Point(30, -10))

        >>> area.is_right(Point(0, 100))
        False
        >>> area.is_right(Point(31, -11))
        True
        """
        return point.x > self.bottom_right.x


def helper(s: str) -> tuple[int, int]:
    """
    >>> helper("x=20..30")
    (20, 30)
    >>> helper("y=-10..-5")
    (-10, -5)
    """
    a, b = map(int, s[2:].split(".."))
    return a, b


@dataclass
class Puzzle(PuzzleTemplate):
    target: Area

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":

        line = next(iter(lines)).strip().removeprefix("target area: ")
        x_raw, y_raw = line.split(", ")
        x_min, x_max = helper(x_raw)
        y_min, y_max = helper(y_raw)

        return cls(target=Area(top_left=Point(x_min, y_max), bottom_right=Point(x_max, y_min)))

    def simulate_shot(self, velocity: Point) -> Optional[int]:
        position = Point(0, 0)
        max_y = 0

        while True:
            position = position + velocity
            max_y = max(max_y, position.y)

            if self.target.is_inside(position):
                return max_y

            if self.target.is_under(position) or self.target.is_right(position):
                break

            # print(position)
            # assume we're always shooting to the right!
            velocity = Point(x=max(0, velocity.x - 1), y=velocity.y - 1)

        return None

    def task_one(self) -> int:
        return max(
            filter(
                lambda x: x is not None,
                (
                    self.simulate_shot(Point(x, y))
                    for x in range(0, self.target.bottom_right.x + 1)
                    for y in range(0, -self.target.bottom_right.y)
                ),
            )
        )

    def task_two(self) -> int:
        # x is decreasing by 1, e.g.: 5, 4, 3, 2, 1, 0, 0, 0, 0, ... and we need to reach at least
        # `target.top_left.x`. Sum of arithmetic sequence is S_n = n*(a_1 + a_n)/2, so for our
        # initial x velocity, we reach at most: (x * (x+1)) / 2
        # solve for x we get minimum required bound
        # min_x = (-1 + sqrt(1 + c * target.min_x))/2
        min_x = ceil((-1 + sqrt(1 + 2 * self.target.top_left.x)) / 2)

        # we would overshoot in the first step
        max_x = self.target.bottom_right.x

        # the y goes like this: 3, 2, 1, 0, -1, -2, -3
        # so when it passes y=0 it has velocity = -y_initial
        # and if it's lower than target.min_y we would undershoot it
        max_y = -self.target.bottom_right.y

        # we would undershoot in the first step
        min_y = self.target.bottom_right.y

        initial = [
            (x, y)
            for x in range(min_x, max_x + 1)
            for y in range(min_y, max_y)
            if self.simulate_shot(Point(x, y)) is not None
        ]

        return len(initial)
