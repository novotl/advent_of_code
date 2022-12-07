from typing import Iterable
from dataclasses import dataclass
from collections import deque
from advent_of_code.runner import PuzzleTemplate
from copy import deepcopy
from itertools import chain


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    children: list

    @property
    def size(self):
        return sum(child.size for child in self.children)

    def task_one(self, limit):
        size = self.size

        res = list(
            chain(*(child.task_one(limit) for child in self.children if isinstance(child, Folder)))
        )

        if size <= limit:
            res.append(self)

        return res

    def task_two(self, limit):
        size = self.size

        res = list(
            chain(*(child.task_two(limit) for child in self.children if isinstance(child, Folder)))
        )

        if size >= limit:
            res.append(self)

        return res


def rec_parse(lines, name):
    files = []

    for line in lines:
        if line == "$ ls":
            continue
        elif line == "$ cd ..":
            break
        elif line.startswith("$ cd"):
            dir_name = line.split()[2]
            files.append(rec_parse(lines, dir_name))
        else:
            parts = line.split()
            if parts[0] == "dir":
                continue
            else:
                files.append(File(name=parts[1], size=int(parts[0])))

    return Folder(name, files)


@dataclass
class Puzzle(PuzzleTemplate):
    def __init__(self, folder: Folder) -> None:
        self.folder = folder

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        lines = (line.strip() for line in lines)
        next(lines)

        folder = rec_parse(lines, "/")
        return cls(folder)

    def task_one(self, size: int = 4) -> int:
        res = self.folder.task_one(100_000)
        print(res)
        return sum(folder.size for folder in res)

    def task_two(self) -> int:
        total_space = 70_000_000
        required_space = 30_000_000

        free_space = total_space - self.folder.size
        need_to_free_up = required_space - free_space

        print(f"Need to free up: {need_to_free_up}")
        res = self.folder.task_two(need_to_free_up)

        return min(folder.size for folder in res)
