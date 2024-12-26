from collections import defaultdict
from functools import cmp_to_key
from sys import stdin
import re


def correct(rules: dict[int, int], seq: list[int]) -> bool:
    seen = set()
    for num in seq:
        if any(invalid in seen for invalid in rules.get(num, [])):
            raise ValueError

        seen.add(num)
    else:
        return seq[len(seq) // 2]


def main():
    input_line = iter(stdin.read().strip().splitlines())

    # before -> after
    rules = defaultdict(set)

    for line in input_line:
        if not line:
            break

        [a, b] = map(int, line.split("|"))
        rules[a].add(b)

    res = 0
    for i, line in enumerate(input_line, start=1):
        seq = list(map(int, line.split(",")))
        try:
            correct(rules, seq)
            # res += correct(rules, seq)
            print(f"Line {i} valid")
        except ValueError:
            print(f"Line {i} not valid")

            def ordering(x, y):
                if y in rules.get(x, []):
                    return -1
                elif x in rules.get(y, []):
                    return 1
                return 0

            seq.sort(key=cmp_to_key(ordering))
            res += seq[len(seq) // 2]

    print(res)


if __name__ == "__main__":
    main()
