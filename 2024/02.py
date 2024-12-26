from sys import stdin


def is_safe(levels: list[int]) -> bool:
    it_ = iter(levels)

    prev = next(it_)
    asc = None
    for curr in it_:
        diff = prev - curr

        if asc and diff < 0:
            return False
        elif asc is False and diff > 0:
            return False
        elif diff > 0:
            asc = True
        else:
            asc = False

        if not (1 <= abs(diff) <= 3):
            return False
        prev = curr

    return True


def main():
    input_lines = stdin.read().strip().splitlines()

    safe = 0

    for report in input_lines:
        levels = list(map(int, report.split()))

        if is_safe(levels):
            safe += 1
        else:
            for i in range(len(levels)):
                if is_safe(levels[:i] + levels[i + 1 :]):
                    safe += 1
                    break

    print(safe)


if __name__ == "__main__":
    main()
