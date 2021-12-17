from typing import Iterable
from copy import deepcopy
from advent_of_code.runner import PuzzleTemplate
from dataclasses import dataclass, field


@dataclass
class Board:
    # board juts for visualization purpose
    board: list[list[int]] = field(default_factory=lambda: [[None] * 5 for _ in range(5)])
    # number can appear on a board at most once
    # maps number to indices on the board
    index: dict[int, tuple[int, int]] = field(default_factory=dict)

    # set of all number that wasn't marked
    unmarked_numbers: set[int] = field(default_factory=set)
    # number of remaining unmarked number in each row / col
    remaining_cols: dict[int, int] = field(default_factory=dict)
    remaining_rows: dict[int, int] = field(default_factory=dict)
    won: bool = False

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Board":
        """
        Note: this functions get's an iterator, so make sure to take only what is required!
        """
        board = cls()

        next(lines)  # skip the first empty line
        for row, cols in enumerate(lines):
            for col, number_raw in enumerate(cols.split()):
                number = int(number_raw)
                board.board[row][col] = number
                board.index[number] = (row, col)
                board.unmarked_numbers.add(number)

            if row == 4:
                break

        for i in range(5):
            board.remaining_cols[i] = 5
            board.remaining_rows[i] = 5

        return board

    def call_number(self, number: int) -> bool:
        if not self.won and number in self.index:
            row, col = self.index[number]
            self.board[row][col] = "x"
            self.unmarked_numbers.remove(number)
            self.remaining_cols[col] -= 1
            self.remaining_rows[row] -= 1

            won = self.remaining_cols[col] == 0 or self.remaining_rows[row] == 0
            if won:
                # bingo!
                self.won = True
            return won

        return False

    def score(self, called_number: int) -> int:
        """
        The score of the winning board can now be calculated. Start by finding the sum of all
        unmarked numbers on that board. Then, multiply that sum by the number that was just called
        when the board won.
        """
        return sum(self.unmarked_numbers) * called_number

    def __str__(self) -> str:
        return "\n".join(" ".join(str(char).rjust(2) for char in row) for row in self.board)


class Puzzle(PuzzleTemplate):
    _input: list[int]
    _boards: list[Board]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        puzzle = cls()

        it = iter(lines)
        puzzle._input = [int(number) for number in next(it).split(",")]
        puzzle._boards = []

        while it:
            try:
                puzzle._boards.append(Board.from_lines(it))
            except StopIteration:
                break

        return puzzle

    def task_one(self) -> int:
        """
        Return score of the board that has the first Bingo!
        """
        boards = deepcopy(self._boards)
        for number in self._input:
            for board_num, board in enumerate(boards):
                if board.call_number(number):
                    print(f"Bingo! on board {board_num} \n")
                    print(f"{board}\n")
                    return board.score(number)

    def task_two(self) -> int:
        """
        Return score of the board that has the last Bingo!
        """
        boards = deepcopy(self._boards)
        boards_remaining = len(boards)

        for number in self._input:
            for board_num, board in enumerate(boards):
                if board.call_number(number):
                    boards_remaining -= 1

                    if boards_remaining == 0:
                        print(f"Bingo! on last board {board_num} \n")
                        print(f"{board}\n")
                        return board.score(number)
