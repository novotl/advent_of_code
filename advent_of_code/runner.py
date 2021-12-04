from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional, Type, TypeVar
import click
import time
from datetime import timedelta
from pathlib import Path
from typing import Any
from enum import Enum


class PuzzleTemplate(ABC):
    @classmethod
    @abstractmethod
    def from_lines(cls, lines: Iterable[str]) -> "PuzzleTemplate":
        raise NotImplementedError()

    @abstractmethod
    def task_one(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def task_two(self) -> int:
        raise NotImplementedError()


T = TypeVar("T")


def time_it(func: Callable[[], T]) -> T:
    tic = time.time()
    result = func()
    toc = time.time()
    print(f"Execution took: {timedelta(seconds=toc - tic)}")
    return result


def get_solution(path: Path) -> Optional[str]:
    if path.exists():
        with path.open() as f:
            return "".join((line.strip() for line in f.readlines()))

    return None


def verify_solution(actual: Any, expected: str):
    _actual = str(actual)
    if not expected:
        print(f"\U00002753 {actual}")
    elif expected == _actual:
        print(f"\U00002705 {actual}")
    else:
        print(f"\U0000274C {actual}, the correct solution is: {expected}")


class InstanceSize(Enum):
    SMALL = "small"
    BIG = "big"


def _puzzle_runner(puzzle: Type[PuzzleTemplate], instance_size: InstanceSize, directory: Path):
    print(f"--- \N{christmas tree} Running {instance_size.value} instance \N{christmas tree} ---")
    directory = directory / "assets"
    puzzle_input = directory / f"input_{instance_size.value}.txt"
    with puzzle_input.open() as f:
        puzzle = puzzle.from_lines(f.readlines())
        one = time_it(lambda: puzzle.task_one())
        verify_solution(one, get_solution(directory / f"solution_{instance_size.value}_one.txt"))

        print()

        two = time_it(lambda: puzzle.task_two())
        verify_solution(two, get_solution(directory / f"solution_{instance_size.value}_two.txt"))


def attach_cli(puzzle: Type[PuzzleTemplate], directory: Path):
    @click.command()
    @click.option("--small", is_flag=True, help="Computes solution for the small puzzle instance")
    @click.option("--big", is_flag=True, help="Computes solutions for the big puzzle instance")
    def solve(small: bool, big: bool):
        if small:
            _puzzle_runner(puzzle, InstanceSize.SMALL, directory)

        if small and big:
            print()

        if big:
            _puzzle_runner(puzzle, InstanceSize.BIG, directory)

    solve()
