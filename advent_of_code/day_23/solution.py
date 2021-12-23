from functools import lru_cache
from typing import Iterable, Literal, TypeVar
from dataclasses import dataclass
import heapq
from advent_of_code.runner import PuzzleTemplate
import re

AMPHIPODS = {"#": -1, ".": 0, "A": 1, "B": 10, "C": 100, "D": 1000}
AMPHIPODS_REV = {v: k for k, v in AMPHIPODS.items()}
HOME_BURROW = {1: 3, 10: 5, 100: 7, 1000: 9}

T = TypeVar("T")


def replace_tuple(tuple_: tuple[T, ...], index: int, new_value: T) -> tuple[T, ...]:
    """
    Tuples are immutable, this function creates a new tuple by replacing value at given index.
        >>> replace_tuple((1, 2, 3), 1, 5)
        (1, 5, 3)
    """
    list_ = list(tuple_)
    return tuple(list_[:index] + [new_value] + list_[index + 1 :])


def sign(i: int) -> Literal[-1, 0, 1]:
    """
    Signum function. Extracts sign of the given number

        >>> sign(42)
        1
        >>> sign(0)
        0
        >>> sign(-42)
        -1
    """
    if i > 0:
        return 1
    elif i < 0:
        return -1
    else:
        return 0


@dataclass(frozen=True)
class State:
    grid: tuple[tuple[int, ...], ...]

    def is_goal(self) -> bool:
        """
        Returns true for a State where all Amphipods are in correct burrows.
        """
        _, *burrows = self.grid
        return all(
            all(burrow[home_row] == amphipod for burrow in burrows)
            for amphipod, home_row in HOME_BURROW.items()
        )

    def next_states(self) -> list[tuple["State", int]]:
        hallway, *burrows = self.grid

        # All valid moves from hallway -> burrow
        for col in range(1, 12):
            if hallway[col] > 0:
                multiplier = hallway[col]
                home_col = HOME_BURROW[multiplier]
                # we cannot go into burrow if some is occupied by a different amphipod
                if any(
                    burrows[level][home_col] != 0 and burrows[level][home_col] != multiplier
                    for level in range(0, len(burrows))
                ):
                    continue

                dir_ = sign(home_col - col)
                assert dir_ != 0  # direction = 0 may never happen (forbidden tile)

                for new_col in range(col + dir_, home_col, dir_):
                    if hallway[new_col] != 0:  # hallway is not empty
                        break
                else:
                    # allways go to the deepest possible spot in the burrow
                    deepest_burrow = max(
                        level for level in range(0, len(burrows)) if burrows[level][home_col] == 0
                    )
                    cost = (abs(home_col - col) + 1 + deepest_burrow) * multiplier

                    yield cost, State(
                        grid=(
                            replace_tuple(hallway, col, 0),
                            *replace_tuple(
                                burrows,
                                deepest_burrow,
                                replace_tuple(burrows[deepest_burrow], home_col, multiplier),
                            ),
                        )
                    )

        # All valid moves from burrow -> hallway
        for col in range(3, 10, 2):  # only valid burrow columns
            for burrow_level in range(0, len(burrows)):
                if burrows[burrow_level][col] <= 0:
                    continue  # nothing to move the square has no amphipod

                if any(burrows[level][col] != 0 for level in range(0, burrow_level)):
                    continue  # someone is blocking us in the burrow

                multiplier = burrows[burrow_level][col]
                ranges = (range(-1, -10, -1), range(1, 10))  # going left and going right
                for range_ in ranges:
                    for diff in range_:
                        if hallway[col + diff] == 0:  # hallway must be free
                            new_col = col + diff
                            if new_col in {3, 5, 7, 9}:  # cannot stand in front of a burrow
                                continue
                            # cost: moving out of burrow + one square in front of it + hallway
                            cost = (burrow_level + 1 + abs(diff)) * multiplier
                            yield cost, State(
                                grid=(
                                    replace_tuple(hallway, new_col, multiplier),
                                    *replace_tuple(
                                        burrows,
                                        burrow_level,
                                        replace_tuple(burrows[burrow_level], col, 0),
                                    ),
                                )
                            )
                        else:
                            # hallway is blocked, cannot go any further
                            break

    def __str__(self) -> str:
        lines = (
            "",
            "".join("#" * 13),
            *("".join(AMPHIPODS_REV[char] for char in self.grid[i]) for i in range(len(self.grid))),
            "".join("#" * 13),
            "",
        )

        return "\n".join(lines)

    def __lt__(self, other: "State") -> bool:
        # we're ordering by (cost, State), if cost is the same, we don't care which State is
        # explored first
        return False


@dataclass
class Puzzle(PuzzleTemplate):
    init_state: State

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        it = iter(lines)

        next(it)  # top wall
        hallway = tuple(AMPHIPODS[i] for i in next(it).strip())

        burrows = []

        for line in (line.strip() for line in it):
            if all(char == "#" for char in line):
                break
            burrow = tuple(map(lambda x: AMPHIPODS[x], line.strip().center(13, "#")))
            burrows.append(burrow)

        return cls(init_state=State(grid=(hallway, *tuple(burrows))))

    @staticmethod
    def solve(init_state: State) -> int:
        heap: list[tuple[int, State]] = []
        heapq.heappush(heap, (0, init_state))
        visited = set()

        while heap:
            cost, state = heapq.heappop(heap)
            # thanks to the heap, we always pop the lowest cost to the state first, so if it's in
            # visited, we already found a cheaper route and it's not worth exploring further
            if state in visited:
                continue

            visited.add(state)
            if state.is_goal():
                return cost

            for next_cost, next_state in state.next_states():
                assert next_cost > 0
                if next_state not in visited:
                    heapq.heappush(heap, (cost + next_cost, next_state))

    def task_one(self) -> int:
        hallway, *burrows = self.init_state.grid
        minimized = State(grid=(hallway, burrows[0], burrows[-1]))
        return self.solve(minimized)

    def task_two(self) -> int:
        return self.solve(self.init_state)
