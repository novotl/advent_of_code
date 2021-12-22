from typing import Iterable, Optional, Tuple, Union
from dataclasses import dataclass
import json
from advent_of_code.runner import PuzzleTemplate
from math import ceil, floor
from functools import reduce
from itertools import permutations

SnailfishNumber = Union[int, "SnailfishNumber"]


def add_left(number: SnailfishNumber, add: int) -> SnailfishNumber:
    """
    Performs addition to the leftmost element of the tree.

    >>> add_left([[1, 2], 3], 2)
    [[3, 2], 3]
    """
    if add == 0:
        return number

    if isinstance(number, int):
        return number + add

    left, right = number
    return [add_left(left, add), right]


def add_right(number: SnailfishNumber, add: int) -> SnailfishNumber:
    """
    Performs addition to hte rightmost element of the tree.

    >>> add_right([1, [2, 3]], 2)
    [1, [2, 5]]
    """
    if add == 0:
        return number

    if isinstance(number, int):
        return number + add

    left, right = number
    return [left, add_right(right, add)]


def explode(number: SnailfishNumber) -> SnailfishNumber:
    """
    >>> explode([[[[[9,8],1],2],3],4])
    [[[[0, 9], 2], 3], 4]

    >>> explode([7,[6,[5,[4,[3,2]]]]])
    [7, [6, [5, [7, 0]]]]

    >>> explode([[6,[5,[4,[3,2]]]],1])
    [[6, [5, [7, 0]]], 3]

    >>> explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]

    # >>> explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    # [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]
    """

    def explode_helper(
        exploded: bool, number: SnailfishNumber, depth: int
    ) -> Tuple[bool, Optional[SnailfishNumber], int, int]:
        # only one explosion per reduction step, also cannot explode element
        if exploded or isinstance(number, int):
            return exploded, number, 0, 0

        left, right = number
        if depth >= 4:
            # depth >=4 means explode
            assert isinstance(left, int)
            assert isinstance(right, int)
            return True, None, left, right

        exploded, left, left_left, left_right = explode_helper(exploded, left, depth + 1)
        if left is None:
            return exploded, [0, add_left(right, left_right)], left_left, 0

        # we need to pass exploded flag around, otherwise we could explode in both left and right
        exploded, right, right_left, right_right = explode_helper(exploded, right, depth + 1)
        if right is None:
            return exploded, [add_right(left, right_left), 0], 0, right_right

        return (
            exploded,
            [add_right(left, right_left), add_left(right, left_right)],
            left_left,
            right_right,
        )

    _, snail, _, _ = explode_helper(False, number, 0)
    return snail


def split(number: SnailfishNumber) -> SnailfishNumber:
    """
    >>> split([[[[0,7],4],[15,[0,13]]],[1,1]])
    [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]

    >>> split([[[[0,7],4],[[7,8],[0,13]]],[1,1]])
    [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]
    """

    def split_helper(splitted: bool, number: SnailfishNumber) -> Tuple[bool, SnailfishNumber]:
        if splitted:
            # if we already splitted don't split again
            return splitted, number

        if isinstance(number, int):
            if number > 9:
                return True, [floor(number / 2), ceil(number / 2)]

            return False, number

        # recursively split left and right branches
        left, right = number
        splitted, left_snail = split_helper(splitted, left)
        splitted, right_snail = split_helper(splitted, right)

        return splitted, [left_snail, right_snail]

    _, number = split_helper(False, number)
    return number


def magnitude(number: SnailfishNumber) -> int:
    """
    >>> magnitude([9,1])
    29

    >>> magnitude([[9,1],[1,9]])
    129
    """
    if isinstance(number, int):
        return number

    left, right = number
    return 3 * magnitude(left) + 2 * magnitude(right)


def add(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    s = [a, b]

    while True:
        s_new = explode(s)
        if s_new != s:
            s = s_new
            continue

        s_new = split(s_new)
        if s_new != s:
            s = s_new
            continue

        s = s_new
        break

    return s


@dataclass
class Puzzle(PuzzleTemplate):
    lines: list[SnailfishNumber]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        return cls([json.loads(line.strip()) for line in lines])

    def task_one(self) -> int:
        number = reduce(add, self.lines[1:], self.lines[0])
        return magnitude(number)

    def task_two(self) -> int:
        max_ = 0
        for a, b in permutations(self.lines, r=2):
            max_ = max(max_, magnitude(add(a, b)))

        return max_
