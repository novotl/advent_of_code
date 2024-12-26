from sys import stdin
import re


def main():
    input_line = "".join(stdin.read().strip().splitlines())

    matches = re.findall(r"(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))", input_line.strip())

    res = 0
    coeff = 1

    for m in matches:
        # DO
        if m[3]:
            coeff = 1
        # DON'T
        elif m[4]:
            coeff = 0
        else:
            x, y = int(m[1]), int(m[2])
            res += coeff * x * y

    print(res)

    # print(sum((int(x) * int(y)) for x, y in matches))


if __name__ == "__main__":
    main()
