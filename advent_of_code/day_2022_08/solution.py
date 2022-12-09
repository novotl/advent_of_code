from typing import Iterable
from dataclasses import dataclass
from collections import deque
from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy
from itertools import chain, product


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, forest: list[list[int]]) -> None:
        self.forest = forest
        self.rows = len(self.forest)
        self.cols = len(self.forest[0])

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        forest = [[int(tree) for tree in row.strip()] for row in lines]

        return cls(forest)

    def task_one(self) -> int:
        visible_coords = set()

        for row in range(self.rows):
            max_height = -1
            for col in range(self.cols):
                if (tree_height := self.forest[col][row]) > max_height:
                    max_height = tree_height
                    visible_coords.add((col, row))

        for row in range(self.rows):
            max_height = -1
            for col in range(self.cols - 1, -1, -1):
                if (tree_height := self.forest[col][row]) > max_height:
                    max_height = tree_height
                    visible_coords.add((col, row))

        for col in range(self.cols):
            max_height = -1
            for row in range(self.rows):
                if (tree_height := self.forest[col][row]) > max_height:
                    max_height = tree_height
                    visible_coords.add((col, row))

        for col in range(self.cols):
            max_height = -1
            for row in range(self.rows - 1, -1, -1):
                if (tree_height := self.forest[col][row]) > max_height:
                    max_height = tree_height
                    visible_coords.add((col, row))

        print(sorted(visible_coords))
        print(len(visible_coords))

    def tree_score(self, row: int, col: int) -> int:
        origin_height = self.forest[row][col]

        score = 1

        for d_row, d_col in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            cur_row, cur_col = row, col
            while True:
                cur_row += d_row
                cur_col += d_col
                cur_height = self.forest[cur_row][cur_col]
                if (
                    cur_height >= origin_height
                    or cur_row == 0
                    or cur_col == 0
                    or cur_row == self.rows - 1
                    or cur_col == self.cols - 1
                ):
                    dist = abs(cur_row - row) if d_row != 0 else abs(cur_col - col)
                    score = score * dist
                    break

        return score

    def task_two(self) -> int:
        max_score = 0

        for row in range(1, self.rows - 1):
            for col in range(1, self.cols - 1):
                max_score = max(max_score, self.tree_score(row, col))

        return max_score
