from collections import Counter, defaultdict
from copy import deepcopy
from functools import cache, cmp_to_key, reduce
from itertools import chain, combinations, count, product
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt, truediv, xor, and_, or_
from typing import Iterable
from PIL import Image
import numpy as np
from tqdm import tqdm
from heapq import heappush, heappop

OPS = {"AND": and_, "OR": or_, "XOR": xor}


def propagate(gates, wires):
    wires = deepcopy(wires)

    while True:
        found = False
        for (op, first, second), res in gates.items():
            if first in wires and second in wires and not all(r in wires for r in res):
                for r in res:
                    wires[r] = op(wires[first], wires[second])
                found = True
        if not found:
            break

    res = list(sorted((x for x in wires.items() if x[0].startswith("z")), reverse=True))
    return int("".join(str(int(x)) for _, x in res), base=2)


def compare(actual, expected):
    wrong_bits = []
    actual = reversed(bin(actual)[2:])
    expected = reversed(bin(expected)[2:])
    for bit, (a, e) in enumerate(zip(actual, expected)):
        if a != e:
            wrong_bits.append(bit)

    return wrong_bits


def print_graphviz(gates):
    print("digraph G {")
    print("subgraph x {")
    for i in range(45):
        print(f"\tx{i:02}")
    print("}")

    print("subgraph y {")
    for i in range(45):
        print(f"\ty{i:02}")
    print("}")

    print("subgraph z {")
    for i in range(46):
        print(f"\tz{i:02}")
    print("}")

    for (op, first, second), res in gates.items():
        colors = {"or_": "red", "xor": "green", "and_": "blue"}
        for r in res:
            print(f"\t{first} -> {r} [color={colors[op.__name__]}]")
            print(f"\t{second} -> {r} [color={colors[op.__name__]}]")
    print("}")


def print_mermaid(gates):
    print("flowchart TD")
    print(f"\tsubgraph x ")
    for i in range(45):
        print(f"\t\tx{i:02}")
    print(f"\tend")

    print(f"\tsubgraph y ")
    for i in range(45):
        print(f"\t\ty{i:02}")
    print(f"\tend")

    print(f"\tsubgraph z ")
    for i in range(46):
        print(f"\t\tz{i:02}")
    print(f"\tend")

    link_id = 0
    for (op, first, second), res in gates.items():
        colors = {"or_": "red", "xor": "green", "and_": "blue"}
        for r in res:
            print(f"\t{first} -- {op.__name__} --> {r}")
            print(f"\t{second} -- {op.__name__} --> {r}")
            print(f"\tlinkStyle {link_id} stroke:{colors[op.__name__]}")
            print(f"\tlinkStyle {link_id +1 } stroke:{colors[op.__name__]}")
            link_id += 2


def main():
    lines = iter(stdin.read().strip().splitlines())

    wires: dict[str, bool] = {}
    gates = defaultdict(set)

    for line in lines:
        if not line:
            break

        wire, value = line.split(":")
        wires[wire] = bool(int(value))

    for line in lines:
        match = re.match(r"(\w{3}) (XOR|OR|AND) (\w{3}) -> (\w{3})", line)
        if match:
            groups = match.groups()
            g = (OPS[groups[1]], groups[0], groups[2])
            gates[g].add(groups[3])

    res = propagate(gates, wires)

    in_x_bits = list(
        sorted((x for x in wires.items() if x[0].startswith("x")), reverse=True)
    )
    in_y_bits = list(
        sorted((x for x in wires.items() if x[0].startswith("y")), reverse=True)
    )
    int_x = int("".join(str(int(x)) for _, x in in_x_bits), base=2)
    int_y = int("".join(str(int(x)) for _, x in in_y_bits), base=2)
    expected = int_x + int_y

    # print(compare(res, expected))

    # print_graphviz(gates)
    print_mermaid(gates)

    # print(
    #     ",".join(
    #         sorted(
    #             [
    #                 "z23",
    #                 "qqp",
    #                 "z16",
    #                 "pbv",
    #                 "z36",
    #                 "fbq",
    #                 "qnw",
    #                 "qff",
    #             ]
    #         )
    #     )
    # )


if __name__ == "__main__":
    main()

# pair 1
# wdr OR jcd -> z23
# cts XOR bcd -> qqp


# pair 2
# x16 AND y16 -> z16
# dfn XOR qcr -> pbv

# pair 3
# jdd AND rbm -> z36
# jdd XOR rbm -> fbq

# pair 4
# x11 AND y11 -> qnw
# x11 XOR y11 -> qff
