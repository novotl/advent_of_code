from functools import lru_cache
from typing import Iterable, Match, NamedTuple, Optional
from dataclasses import dataclass, field

from advent_of_code.runner import PuzzleTemplate
from collections import defaultdict
from pprint import pprint
from collections import deque
from itertools import permutations, product, combinations


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: "Point") -> "Point":
        """
        >>> a, b = Point(10, 2, 3), Point(-1, -1, -6)
        >>> a + b
        Point(x=9, y=1, z=-3)
        """
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        """
        >>> a, b = Point(10, 2, 3), Point(-1, -1, -6)
        >>> a - b
        Point(x=11, y=3, z=9)
        """

        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def manhattan_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass
class Puzzle(PuzzleTemplate):
    # scanner -> pointcloud of beacons
    pointclouds: dict[int, set[Point]]
    # used to cache all pointcloud rotations
    _cached_pointclouds: dict[int, dict[int, set[Point]]]
    _solution: Optional[tuple[int, int]] = None

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        scanners = defaultdict(set)
        current_scanner = -1
        for line in (line.strip() for line in lines):
            if not line:
                continue

            if line.startswith("---"):
                current_scanner += 1
                continue

            scanners[current_scanner].add(Point(*map(int, line.split(","))))

        return cls(
            pointclouds=dict(scanners), _cached_pointclouds=defaultdict(lambda: defaultdict(set))
        )

    def find(
        self, reference_point: Point, scanner: int, check: set[Point]
    ) -> Optional[tuple[Point, tuple[int, Point]]]:
        ordinal = -2
        for x, y, z in permutations((lambda p: p.x, lambda p: p.y, lambda p: p.z)):
            ordinal += 1
            for mx, my, mz in product((-1, 1), repeat=3):
                ordinal += 1
                if not self._cached_pointclouds[scanner][ordinal]:
                    self._cached_pointclouds[scanner][ordinal] = {
                        Point(x(point) * mx, y(point) * my, z(point) * mz)
                        for point in self.pointclouds[scanner]
                    }

                for point in self._cached_pointclouds[scanner][ordinal]:
                    translation = reference_point - point

                    new_points = {
                        point + translation for point in self._cached_pointclouds[scanner][ordinal]
                    }

                    if len(new_points.intersection(check)) >= 12:
                        print(f"{scanner}: {translation}")
                        return translation, new_points

    def solution(self) -> tuple[int, int]:
        if not self._solution:
            pointcloud = set(self.pointclouds[0])
            candidates = set(self.pointclouds[0])
            found = {0}
            transformations = [Point(0, 0, 0)]

            while len(found) != len(self.pointclouds):
                candidate = candidates.pop()
                for key in self.pointclouds.keys() - found:
                    matches = self.find(reference_point=candidate, scanner=key, check=pointcloud)

                    if matches:
                        transformation, new_points = matches
                        transformations.append(transformation)
                        candidates = candidates.union(new_points)
                        pointcloud = pointcloud.union(new_points)
                        found.add(key)

            max_ = 0
            for a, b in combinations(transformations, r=2):
                max_ = max(max_, a.manhattan_distance(b))

            self._solution = len(pointcloud), max_

        return self._solution

    def task_one(self) -> int:
        part_one, _ = self.solution()
        return part_one

    def task_two(self) -> int:
        _, part_two = self.solution()
        return part_two
