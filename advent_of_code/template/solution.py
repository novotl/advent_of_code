from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls()

    def task_one(self) -> int:
        pass

    def task_two(self) -> int:
        pass
