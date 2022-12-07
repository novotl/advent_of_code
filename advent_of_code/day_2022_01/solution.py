from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, lines) -> None:
        self.lines = [line.strip() for line in lines]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(lines)

    def task_one(self) -> int:
        max_group = 0
        running_count = 0
        for line in self.lines:
            if not line:
                max_group = max(max_group, running_count)
                running_count = 0
            else:
                print(line)
                running_count += int(line)

        max_group = max(max_group, running_count)

        return max_group

    def task_two(self) -> int:
        groups = []

        running_count = 0
        for line in self.lines:
            if not line:
                groups.append(running_count)
                running_count = 0
            else:
                print(line)
                running_count += int(line)

        groups.append(running_count)

        groups.sort()
        print(groups)
        return sum(groups[-3:])
