from collections import Counter, defaultdict
from copy import deepcopy
from functools import cache, cmp_to_key, reduce
from itertools import chain, combinations, count, product
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

DIRECTIONAL = {
    "A": {"<": "^", "v": ">"},
    "^": {"v": "v", ">": "A"},
    ">": {"<": "v", "^": "A"},
    "<": {">": "v"},
    "v": {"<": "<", "^": "^", ">": ">"},
}

NUMERICAL = {
    "A": {"<": "0", "^": "3"},
    "0": {">": "A", "^": "2"},
    "1": {"^": "4", ">": "2"},
    "2": {"<": "1", "^": "5", "v": "0", ">": "3"},
    "3": {"<": "2", "^": "6", "v": "A"},
    "4": {"^": "7", "v": "1", ">": "5"},
    "5": {"<": "4", "^": "8", "v": "2", ">": "6"},
    "6": {"<": "5", "^": "9", "v": "3"},
    "7": {"v": "4", ">": "8"},
    "8": {"<": "7", "v": "5", ">": "9"},
    "9": {"<": "8", "v": "6"},
}

# trick to have hashable input to functions
KEYBOARDS = [NUMERICAL, DIRECTIONAL]
NUM = 0
DIR = 1


@cache
def search_bfs(start, goal, keyboard_id):
    graph = KEYBOARDS[keyboard_id]
    queue = [(start, "")]
    best = None

    res = []

    while queue:
        current, seq = queue.pop(0)
        if best and len(seq) > best:
            return res

        if current == goal:
            best = len(seq)
            res.append(seq + "A")

        for move, next_ in graph[current].items():
            queue.append((next_, seq + move))


@cache
def recursion(input_: str, level: int, keyboard_id: int):
    res = 0
    for start, goal in zip("A" + input_[:-1], input_):
        paths = search_bfs(start, goal, keyboard_id)

        if level == 0:
            res += len(min(paths, key=len))
        else:
            res += min(recursion(path, level - 1, DIR) for path in paths)

    return res


def main():
    lines = iter(stdin.read().strip().splitlines())

    res = 0
    for line in lines:
        print(line)
        res += int(line[:-1]) * recursion(line, 25, NUM)
    print(res)


if __name__ == "__main__":
    main()
