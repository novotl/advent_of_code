from collections import Counter, defaultdict
from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    edges_from: dict[str, list[str]]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        edge_to = defaultdict(list)
        for line in lines:
            start, end = line.strip().split("-")
            edge_to[start].append(end)
            edge_to[end].append(start)

        return cls(edges_from=dict(edge_to))

    @staticmethod
    def is_big(cave: str) -> bool:
        """
        >>> Puzzle.is_big("DX")
        True

        >>> Puzzle.is_big("pj")
        False
        """
        return cave.isupper()

    def _recursion(
        self, current_cave: str, visited_caves: Counter, path: list, joker_used: bool
    ) -> int:
        if current_cave == "end":
            return 1

        # store current cave on the "stack"
        paths = 0
        visited_caves[current_cave] += 1
        path.append(current_cave)

        for next_cave in self.edges_from.get(current_cave, ()):
            next_big = self.is_big(next_cave)
            # we may go to the next cave if it's a big cave or a small one that was not yet visited
            if next_big or visited_caves[next_cave] < 1:
                paths += self._recursion(
                    current_cave=next_cave,
                    visited_caves=visited_caves,
                    path=path,
                    joker_used=joker_used,
                )
            # actually, we may visit one small cave twice (not the start though) by using a "joker"
            elif next_cave != "start" and not next_big and not joker_used:
                paths += self._recursion(
                    current_cave=next_cave, visited_caves=visited_caves, path=path, joker_used=True
                )

        # pop current cave from the "stack"
        visited_caves[current_cave] -= 1
        path.pop()

        return paths

    def task_one(self) -> int:
        return self._recursion(
            current_cave="start", visited_caves=Counter(), path=[], joker_used=True
        )

    def task_two(self) -> int:
        return self._recursion(
            current_cave="start", visited_caves=Counter(), path=[], joker_used=False
        )
