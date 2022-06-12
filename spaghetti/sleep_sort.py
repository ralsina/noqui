"""This module implements sleep sort.

Sleep sort is kinda related to spaghetti sort, in a way.

It's a O(n) sorting algorithm, although it's often described
as having O(n+max(v)) where max(v) is the largest element in
the unsorted array (that description is **wrong**).
"""

import asyncio
from fractions import Fraction
from collections import deque
from typing import Iterable, List


__all__ = ["async_sort", "sort"]


def sort(l: Iterable[int], how_fast: int = 1000) -> Iterable[int]:
    """
    Implement sort (only for integers).

    Arguments:

    * l            An Iterable of integers to be sorted
    * how_fast     Integer expressing how fast to sort. Larger is faster (default 1000)

    Caveats:

    * Lists that are too long (millions/billions of elements) may fail to sort
    * If you ask to sort too fast, results may be inaccurate

    >>> sort([3, 2, 1])
    [1, 2, 3]

    >>> import timeit
    >>> t1 = timeit.timeit(lambda: sort([1, 2, 3], how_fast=100), number=100)
    >>> t2 = timeit.timeit(lambda: sort([1, 2, 3], how_fast=1000), number=100)
    >>> t3 = timeit.timeit(lambda: sort([1, 2, 3], how_fast=10000), number=100)
    >>> t1 > t2 > t3  or (t1, t2, t3) # Larger is slower
    True

    >>> sort([])
    []

    >>> sort([1])
    [1]

    >>> sort([1, 1])
    [1, 1]
    """

    return asyncio.run(async_sort(l, how_fast))


async def async_sort(l: List[Fraction], how_fast: int = 1000) -> List[int]:
    """
    Async implementation of sleep sort.
    """

    if len(l) < 2 or len(set(l)) < 2:
        # Corner cases: empty lists, one element, only one repeated element
        return l

    norm_l = _normalize(l)
    d = deque()
    waiting = []
    loop = asyncio.get_running_loop()
    for i in norm_l:
        waiting.append(asyncio.create_task(_wait(i, d, how_fast)))

    await asyncio.gather(*waiting)
    sorted = [d.popleft() for _ in l]
    return _denormalize(l, sorted)


async def _wait(value: Fraction, d: deque, how_fast: int):
    await asyncio.sleep(value / how_fast)
    d.append(value)


def _normalize(l: Iterable[int]) -> List[Fraction]:
    """
    Normalize a list of integers.

    Transforms a list of integers into a list of fractions
    in the interval [0, 1]

    >>> _normalize([5, 6, 7])
    [Fraction(0, 1), Fraction(1, 2), Fraction(1, 1)]

    >>> _normalize([-5, 6, 7])
    [Fraction(0, 1), Fraction(11, 12), Fraction(1, 1)]
    """
    max_v = max(l)
    min_v = min(l)
    factor = Fraction(1, max_v - min_v)

    return [(i - min_v) * factor for i in l]


def _denormalize(original: Iterable[int], normalized: List[Fraction]) -> List[Fraction]:
    """Given two lists, the original and a normalized but disordered version of it,
    denormalize the second one to match the original.

    Therefore, the elements of the output will match the original list
    but the order will match the normalized list.

    >>> _denormalize([5, 6, 7], [Fraction(1, 1), Fraction(1, 2), Fraction(0, 1)])
    [7, 6, 5]

    >>> _denormalize([6, 7, -5], [Fraction(0, 1), Fraction(11, 12), Fraction(1, 1)])
    [-5, 6, 7]
    """
    max_v = max(original)
    min_v = min(original)
    factor = Fraction(1, max_v - min_v)

    return [int(i / factor + min_v) for i in normalized]
