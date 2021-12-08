from typing import Iterable, Optional
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from collections import defaultdict
from pprint import pprint
from functools import reduce
from copy import deepcopy

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


by_lengths = defaultdict(list)
for digit, segment in LIT_SEGMENTS.items():
    by_lengths[len(segment)].append(digit)


# TODO: the set has always only one element
def mappings_to_digit(segments, mapping: dict[str, set[str]]):
    mapped_segments = set(next(iter(mapping[segment])) for segment in segments)

    for k, v in LIT_SEGMENTS.items():
        if v == mapped_segments:
            return k

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
    def assign(possible_mappings, option, segment) -> Optional[dict[str, list[str]]]:
        next_mappings = deepcopy(possible_mappings)
        for k, v in next_mappings.items():
            if k == segment:
                continue

            if option in v:
                v.remove(option)
            if not v:
                # some assumption is not valid, because we have no options left
                print("constraint violated")
                return None
        next_mappings[segment] = set(option)

        return next_mappings

    def recursion(self, segments: list[str], possible_mappings: dict[str, str]):
        if not segments:
            # we have all mappings, need to check if all patterns are valid e.g. display a number
            pprint(possible_mappings)

            for pattern in self.patterns:
                digit = mappings_to_digit(pattern, possible_mappings)
                if digit is None:
                    print("constraint violated")
                    return
            print("Found solution!")
            return possible_mappings

        segment = segments.pop()

        options = list(sorted(possible_mappings[segment]))
        # pick one option
        for option in options:
            print(f"Assume {segment} = {option} | options={options})")
            next_mappings = self.assign(possible_mappings, option, segment)
            if next_mappings is None:
                continue
            print("Candidate:")
            pprint(next_mappings)

            solution = self.recursion(list(segments), next_mappings)
            if solution:
                return solution

    def solve(self) -> int:
        # broken segment -> original segment
        possible_mappings = {char: set("abcdefg") for char in "abcdefg"}

        # initial pruning
        for pattern in self.patterns:
            matches = by_lengths[len(pattern)]
            all_valid_options = reduce(
                lambda a, b: a.union(b), (LIT_SEGMENTS[match] for match in matches), set()
            )

            for broken_segment in pattern:
                possible_mappings[broken_segment] = possible_mappings[broken_segment].intersection(
                    all_valid_options
                )

        print("After initial pruning:")
        pprint(possible_mappings)

        # TODO: heuristics, iterate segments with lower number of options first
        mapping = self.recursion(
            list(sorted(possible_mappings.keys(), reverse=True)), possible_mappings
        )

        # 💩
        a = mappings_to_digit(self.outputs[0], mapping)
        b = mappings_to_digit(self.outputs[1], mapping)
        c = mappings_to_digit(self.outputs[2], mapping)
        d = mappings_to_digit(self.outputs[3], mapping)
        x = a * 1000 + b * 100 + c * 10 + d
        return x


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
