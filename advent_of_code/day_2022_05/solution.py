from typing import Iterable
from dataclasses import dataclass
from collections import deque
from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy


@dataclass
class Instruction:
    amount: int
    start: int
    end: int

    @classmethod
    def from_line(cls, line: str):
        words = line.strip().split(" ")
        # -1 to convert from starting index 1 to start index 0
        return cls(amount=int(words[1]), start=int(words[3]) - 1, end=int(words[5]) - 1)


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, stacks: list, instructions: list) -> None:
        self.stacks = stacks
        self.instructions = instructions

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        crate_size = 4  # "[A] " - brackets, symbol, whitespace
        stacks = []

        it = iter(lines)
        for line in it:
            if line == "\n":
                break

            if not stacks:
                for _ in range(len(line) // crate_size):
                    stacks.append(deque())

            for i in range(len(stacks)):
                if (
                    crate_symbol := line[i * crate_size + 1]
                ) != " " and not crate_symbol.isnumeric():
                    stacks[i].append(crate_symbol)

        instructions = [Instruction.from_line(line) for line in it]

        return cls(stacks, instructions)

    def task_one(self) -> int:
        stacks = deepcopy(self.stacks)
        for instruction in self.instructions:
            for _ in range(instruction.amount):
                stacks[instruction.end].appendleft(stacks[instruction.start].popleft())

        top_crates = (stack[0] for stack in stacks)
        print("".join(top_crates))

    def task_two(self) -> int:
        stacks = deepcopy(self.stacks)

        for instruction in self.instructions:
            new_stack = [stacks[instruction.start].popleft() for _ in range(instruction.amount)]
            for crate in reversed(new_stack):
                stacks[instruction.end].appendleft(crate)

        top_crates = (stack[0] for stack in stacks)
        print("".join(top_crates))
