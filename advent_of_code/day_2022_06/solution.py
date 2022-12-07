from typing import Iterable
from dataclasses import dataclass
from collections import deque
from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, line: str) -> None:
        self.line = line

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(next(iter(lines)))

    def task_one(self, size: int = 4) -> int:
        return next(
            i for i in range(size, len(self.line)) if len(set(self.line[i - size : i])) == size
        )

    def task_two(self) -> int:
        return self.task_one(size=14)
