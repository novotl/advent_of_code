from collections import defaultdict
from copy import deepcopy
from functools import cmp_to_key, reduce
from itertools import chain, combinations, count
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt
from typing import Iterable
from PIL import Image
import numpy as np
from tqdm import tqdm

@dataclass(frozen=True)
class Point:
    r: int
    c: int

    def __add__(self, p):
        return self.__class__(self.r + p.r, self.c + p.c)

    def __sub__(self, p):
        return self.__class__(self.r - p.r, self.c - p.c)

    def __mul__(self, coef):
        return self.__class__(self.r * coef, self.c * coef)

    def mod(self, x, y):
        return self.__class__(self.r % x, self.c % y)

    def __str__(self):
        return f"({self.r}, {self.c})"

    def __iter__(self):
        return iter((self.r, self.c))

    def rotate_right(self):
        return Point(self.c, -self.r)


class Robot:
    def __init__(self, s: str):
        [*nums] = map(int, re.match(r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", s).groups())
        self.pos = Point(nums[0], nums[1])
        self.vel = Point(nums[2], nums[3])

    def step(self, steps):
        self.pos += self.vel * steps

    def __str__(self):
        return f"{self.pos}; {self.vel}"


def main():
    lines = iter(stdin.read().strip().splitlines())

    robots = [Robot(line) for line in lines]

    wide = 101
    tall = 103

    # > 100
    # > 1000
    # < 10_000
    steps = 7055
    for r in robots:
        r.step(steps)

    for i in tqdm(range(1)):
    # for i in tqdm(range(1, 9000)):
        # for r in robots:
        #     r.step(1)

        data = np.zeros((tall, wide, 3), dtype=np.uint8)        
        positions = [r.pos.mod(wide, tall) for r in robots]

        for pos in positions:
            data[pos.c, pos.r] = [255, 255, 255]
        
        image = Image.fromarray(data)
        image.save(f'pics/{i}.png')
        # # with open(f"pics/{i}", "w") as f:
        # for t in range(tall):
        #     for w in range(wide):
        #         p = Point(w, t)
        #         robot_positions = sum(p == r for r in positions)
        #         if not robot_positions:
        #             print(".", end="")
        #             # f.write(".")
        #         else:
        #             print(robot_positions, end="")
        #             # f.write("*")
        #     print("")
            # f.write("\n")

    # quads = [(lt, lt), (gt, lt), (lt, gt), (gt, gt)]
    # w = wide // 2
    # t = tall // 2

    # s = [0, 0, 0, 0]
    # for e, quad in enumerate(quads):
    #     q1, q2 = quad
    #     for p in positions:
    #         x, y = p
    #         if q1(x, w) and q2(y, t):
    #             s[e] += 1
    # print(s)
    # print(reduce(mul, s))


if __name__ == "__main__":
    main()
