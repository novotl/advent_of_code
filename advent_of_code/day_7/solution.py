from typing import Iterable, Protocol
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


def sum_arithmetic_sequence(a_n: int) -> int:
    """
    Returns 1 + 2 + ... + a_n.

        >>> sum_arithmetic_sequence(4)
        10

        >>> sum_arithmetic_sequence(5)
        15
    """
    return int((a_n * (a_n + 1)) / 2)


class FuelConsumption(Protocol):
    def __call__(self, position: int, target_position: int) -> int:
        pass


def fuel_consumption_constant(position: int, target_position: int) -> int:
    """
    >>> fuel_consumption_constant(16, 2)
    14

    >>> fuel_consumption_constant(2, 2)
    0

    >>> fuel_consumption_constant(2, 14)
    12
    """
    return abs(position - target_position)


def fuel_consumption_linear(position: int, target_position: int) -> int:
    """
    >>> fuel_consumption_linear(16, 5)
    66

    >>> fuel_consumption_linear(2, 2)
    0

    >>> fuel_consumption_linear(14, 5)
    45
    """
    return sum_arithmetic_sequence(abs(position - target_position))


@dataclass
class Puzzle(PuzzleTemplate):
    positions: list[int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        line = next(iter(lines))
        return cls([int(num) for num in line.split(",")])

    def task_one(self, consumption_function: FuelConsumption = fuel_consumption_constant) -> int:
        _min, _max = min(self.positions), max(self.positions)
        return min(
            sum(
                consumption_function(position=position, target_position=depth)
                for position in self.positions
            )
            for depth in range(_min, _max + 1)
        )

    def task_two(self) -> int:
        return self.task_one(consumption_function=fuel_consumption_linear)
