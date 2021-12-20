from typing import Iterable, Optional
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from collections import defaultdict
from pprint import pprint
from functools import reduce
from copy import deepcopy
from advent_of_code.utils import invert_dictionary

# 7 segment display mapping:
#
#    0:      1:      2:      3:      4:
#   aaaa    ....    aaaa    aaaa    ....
#  b    c  .    c  .    c  .    c  b    c
#  b    c  .    c  .    c  .    c  b    c
#   ....    ....    dddd    dddd    dddd
#  e    f  .    f  e    .  .    f  .    f
#  e    f  .    f  e    .  .    f  .    f
#   gggg    ....    gggg    gggg    ....
#
#    5:      6:      7:      8:      9:
#   aaaa    aaaa    aaaa    aaaa    aaaa
#  b    .  b    .  .    c  b    c  b    c
#  b    .  b    .  .    c  b    c  b    c
#   dddd    dddd    ....    dddd    dddd
#  .    f  e    f  .    f  e    f  .    f
#  .    f  e    f  .    f  e    f  .    f
#   gggg    gggg    ....    gggg    gggg
#
LIT_SEGMENTS = {
    0: {"a", "b", "c", "e", "f", "g"},
    1: {"c", "f"},
    2: {"a", "c", "d", "e", "g"},
    3: {"a", "c", "d", "f", "g"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "d", "f", "g"},
    6: {"a", "b", "d", "e", "f", "g"},
    7: {"a", "c", "f"},
    8: {"a", "b", "c", "d", "e", "f", "g"},
    9: {"a", "b", "c", "d", "f", "g"},
}


by_lengths = invert_dictionary(LIT_SEGMENTS, key=len)


def segments_to_digit(segments: str, mapping: dict[str, str]) -> Optional[int]:
    """
    Given segments and segment mapping returns corresponding digit or None if it doesn't map to
    a valid digit.

        >>> segments_to_digit('ab', {'a': 'c', 'b': 'f'})
        1

        >>> segments_to_digit('abcd', {'a': 'b', 'b': 'f', 'c': 'c', 'd': 'd'})
        4

        >>> segments_to_digit('ef', {'e': 'a', 'f': 'b'})
    """
    mapped_segments = set(mapping[segment] for segment in segments)

    for digit, lit_segments in LIT_SEGMENTS.items():
        if lit_segments == mapped_segments:
            return digit

    return None


@dataclass
class Entry:
    patterns: list[str]
    outputs: list[str]

    @classmethod
    def from_line(cls, line: str) -> "Entry":
        patterns, outputs = line.split(" | ")
        return cls(
            patterns=[pattern.strip() for pattern in patterns.split()],
            outputs=[output.strip() for output in outputs.split()],
        )

    @staticmethod
    def _assign(
        possible_mappings: dict[str, set[str]], segment: str, option: str
    ) -> Optional[dict[str, list[str]]]:
        """
        Assign a mapping and filter out all invalid options.


            >>> mappings = {
            ...     'a': {'a', 'b', 'c'},
            ...     'b': {'a', 'c'},
            ...     'c': {'d', 'b'}
            ... }

        Assigning mapping 'a -> b' rules out all other option for 'a' and also rules out 'b' as a valid
        option for 'c'.

            >>> Entry._assign(mappings, 'a', 'b') == {'a': {'b'}, 'b': {'a', 'c'}, 'c': {'d'}}
            True
        """

        next_mappings = deepcopy(possible_mappings)
        for segment_to_map, options in next_mappings.items():
            # deal with this special case after for loop
            if segment_to_map == segment:
                continue

            if option in options:
                options.remove(option)

            if not options:
                # some assumption is not valid, because we have no options left
                return None
        next_mappings[segment] = set(option)

        return next_mappings

    @staticmethod
    def _heuristics(segments: Iterable[str], possible_mappings: dict[str, set[str]]) -> list[str]:
        """
        Try segments with fewer options first to prune bad assumptions faster.

            >>> Entry._heuristics('abc', {'a': {'a'}, 'b': {'a', 'b'}, 'c': {'a', 'b', 'c'}})
            ['c', 'b', 'a']
        """

        # reverse because we use list.pop
        return list(
            sorted(segments, key=lambda segment: len(possible_mappings[segment]), reverse=True)
        )

    def recursion(
        self, segments: list[str], possible_mappings: dict[str, set[str]]
    ) -> Optional[dict[str, str]]:
        """
        Tries to guess a mapping and tests if it fits.

        Eventually tries all possible mappings.
        """
        if not segments:
            # we have some 1-1 mapping of segments, try if all patterns match to a number
            assert all(1 == len(value) for value in possible_mappings.values())
            final_mapping = {k: v.pop() for k, v in possible_mappings.items()}

            if all(
                segments_to_digit(pattern, final_mapping) is not None for pattern in self.patterns
            ):
                return final_mapping
            return None

        # this level of recursion picks one segment and tries to map it to all valid options
        segment = segments.pop()
        options = list(sorted(possible_mappings[segment]))

        for option in options:
            next_mappings = self._assign(possible_mappings, segment, option)
            if next_mappings is None:
                # some segment has no options left, we made a bad assumption -> backtrack
                continue

            solution = self.recursion(self._heuristics(segments, next_mappings), next_mappings)
            if solution:
                return solution

    def solve(self) -> int:
        # everything maps to everything
        possible_mappings = {char: set("abcdefg") for char in "abcdefg"}

        # initial pruning based on number of lit segments
        # if we have lit 'ab' it may only map to one digit = 1 which is 'cf'
        # so only valid options are `a -> {cf}` and `b -> {cf}`
        for pattern in self.patterns:
            matches = by_lengths[len(pattern)]
            all_valid_options = reduce(
                lambda a, b: a.union(b), (LIT_SEGMENTS[match] for match in matches), set()
            )

            for broken_segment in pattern:
                possible_mappings[broken_segment] = possible_mappings[broken_segment].intersection(
                    all_valid_options
                )

        mapping = self.recursion(
            self._heuristics(possible_mappings.keys(), possible_mappings), possible_mappings
        )

        assert mapping, "There is no valid assignment"

        return sum(
            segments_to_digit(segments, mapping) * 10 ** power
            for power, segments in enumerate(reversed(self.outputs))
        )


@dataclass
class Puzzle(PuzzleTemplate):
    entries: list[Entry]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(entries=[Entry.from_line(line) for line in lines])

    def task_one(self) -> int:
        total = 0
        for entry in self.entries:
            for digit in entry.outputs:
                lit_segments = len(digit)
                if len(by_lengths[lit_segments]) == 1:
                    total += 1

        return total

    def task_two(self) -> int:
        return sum(entry.solve() for entry in self.entries)
