from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt, truediv
from typing import Iterable
from PIL import Image
import numpy as np
from tqdm import tqdm
from heapq import heappush, heappop


COMBO = {
    0: lambda a, b, c: 0,
    1: lambda a, b, c: 1,
    2: lambda a, b, c: 2,
    3: lambda a, b, c: 3,
    4: lambda a, b, c: a,
    5: lambda a, b, c: b,
    6: lambda a, b, c: c,
}

OPCODE = {0: lambda operand, a, b, c: a / (COMBO[operand] ** 2)}


def solve(a: int, b: int, c: int, program: list[int]) -> list[int]:
    output = []

    instruction_pointer = 0
    while True:
        try:
            opcode = program[instruction_pointer]
            operand = program[instruction_pointer + 1]
        except IndexError:
            break

        if opcode == 0:
            a = a // (2 ** COMBO[operand](a, b, c))
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = COMBO[operand](a, b, c) % 8
        elif opcode == 3:
            if a == 0:
                instruction_pointer += 2
                continue
            else:
                instruction_pointer = operand
                continue
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            output.append(COMBO[operand](a, b, c) % 8)
            l = len(output)
            if output[l - 1] != program[l - 1]:
                return output
        elif opcode == 6:
            b = a // (2 ** COMBO[operand](a, b, c))
        elif opcode == 7:
            c = a // (2 ** COMBO[operand](a, b, c))

        instruction_pointer += 2

    return output


def main():
    lines = iter(stdin.read().strip().splitlines())

    a = int(next(lines).split(":")[-1])
    b = int(next(lines).split(":")[-1])
    c = int(next(lines).split(":")[-1])
    next(lines)
    [*program] = map(int, next(lines).split(":")[-1].split(","))

    # part_a = solve(a, b, c, program)
    # print(",".join(map(str, part_a)))


    # 247839002892474
    
    common = {i: 8 ** len(program) - 1 for i in range(len(program))}

    for start_number in tqdm(range(10_000_000)):
        init = start_number * 8**10 + 0o0356514272

        output = solve(a=init, b=0, c=0, program=program)

        if output == program:
            print(init)
            break

        for i in range(len(program)):
            try:
                if output[i] == program[i]:
                    common[i] = common[i] & init
            except IndexError:
                break

    for k, v in common.items():
        print(f"{k}: {oct(v)}")


if __name__ == "__main__":
    main()
