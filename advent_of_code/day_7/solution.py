from typing import Iterable, Protocol
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from statistics import median
from functools import partial


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

    def fuel_consumption(self, function: FuelConsumption, target_position: int) -> int:
        return sum(
            function(position=position, target_position=target_position)
            for position in self.positions
        )

    def task_one(self) -> int:
        # we cannot move to float depth, either ceil or floor should give the same result
        _median = int(median(self.positions))

        return self.fuel_consumption(function=fuel_consumption_constant, target_position=_median)

    def task_two(self) -> int:
        """
        We're looking for a minimum of function in the shape of U. It may have multiple minima,
        but they should all be equal and "next to each other".
        """
        fuel_consumption = partial(self.fuel_consumption, function=fuel_consumption_linear)

        left_bound, right_bound = min(self.positions), max(self.positions)

        # Bisection method
        while True:
            half = left_bound + int((right_bound - left_bound) / 2)

            half_cost = fuel_consumption(target_position=half)
            look_left = fuel_consumption(target_position=half - 1)
            look_right = fuel_consumption(target_position=half + 1)

            if look_left >= half_cost <= look_right:
                # going either left or right doesn't improve our position, we have global min
                return half_cost

            elif look_left < half_cost:
                right_bound = half - 1

            elif look_right < half_cost:
                left_bound = half + 1
