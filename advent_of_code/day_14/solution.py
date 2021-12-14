from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
from collections import Counter


@dataclass
class Puzzle(PuzzleTemplate):
    ends: tuple[str, str]
    template: Counter[str]
    rules: dict[str, str]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        it = iter(lines)

        template_raw = next(it).strip()
        template = Counter(map("".join, zip(template_raw, template_raw[1:])))
        ends = template_raw[0], template_raw[-1]

        next(it)  # skip blank line

        pairs = (line.strip().split(" -> ") for line in it)
        rules = {from_: to for from_, to in pairs}

        return cls(ends=ends, template=template, rules=rules)

    def apply_rule(self, elements: str) -> str:
        """
        >>> puzzle = Puzzle.from_lines(["ABA", "", "AB -> C"])
        >>> puzzle.apply_rule("AB")
        ('AC', 'CB')
        """

        new_element = self.rules[elements]
        return f"{elements[0]}{new_element}", f"{new_element}{elements[-1]}"

    def task_one(self, steps: int = 10) -> int:
        template = self.template

        for _ in range(steps):
            new_template = Counter()
            for element_pair, count in template.items():
                for new_pairs in self.apply_rule(element_pair):
                    new_template[new_pairs] += count
            template = new_template

        letter_counts = Counter()
        for element_pair, count in template.items():
            letter_counts[element_pair[0]] += count
            letter_counts[element_pair[1]] += count

        # we count every element twice (as first in the pair and as the second)
        # need to do the same for the very first and very last which are counted only once
        for end in self.ends:
            letter_counts[end] += 1

        occurrences = letter_counts.most_common()
        return (occurrences[0][1] - occurrences[-1][1]) // 2

    def task_two(self) -> int:
        return self.task_one(steps=40)
