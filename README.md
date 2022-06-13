# Welcome

This repository may in the future contain one or more Python modules to do 
quirky/interesting things.

Currently the only implemented thing is sleep sort, an exotic sorting
algorithm that is O(n) (yes, really!)

To use it:

```python
>>> from ñoqui.sleep_sort import sort  # Or async_sort!
>>> sort([3, 2, 1], how_fast=500)
[1, 2, 3]
```

For further documentation and insights, just look at the source code,
it's well commented and includes tests.
