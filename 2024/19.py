from collections import defaultdict
from copy import deepcopy
from functools import cache, cmp_to_key, reduce
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


@cache
def solve(pattern: str, towels: set[str]) -> int:
    if pattern == "":
        return 1

    res = 0
    for towel in towels:
        if pattern.startswith(towel):
            tail = pattern[len(towel) :]
            tail_res = solve(tail, towels)
            res += tail_res
            # print(f"{pattern} starts with {towel}, remaining {tail}")

    return res


def main():
    lines = iter(stdin.read().strip().splitlines())

    towels = frozenset(towel.strip() for towel in next(lines).split(","))
    next(lines)

    part_1 = 0
    part_2 = 0
    for pattern in lines:
        res = solve(pattern, towels)
        if res:
            part_1 += 1
            part_2 += res

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


if __name__ == "__main__":
    main()
