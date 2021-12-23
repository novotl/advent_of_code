from collections import Counter
from typing import Iterable, Literal, NamedTuple, Optional
from dataclasses import dataclass
import re
from advent_of_code.runner import PuzzleTemplate

CUBE_REGEX = re.compile(r"-?\d+")


class Point(NamedTuple):
    x: int
    y: int
    z: int


def intersects(a_max: Point, a_min: Point, b_max: Point, b_min: Point) -> bool:
    # thanks random stranger on the internet: https://stackoverflow.com/a/53488289/8320732
    return (
        a_max.x >= b_min.x
        and a_min.x <= b_max.x
        and a_max.y >= b_min.y
        and a_min.y <= b_max.y
        and a_max.z >= b_min.z
        and a_min.z <= b_max.z
    )


@dataclass(frozen=True)
class Cube:
    max_point: Point
    min_point: Point
    sign: Literal[1, -1]

    @classmethod
    def from_string(cls, string: str) -> "Cube":
        """
        >>> Cube.from_string('on x=-20..26,y=-36..17,z=-47..7')
        Cube(max_point=Point(x=26, y=17, z=7), min_point=Point(x=-20, y=-36, z=-47), sign=1)

        >>> Cube.from_string('off x=-48..-32,y=26..41,z=-47..-37')
        Cube(max_point=Point(x=-32, y=41, z=-37), min_point=Point(x=-48, y=26, z=-47), sign=-1)
        """
        sign, rest = string.split(" ")
        x_min, x_max, y_min, y_max, z_min, z_max = map(int, CUBE_REGEX.findall(rest))
        max_point = Point(x_max, y_max, z_max)
        min_point = Point(x_min, y_min, z_min)
        return cls(min_point=min_point, max_point=max_point, sign=1 if sign == "on" else -1)

    def crop(
        self, max_point: Point = Point(50, 50, 50), min_point: Point = Point(-50, -50, -50)
    ) -> Optional["Cube"]:
        """
        >>> Cube.from_string('off x=-48..-32,y=26..41,z=-47..-37').crop()
        Cube(max_point=Point(x=-32, y=41, z=-37), min_point=Point(x=-48, y=26, z=-47), sign=-1)

        >>> Cube.from_string('off x=-52..52,y=-52..52,z=-52..52').crop()
        Cube(max_point=Point(x=50, y=50, z=50), min_point=Point(x=-50, y=-50, z=-50), sign=-1)

        >>> Cube.from_string('off x=100..110,y=100..110,z=100..110').crop()
        """
        if not intersects(self.max_point, self.min_point, max_point, min_point):
            return None

        new_max_point = Point(*map(lambda x: max(-50, min(50, x)), self.max_point))
        new_min_point = Point(*map(lambda x: max(-50, min(50, x)), self.min_point))

        return Cube(max_point=new_max_point, min_point=new_min_point, sign=self.sign)

    def area(self) -> int:
        """
        >>> Cube.from_string('on x=10..12,y=10..12,z=10..12').area()
        27

        >>> Cube.from_string('off x=10..12,y=10..12,z=10..12').area()
        -27
        """
        return (
            (self.max_point.x - self.min_point.x + 1)
            * (self.max_point.y - self.min_point.y + 1)
            * (self.max_point.z - self.min_point.z + 1)
        ) * self.sign

    def opposite(self) -> "Cube":
        """
        >>> a = Cube.from_string('on x=10..12,y=10..12,z=10..12').opposite()
        >>> b = Cube.from_string('off x=10..12,y=10..12,z=10..12')
        >>> a == b
        True
        """
        return Cube(min_point=self.min_point, max_point=self.max_point, sign=-self.sign)

    def intersection(self, other: "Cube") -> Optional["Cube"]:
        """
        >>> a = Cube.from_string('on x=10..12,y=10..12,z=10..12')
        >>> b = Cube.from_string('on x=11..13,y=11..13,z=11..13')
        >>> intersection = a.intersection(b)
        >>> intersection
        Cube(max_point=Point(x=12, y=12, z=12), min_point=Point(x=11, y=11, z=11), sign=-1)
        >>> intersection.area()
        -8

        >>> c = Cube.from_string('on x=5..8,y=5..8,z=5..8')
        >>> a.intersection(c)
        """
        # test if there is intersection
        if not intersects(self.max_point, self.min_point, other.max_point, other.min_point):
            return None

        # we're adding some cube twice -> subtract it once
        # we're subtracting some cube twice -> add it once
        if self.sign == other.sign:
            new_sign = -self.sign
        # we need to switch off part of lit cube
        # this cube is negative (it turned of some other cube) -> we need to light it back up
        else:
            new_sign = other.sign

        new_max = Point(
            min(self.max_point.x, other.max_point.x),
            min(self.max_point.y, other.max_point.y),
            min(self.max_point.z, other.max_point.z),
        )

        new_min = Point(
            max(self.min_point.x, other.min_point.x),
            max(self.min_point.y, other.min_point.y),
            max(self.min_point.z, other.min_point.z),
        )

        return Cube(min_point=new_min, max_point=new_max, sign=new_sign)

    def __str__(self) -> str:
        sign = "on" if self.sign == 1 else "off"
        return f"{sign} x={self.min_point.x}..{self.max_point.x},y={self.min_point.y}..{self.max_point.y},z={self.min_point.z}..{self.max_point.z}"


@dataclass
class Puzzle(PuzzleTemplate):
    cubes: list[Cube]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        cubes = [Cube.from_string(line.strip()) for line in lines]

        return cls(cubes=cubes)

    def solve(self) -> Counter[Cube]:
        final_cubes = Counter()

        for new_cube in self.cubes:
            new_cubes = []

            for cube in final_cubes.keys():
                if intersection := cube.intersection(new_cube):
                    new_cubes.append(intersection)

            if new_cube.sign == 1:
                # we cannot add a negative cube, because everything is turned off
                new_cubes.append(new_cube)

            for cube in new_cubes:
                # if we have one cube in "on" and the same one in "off", they will cancel out
                opposite = cube.opposite()
                if opposite in final_cubes:
                    final_cubes[opposite] -= 1
                    if final_cubes[opposite] == 0:
                        del final_cubes[opposite]
                else:
                    final_cubes[cube] += 1

        return final_cubes

    def task_one(self) -> int:
        cubes = self.solve()
        cropped = (cube.crop() for cube in cubes)
        return sum(cube.area() for cube in cropped if cube)

    def task_two(self) -> int:
        cubes = self.solve()
        return sum(cube.area() for cube in cubes)
