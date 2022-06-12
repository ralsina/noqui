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


async def _wait(value, d: deque):
    await asyncio.sleep(value / 1000)
    d.append(value)


def _normalize(l: Iterable[int]) -> List[Fraction]:
    max_v = max(l)
    min_v = min(l)
    factor = Fraction(1, max_v - min_v)

    return [(i - min_v) * factor for i in l]


def _denormalize(original: Iterable[int], normalized: List[Fraction]) -> List[Fraction]:
    max_v = max(original)
    min_v = min(original)
    factor = Fraction(1, max_v - min_v)

    return [int(i / factor + min_v) for i in normalized]


async def async_sort(l: List[Fraction]) -> List[int]:
    """
    Async implementation of sleep sort.
    """

    d = deque()
    waiting = []
    loop = asyncio.get_running_loop()
    for i in l:
        waiting.append(asyncio.create_task(_wait(i, d)))

    await asyncio.gather(*waiting)
    return [d.popleft() for _ in l]


def sort(l: Iterable[int]) -> Iterable[int]:
    """
    Implement sleep sort (only for integers).

    >>> sort([3, 2, 1])
    [1, 2, 3]

    """

    norm_l = _normalize(l)

    return _denormalize(l, asyncio.run(async_sort(norm_l)))
