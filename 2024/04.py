import re
from sys import stdin
from itertools import chain


def forwards_horizontal(grid):
    for r in grid:
        yield "...."
        yield from r
        yield "...."


def backwards_horizontal(grid):
    yield "...."
    yield from reversed(list(forwards_horizontal(grid)))
    yield "...."


def forwards_vertical(grid):
    for c_index in range(len(grid[0])):
        yield "...."
        for r in grid:
            yield r[c_index]
        yield "...."


def backwards_vertical(grid):
    yield "...."
    yield from reversed(list(forwards_vertical(grid)))
    yield "...."


def diag_tl_br(grid):
    rows = len(grid)
    cols = len(grid[0])

    def gen(r, c):
        yield grid[r][c]

        while True:
            r += 1
            c += 1

            try:
                yield grid[r][c]

            except IndexError:
                yield "...."
                return

    for s in range(rows):
        r, c = (s, 0)
        yield "...."
        yield from gen(r, c)
        yield "...."

    for s in range(1, cols):
        r, c = (0, s)
        yield "...."
        yield from gen(r, c)
        yield "...."


def diag_bl_tr(grid):
    rows = len(grid)
    cols = len(grid[0])

    def gen(r, c):
        yield grid[r][c]

        while True:
            r -= 1
            c += 1

            try:
                if r < 0:
                    raise IndexError
                yield grid[r][c]

            except IndexError:
                yield "...."
                return

    for s in range(rows):
        r, c = (s, 0)

        yield "...."
        yield from gen(r, c)
        yield "...."

    for s in range(1, cols):
        r, c = (rows - 1, s)
        yield "...."
        yield from gen(r, c)
        yield "...."


def diag_tr_bl(grid):
    yield "...."
    yield from reversed(list(diag_bl_tr(grid)))
    yield "...."


def diag_br_tl(grid):
    yield "...."
    yield from reversed(list(diag_tl_br(grid)))
    yield "...."


def main_part1():
    lines = stdin.read().strip().splitlines()

    grid = [list(line) for line in lines]

    all_directions = "".join(
        chain(
            forwards_horizontal(grid),
            backwards_horizontal(grid),
            forwards_vertical(grid),
            backwards_vertical(grid),
            diag_tl_br(grid),
            diag_br_tl(grid),
            diag_tr_bl(grid),
            diag_bl_tr(grid),
        )
    )

    # print(all_directions)

    matches = re.findall(r"XMAS", all_directions)
    print(len(matches))


def main_part2():
    lines = stdin.read().strip().splitlines()

    grid = [list(line) for line in lines]

    rows = len(grid)
    cols = len(grid[0])

    count = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # print((r, c))
            if grid[r][c] != "A":
                continue

            if (grid[r - 1][c - 1] != "M" or grid[r + 1][c + 1] != "S") and (
                grid[r + 1][c + 1] != "M" or grid[r - 1][c - 1] != "S"
            ):
                continue

            if (grid[r + 1][c - 1] != "M" or grid[r - 1][c + 1] != "S") and (
                grid[r - 1][c + 1] != "M" or grid[r + 1][c - 1] != "S"
            ):
                continue

            count += 1

    print(count)


if __name__ == "__main__":
    main_part1()
    # main_part2()
