from typing import Callable, Iterable, TypeVar
from collections import defaultdict

K = TypeVar("K")
V = TypeVar("V")
U = TypeVar("U")


def identity(value: V) -> V:
    return value


def invert_dictionary(dictionary: dict[K, V], key: Callable[[V], U] = identity) -> dict[U, list[K]]:
    """
    Inverts a dictionary.

        >>> invert_dictionary({'a': 1, 'b': 2})
        {1: ['a'], 2: ['b']}

        >>> invert_dictionary({'a': 1, 'b': 1, 'c': 2})
        {1: ['a', 'b'], 2: ['c']}

    Supports mapping the new keys:

        >>> invert_dictionary({1: 'cat', 2: 'dog', 3: 'dog'}, key=lambda s: s[::-1])
        {'tac': [1], 'god': [2, 3]}

    Values must be hashable:

        >>> invert_dictionary({'a': [1, 2]})
        Traceback (most recent call last):
        ...
        TypeError: unhashable type: 'list'

        >>> invert_dictionary({'a': [1, 2]}, key=tuple)
        {(1, 2): ['a']}
    """
    inverted = defaultdict(list)
    for k, v in dictionary.items():
        inverted[key(v)].append(k)

    return dict(inverted)
