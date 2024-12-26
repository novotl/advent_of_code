from collections import Counter
from sys import stdin


def main():
    input_lines = stdin.read().strip().splitlines()
    left, right = [], []

    for line in input_lines:
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    left.sort()
    # right.sort()
    frequency = Counter(right)

    print(sum(abs(a - b) for a, b in zip(left, right)))
    print(sum((a * frequency[a]) for a in left))


if __name__ == "__main__":
    main()
