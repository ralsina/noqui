"""This module implements sleep sort.

Sleep sort is kinda related to spaghetti sort, in a way.

It's a O(n) sorting algorithm, although it's often described
as having O(n+max(v)) where max(v) is the largest element in
the unsorted array (that description is **wrong**).
"""

import asyncio
from fractions import Fraction
from collections import deque
from typing import Iterable


async def _wait(value, d: deque):
    await asyncio.sleep(value / 1000)
    d.append(value)


async def async_sort(l: List[fraction]) -> List[int]:
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

    return asyncio.run(async_sort(l))
