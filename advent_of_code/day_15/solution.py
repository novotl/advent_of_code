from typing import Iterable, NamedTuple
from dataclasses import dataclass
import heapq

from advent_of_code.runner import PuzzleTemplate


class Point(NamedTuple):
    r: int
    c: int

    def __add__(self, other: "Point") -> "Point":
        """
        >>> a, b = Point(1, 2), Point(3, 4)
        >>> a + b
        Point(r=4, c=6)
        """
        return self.__class__(self.r + other.r, self.c + other.c)

    def manhattan_distance(self, other: "Point") -> int:
        """
        >>> a, b = Point(1, 2), Point(3, 4)
        >>> a.manhattan_distance(b)
        4
        >>> a.manhattan_distance(b) == b.manhattan_distance(a)
        True
        """
        return abs(self.r - other.r) + abs(self.c - other.c)


@dataclass
class Puzzle(PuzzleTemplate):
    grid: list[list[int]]
    rows: int
    cols: int

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        grid = [[int(char) for char in line.strip()] for line in lines]

        return cls(grid=grid)

    def is_valid(self, point: Point) -> bool:
        return 0 <= point.r < self.rows and 0 <= point.c < self.cols

    def heuristics(self, point: Point, goal: Point) -> int:
        return point.manhattan_distance(goal)

    def shortest_path(self, start: Point, goal: Point) -> int:
        """
        A* algorithm for shortest paths.
        """
        heap: list[tuple[int, Point]] = []
        heapq.heappush(heap, (self.heuristics(start, goal), start))
        visited = set()
        best_cost: dict[Point, int] = {}

        while heap:
            current_cost_with_heuristics, current_point = heapq.heappop(heap)
            current_cost = current_cost_with_heuristics - self.heuristics(current_point, goal)

            if current_point == goal:
                print(f"The search expanded {len(visited)} nodes.")
                return current_cost

            if current_point in visited:
                # we already explored this point with lower cost, ignore it
                continue

            visited.add(current_point)

            for diff in (Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)):
                new_point = current_point + diff
                if self.is_valid(new_point) and new_point not in visited:
                    this_cost = self.grid[new_point.r][new_point.c]
                    this_heuristics = self.heuristics(new_point, goal)
                    total_cost = current_cost + this_cost + this_heuristics
                    if best_cost.get(new_point, total_cost + 1) > total_cost:
                        best_cost[new_point] = total_cost
                        heapq.heappush(heap, (total_cost, new_point))

    def task_one(self) -> int:
        return self.shortest_path(start=Point(0, 0), goal=Point(r=self.rows - 1, c=self.cols - 1))

    def task_two(self, repeat_rows: int = 5, repeat_cols: int = 5) -> int:
        new_grid = [[0] * self.cols * repeat_cols for _ in range(self.rows * repeat_rows)]

        for row_multiplier in range(0, repeat_rows):
            for col_multiplier in range(0, repeat_cols):
                for r in range(self.rows):
                    for c in range(self.cols):
                        original = self.grid[r][c]
                        # position of the point in the new bigger grid
                        new_r, new_c = (
                            r + row_multiplier * self.rows,
                            c + col_multiplier * self.cols,
                        )
                        # in each new replication (down and right), the cost grows by one
                        # and. Values above 9 wrap back around to 1
                        new_grid[new_r][new_c] = (
                            (original + row_multiplier + col_multiplier - 1) % 9
                        ) + 1

        return self.__class__(grid=new_grid).task_one()
