from typing import Iterable
from dataclasses import dataclass
from itertools import chain
from advent_of_code.runner import PuzzleTemplate
from statistics import median

CORRUPTED_SCORE_BOARD = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_SCORE_BOARD = {")": 1, "]": 2, "}": 3, ">": 4}

OPENING = ["(", "[", "{", "<"]
CLOSING = [")", "]", "}", ">"]
PAIRS = {a: b for a, b in chain(zip(OPENING, CLOSING), zip(CLOSING, OPENING))}


@dataclass
class CheckerOutput:
    syntax_error: int = 0
    missing_chars: str = ""


@dataclass
class Puzzle(PuzzleTemplate):
    lines: list[str]

    @staticmethod
    def check_line(line: str) -> CheckerOutput:
        """
        >>> Puzzle.check_line('{([(<{}[<>[]}>{[]{[(<()>').syntax_error
        Expected ], but found } instead.
        1197

        >>> Puzzle.check_line('[{[{({}]{}}([{[{{{}}([]').syntax_error
        Expected ), but found ] instead.
        57
        """
        stack = list()
        for char in line:
            if char in OPENING:
                stack.append(char)
            elif char in CLOSING:
                opening = stack.pop()
                if PAIRS[opening] != char:
                    print(f"Expected {PAIRS[opening]}, but found {char} instead.")
                    return CheckerOutput(syntax_error=CORRUPTED_SCORE_BOARD[char])
            else:
                raise ValueError(f"Invalid input {char}")

        # if stack is empty - every bracket was properly closed, otherwise add closing brackets
        # to all that are still left in the stack.
        missing_chars = "".join(PAIRS[char] for char in reversed(stack))
        return CheckerOutput(missing_chars=missing_chars)

    @staticmethod
    def autocomplete_score(missing_characters: str) -> int:
        """
        >>> Puzzle.autocomplete_score('')
        0
        >>> Puzzle.autocomplete_score('}}]])})]')
        288957
        >>> Puzzle.autocomplete_score('])}>')
        294
        >>> Puzzle.autocomplete_score(']]}}]}]}>')
        995444
        >>> Puzzle.autocomplete_score(')}>]})')
        5566
        >>> Puzzle.autocomplete_score('}}>}>))))')
        1480781
        """
        score = 0
        for char in missing_characters:
            score *= 5
            score += AUTOCOMPLETE_SCORE_BOARD[char]

        return score

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(lines=[line.strip() for line in lines])

    def task_one(self) -> int:
        return sum(self.check_line(line).syntax_error for line in self.lines)

    def task_two(self) -> int:
        checker_output = (self.check_line(line) for line in self.lines)
        return median(
            self.autocomplete_score(output.missing_chars)
            for output in checker_output
            if output.missing_chars  # ignore syntax errors, they would mess up median
        )
