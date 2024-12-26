from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass

from operator import add, mul
from typing import Iterable
import numpy as np
from sympy import diophantine, symbols

COST_A = 3
COST_B = 1


def parse_button(line):
    A = re.match(r".*X\+(\d+), Y\+(\d+)", line)
    return map(int, A.groups())


def parse_prize(line):
    A = re.match(r".*X=(\d+), Y=(\d+)", line)
    return map(int, A.groups())


def main():
    lines = iter(stdin.read().splitlines())
    total_cost = 0

    while True:
        try:
            next(lines)
        except StopIteration:
            break
        ax, ay = parse_button(next(lines))
        bx, by = parse_button(next(lines))
        px, py = parse_prize(next(lines))
        px += 10000000000000
        py += 10000000000000

        b = (ax * py - ay * px) / (ax * by - ay * bx)
        a = (px - b * bx) / ax

        if a % 1 == 0 and b % 1 == 0:
            total_cost += a * COST_A + b * COST_B
        

    print(int(total_cost))


if __name__ == "__main__":
    main()
