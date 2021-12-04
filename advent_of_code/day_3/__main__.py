from .solution import Puzzle
from advent_of_code.runner import attach_cli
from pathlib import Path


if __name__ == "__main__":
    attach_cli(Puzzle, Path(__file__).parent)
