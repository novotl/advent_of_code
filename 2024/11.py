from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key, lru_cache
from itertools import chain
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from tqdm import tqdm
from operator import add, mul


@lru_cache(maxsize=None)
def blink(stone, times: int):
    if times == 0:
        return 1
    elif stone == 0:
        return blink(1, times - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        mid = len(s) // 2
        return blink(int(s[:mid]), times - 1) + blink(int(s[mid:]), times - 1)
    else:
        return blink(stone * 2024, times - 1)


def main():
    lines = stdin.read().strip().splitlines()

    [*stones] = map(int, lines[0].split())
    iters = 75
    print(sum(blink(stone, iters) for stone in stones))


if __name__ == "__main__":
    main()
