from typing import Iterable
from dataclasses import dataclass
from enum import IntEnum
from collections import Counter

from advent_of_code.runner import PuzzleTemplate


class Commonality(IntEnum):
    MOST_COMMON = 0
    LEAST_COMMON = 1


def binary_str_to_decimal(chars: Iterable[str]) -> int:
    """
    Converts binary string to decimal number.

        >>> binary_str_to_decimal(['1', '0', '1'])
        5

        >>> binary_str_to_decimal('101010')
        42
    """

    return int("".join(chars), base=2)


def most_frequent(sequence: Iterable[str]) -> tuple[str, str]:
    """
    Returns most frequent and least frequent character.

        >>> most_frequent(['a', 'a', 'a', 'b', 'b', 'c'])
        ('a', 'c')

        >>> most_frequent(['a'])
        ('a', 'a')

        >>> most_frequent([])
        Traceback (most recent call last):
        ...
        ValueError: Sequence cannot be empty.

    On ties prefers higher as the most frequent and lower as the least frequent given natural
    ordering.

        >>> most_frequent(['a', 'b'])
        ('b', 'a')

    """
    counter = Counter(sequence)

    if not counter:
        raise ValueError("Sequence cannot be empty.")

    most_common_list = counter.most_common()

    most_common = most_common_list[0]
    least_common = most_common_list[-1]

    if most_common[1] == least_common[1]:
        return tuple(sorted((most_common[0], least_common[0]), reverse=True))

    return most_common[0], least_common[0]


def filter_until_one(lines: list[str], commonality: Commonality) -> str:
    _lines = list(lines)
    index = 0

    while len(_lines) != 1:
        match = most_frequent((line[index] for line in _lines))[commonality]
        _lines = [line for line in _lines if line[index] == match]
        index += 1

    return _lines[0]


@dataclass
class Puzzle(PuzzleTemplate):
    lines: list[int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(lines=[line.strip() for line in lines])

    def task_one(self) -> int:
        rotate = zip(*self.lines)
        most_frequent_raw, least_frequent_raw = zip(*(most_frequent(seq) for seq in rotate))

        return binary_str_to_decimal(most_frequent_raw) * binary_str_to_decimal(least_frequent_raw)

    def task_two(self) -> int:
        first = filter_until_one(self.lines, commonality=Commonality.MOST_COMMON)
        second = filter_until_one(self.lines, commonality=Commonality.LEAST_COMMON)

        return binary_str_to_decimal(first) * binary_str_to_decimal(second)
