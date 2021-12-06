from collections import Counter
from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    groups: Counter[int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        line = next(iter(lines))
        return cls(Counter(int(timer) for timer in line.split(",")))

    def task_one(self, days=80) -> int:
        groups = self.groups

        for _ in range(days):
            new_groups = Counter()
            for timer, count in groups.items():
                if timer == 0:
                    # reset counter of this group of lanternfist
                    new_groups[6] += count
                    # spawn a newborn group
                    new_groups[8] += count
                else:
                    new_groups[timer - 1] += count
            groups = new_groups

        return sum(size for size in groups.values())

    def task_two(self) -> int:
        return self.task_one(days=256)
