from itertools import product
from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate


@dataclass
class Puzzle(PuzzleTemplate):
    positions: tuple[int, int]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        it = iter(lines)

        *_, a = next(it).strip().split(" ")
        *_, b = next(it).strip().split(" ")

        return cls(positions=(int(a), int(b)))

    @staticmethod
    def deterministic_dice(max_num: int) -> Iterable[int]:
        """
        >>> dice = Puzzle.deterministic_dice(3)
        >>> [next(dice) for _ in range(5)]
        [1, 2, 3, 1, 2]
        """
        while True:
            for i in range(max_num):
                yield i + 1

    def task_one(self) -> int:
        a_pos, b_pos = self.positions
        a_score, b_score = 0, 0
        dice = self.deterministic_dice(100)
        rolls = 0

        for turn in range(10_000_000):
            a_pos = ((a_pos + sum(next(dice) for _ in range(3)) - 1) % 10) + 1
            a_score += a_pos
            rolls += 3

            if a_score >= 1000:
                break

            b_pos = ((b_pos + sum(next(dice) for _ in range(3)) - 1) % 10) + 1
            b_score += b_pos
            rolls += 3

            if b_score >= 1000:
                break

        return min(a_score, b_score) * rolls

    def task_two(self) -> int:
        # (a_pos, b_pos, a_score, b_score) -> (a_wins, b_wins)
        dp: dict[tuple[int, int, int, int], tuple[int, int]] = dict()

        for a_score in reversed(range(0, 21)):
            for b_score in reversed(range(0, 21)):
                for a_pos in range(1, 11):
                    for b_pos in range(1, 11):

                        a_wins, b_wins = 0, 0
                        # TODO: optimize, 1+2+3 == 1+3+2 == 2+3+1 == ...
                        for a_roll in product(range(1, 4), repeat=3):
                            new_a_pos = ((a_pos + sum(a_roll) - 1) % 10) + 1
                            new_a_score = a_score + new_a_pos

                            if new_a_score >= 21:
                                a_wins += 1
                                continue

                            for b_roll in product(range(1, 4), repeat=3):
                                new_b_pos = ((b_pos + sum(b_roll) - 1) % 10) + 1
                                new_b_score = b_score + new_b_pos

                                if new_b_score >= 21:
                                    b_wins += 1
                                    continue

                                a, b = dp[(new_a_pos, new_b_pos, new_a_score, new_b_score)]
                                a_wins += a
                                b_wins += b

                        dp[(a_pos, b_pos, a_score, b_score)] = (a_wins, b_wins)

        a_pos, b_pos = self.positions
        return max(dp[(a_pos, b_pos, 0, 0)])
