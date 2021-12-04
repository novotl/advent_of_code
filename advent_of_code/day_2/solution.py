from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    instructions: list

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        raw_in = (line.strip().split() for line in lines)
        return cls(instructions=[(direction, int(unit)) for direction, unit in raw_in])

    def task_one(self) -> int:
        horizontal = 0
        depth = 0

        for direction, unit in self.instructions:
            if direction == "forward":
                horizontal += unit
            elif direction == "up":
                depth -= unit
            elif direction == "down":
                depth += unit
            else:
                raise Exception(f"Unknown direction {direction}")

        return horizontal * depth

    def task_two(self) -> int:
        horizontal = 0
        depth = 0
        aim = 0

        for direction, unit in self.instructions:
            if direction == "forward":
                horizontal += unit
                depth += aim * unit
            elif direction == "up":
                aim -= unit
            elif direction == "down":
                aim += unit
            else:
                raise Exception(f"Unknown direction {direction}")

        return horizontal * depth
