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


@cache
def next(input_):
    input_ = input_ ^ (input_ * 64) % 16777216
    input_ = input_ ^ (input_ // 32) % 16777216
    input_ = input_ ^ (input_ * 2048) % 16777216
    return input_


def part1():
    lines = iter(stdin.read().strip().splitlines())

    final = 0
    for line in tqdm(lines):
        secret = int(line)
        for _ in range(2000):
            secret = next(secret)
        final += secret

    print(final)


def part2():
    lines = iter(stdin.read().strip().splitlines())

    lookup_all = []
    for line in tqdm(lines):
        secret = int(line)
        diffs = []
        lookup = {}
        for _ in range(2000):
            next_secret = next(secret)
            diffs.append(next_secret % 10 - secret % 10)
            if len(diffs) > 3:
                seq = tuple(diffs[-4:])
                if seq not in lookup:
                    lookup[seq] = next_secret % 10
            secret = next_secret

        lookup_all.append(lookup)

    all_sequences = set(chain(*(lookup.keys() for lookup in lookup_all)))
    # print(all_sequences)

    max_bananas = 0
    best_seq = None

    for sequence in tqdm(all_sequences):
        bananas = 0
        for lookup in lookup_all:
            bananas += lookup.get(sequence, 0)

        if bananas > max_bananas:
            max_bananas = bananas
            best_seq = sequence

    print(best_seq)
    print(max_bananas)


if __name__ == "__main__":
    # part1()
    part2()
