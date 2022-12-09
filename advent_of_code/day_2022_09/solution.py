from typing import Iterable
from dataclasses import dataclass
from collections import deque
from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy
from itertools import chain, product


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def touches(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1


DIRECTIONS = {
    "R": Vector(0, 1),
    "L": Vector(0, -1),
    "U": Vector(1, 0),
    "D": Vector(-1, 0),
}

ZERO = Vector(0, 0)


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, instructions: list[tuple[str, int]]) -> None:
        self.instructions = instructions

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        lines = (line.strip().split() for line in lines)
        instructions = [(direction, int(distance)) for direction, distance in lines]

        return cls(instructions)

    @staticmethod
    def move(head: Vector, tail: Vector) -> Vector:
        if head.touches(tail):
            return tail

        tail_direction = ZERO

        if head.y > tail.y:
            tail_direction += DIRECTIONS["R"]
        elif head.y < tail.y:
            tail_direction += DIRECTIONS["L"]

        if head.x > tail.x:
            tail_direction += DIRECTIONS["U"]
        elif head.x < tail.x:
            tail_direction += DIRECTIONS["D"]

        return tail + tail_direction

    def task_one(self) -> int:
        visited = set()

        # x - up (positive); down (negative)
        # y - left (negative); right (positive)
        head = ZERO
        tail = ZERO

        for direction, steps in self.instructions:
            for _ in range(steps):

                head += DIRECTIONS[direction]
                tail = self.move(head, tail)
                visited.add(tail)

        return len(visited)

    def task_two(self) -> int:
        visited = set()

        # x - up (positive); down (negative)
        # y - left (negative); right (positive)
        knots = [ZERO for _ in range(10)]

        for direction, steps in self.instructions:
            for _ in range(steps):
                knots[0] += DIRECTIONS[direction]

                for i in range(1, len(knots)):
                    knots[i] = self.move(knots[i - 1], knots[i])

                visited.add(knots[-1])

        return len(visited)
