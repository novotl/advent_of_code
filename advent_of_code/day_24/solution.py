from typing import Iterable
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
import operator as op

OPERATIONS = {"add": op.add, "div": op.floordiv, "mul": op.mul, "mod": op.mod, "eql": op.eq}


@dataclass
class Puzzle(PuzzleTemplate):
    instructions: tuple[str, str, str]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls(instructions=list(line.strip().split() for line in lines))

    def run_program(self, input_: list[int]) -> int:
        it = iter(input_)
        memory = {"w": 0, "x": 0, "y": 0, "z": 0}
        for instruction, *variables in self.instructions:

            try:
                if instruction == "inp":
                    memory[variables[0]] = next(it)
                else:
                    lhs, rhs = variables
                    lhs = memory[lhs]
                    rhs = memory[rhs] if rhs in memory else int(rhs)

                    memory[variables[0]] = int(OPERATIONS[instruction](lhs, rhs))
            except ZeroDivisionError:
                print("DIVISION BY ZERO")
                return 1
        return memory["z"]

        # rules:
        # w1 + 4 = w14
        # w2 - 2 = w13
        # w3 - 5 = w6
        # w4 - 1 = w5
        # w7 + 7 = w10
        # w8 + 3 = w9
        # w11 + 2 = w12

    def task_one(self) -> int:
        model_number = [
            5,  # w1
            9,  # w2
            9,  # w3
            9,  # w4
            8,  # w5
            4,  # w6
            2,  # w7
            6,  # w8
            9,  # w9
            9,  # w10
            7,  # w11
            9,  # w12
            7,  # w13
            9,  # w14
        ]
        print("".join(map(str, model_number)))
        return self.run_program(model_number)

    def task_two(self) -> int:
        model_number = [
            1,  # w1
            3,  # w2
            6,  # w3
            2,  # w4
            1,  # w5
            1,  # w6
            1,  # w7
            1,  # w8
            4,  # w9
            8,  # w10
            1,  # w11
            3,  # w12
            1,  # w13
            5,  # w14
        ]
        print("".join(map(str, model_number)))
        return self.run_program(model_number)
