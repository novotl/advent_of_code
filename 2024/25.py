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

def fit(lock, key):
    for i in range(len(lock)):
        if key[i] > lock[i]:
            return False
    
    return True

def main():
    lines = iter(stdin.read().strip().splitlines())

    locks = []
    keys = []
    rows = None
    cols = None

    done = False
    while not done:
        diagram = []
        for line in lines:
            if not line:
                break

            diagram.append(list(line))

        if not diagram:
            done = True
            break

        rows = len(diagram)
        cols = len(diagram[0])

        if all(c == '#' for c in diagram[0]):
            type_ = locks
            char = '.'
        else:
            type_ = keys
            char = '#'

        nums = []
        for c in range(cols):
            nums.append(sum(1 for r in range(rows) if diagram[r][c] == char) - 1)

        type_.append(tuple(nums))
        print("Done")

    res = 0
    for lock in locks:
        for key in keys:
            if fit(lock, key):
                res += 1
                print(f"Lock {lock} and key {key} all columns fit!")

    # print(f"Keys: {keys}")
    # print(f"Locks: {locks}")
    print(res)
if __name__ == "__main__":
    main()
