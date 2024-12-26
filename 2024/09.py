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


def part_1(
    disk: list[int], full_positions: list[int], free_positions: list[int]
) -> list[int]:
    while True:
        full = full_positions.pop()
        free = free_positions.pop(0)

        if full <= free:
            break

        disk[free] = disk[full]
        disk[full] = None


def part_2(
    disk: list[int], full_positions: list[int], free_positions: list[int]
) -> list[int]:
    print(disk)
    while True:
        # right most file
        full = full_positions.pop()
        file_size = 1

        try:
            while disk[full_positions[-1]] == disk[full]:
                full_positions.pop()
                file_size += 1
        except IndexError:
            return 

        print(f"File {disk[full]}: {file_size}")
        # leftmost free space
        prev_pos = None
        prev_id = None
        free_size = 0
        for i, pos in enumerate(free_positions):
            if pos >= full:
                break
            if prev_pos is None or prev_pos + 1 != pos:
                prev_pos = pos
                prev_id = i
                free_size = 1
            else:
                prev_pos = pos
                prev_id = i
                free_size += 1

            if free_size == file_size:
                print(f"Free {pos}: {free_size}")
                for i in range(file_size):
                    disk[prev_pos - i] = disk[full - i]
                    disk[full - i] = None
                    free_positions.pop(prev_id - i)
                break

        # print(disk)
        # print(free_positions)
        # print(full_positions)
        # print("---")


def main():
    lines = stdin.read().strip().splitlines()

    disk = []
    free_positions = []
    full_positions = []

    file_id = 0
    is_file = True
    for char in lines[0]:
        # print(char)
        size = int(char)
        if is_file:
            for _ in range(size):
                full_positions.append(len(disk))
                disk.append(file_id)
            file_id += 1
        else:
            for _ in range(size):
                free_positions.append(len(disk))
                disk.append(None)
        is_file = not is_file

    # part_1(disk=disk, full_positions=full_positions, free_positions=free_positions)
    part_2(disk=disk, full_positions=full_positions, free_positions=free_positions)

    print(disk)
    print(free_positions)
    print(full_positions)

    ret = 0
    for i, v in enumerate(disk):
        if v is None:
            continue
        ret += i * v

    print(ret)


if __name__ == "__main__":
    main()
