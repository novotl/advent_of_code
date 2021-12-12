if __name__ == "__main__":
    from .solution import Puzzle
    from advent_of_code.runner import attach_cli
    from pathlib import Path

    attach_cli(Puzzle, Path(__file__).parent)
