from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key
from sys import stdin
import re
from dataclasses import dataclass

from operator import add, mul

def concat(x, y):
    return int(f'{x}{y}')


def recursion(total: int, nums: list[int], i: int, target: int) -> int:
    if i >= len(nums):
        return total == target

    for op in (add, mul, concat):
        next_ = op(total, nums[i])
        if recursion(next_, nums, i+1, target):
            return True
        
    return False


def main():
    lines = stdin.read().strip().splitlines()

    res = 0
    for line in lines:
        l, r = line.split(":")
        target = int(l)
        nums = list(map(int, r.split()))

        print(f"{target} | {nums}")
        if recursion(nums[0], nums, 1, target):
            res += target
    print(res)


if __name__ == "__main__":
    main()
