from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    numbers: list[int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls([int(line.strip()) for line in lines])

    def task_one(self) -> int:
        """
        Given a sequence of numbers `n_0, n_1, ..., n_m`, returns how many times `n_i > n_(i-1)`
        occurs.
        """
        numbers = iter(self.numbers)
        prev = next(numbers)
        increase = 0

        for number in numbers:
            if number > prev:
                increase += 1
            prev = number

        return increase

    def task_two(self) -> int:
        """
        Given a sequence of numbers `n_0, n_1, ..., n_m`, returns how many times
        `n_i + n_(i+1) + n_(i+2)   >   n_(i-1) + n_(i) + n_(i+1)`
        occurs.
        """
        _numbers = list(self.numbers)
        windows = zip(_numbers, _numbers[1:], _numbers[2:])

        prev = sum(next(windows))
        increase = 0

        for window in windows:
            window_sum = sum(window)
            if window_sum > prev:
                increase += 1
            prev = window_sum

        return increase
