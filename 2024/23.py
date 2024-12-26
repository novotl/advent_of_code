from collections import Counter, defaultdict
from copy import deepcopy
from functools import cache, cmp_to_key, reduce
from itertools import chain, combinations, count, product
from pprint import pprint
from sys import stdin
import re
from dataclasses import dataclass
from operator import add, mul, lt, gt, truediv
from typing import Iterable
from PIL import Image
import numpy as np
from tqdm import tqdm
from heapq import heappush, heappop


def part1():
    lines = iter(stdin.read().strip().splitlines())

    graph = defaultdict(list)
    nodes = set()
    for line in lines:
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)
        nodes.add(a)
        nodes.add(b)

    # print(nodes)
    # pprint(graph)

    target = 3
    res = set()

    for start in tqdm(nodes):
        visited = set()
        queue = [(start, 0, tuple())]

        while queue:
            curr, l, hist = queue.pop(0)
            visited.add(hist)

            if l == target and curr == start:
                res.add(hist)

            if l > target:
                break

            for neighbour in sorted(graph[curr]):
                if not all(h in graph[neighbour] for h in hist):
                    continue

                history = tuple(sorted([*hist, neighbour]))

                if history not in visited:
                    queue.append((neighbour, l + 1, history))

    # print(len(res))
    # print(res)

    final = 0
    for cycle in res:
        if any(x.startswith("t") for x in cycle):
            final += 1
    print(final)


def bors_kerbosch_v1(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    for v in P.union(set([])):
        bors_kerbosch_v1(
            R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C
        )
        P.remove(v)
        X.add(v)


def part2():
    lines = iter(stdin.read().strip().splitlines())

    graph = defaultdict(list)
    nodes = set()
    for line in lines:
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)
        nodes.add(a)
        nodes.add(b)
    
    res = []
    bors_kerbosch_v1(set(), nodes, set(), graph, res)
    print(",".join(sorted(max(res, key=len))))


    # print(",".join(sorted(best)))


if __name__ == "__main__":
    # part1()
    part2()
