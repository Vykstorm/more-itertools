
# Introduction

This is as an "extension" of the python itertools builtin library. <br/>
It defines a list of additional utility functions for efficient iteration (some of them are defined also in the "recipes" section of the itertools documentation page)

# Prerequisites & installation

This library is written in Python >= 3.5 and dont have any external dependencies

Install it via ```setup.py``` script

```bash
git clone https://github.com/Vykstorm/more-itertools.git
cd more-itertools
python setup.py install
```

# Examples

```python
from itertools import *
from moreitertools import *
from random import randrange
from operator import lt

# Find the first number greater than zero
first_true([-1, 2, 0, -3, 4], pred=lambda x: x > 0) # 2

# Count the amount of non zero elements
quantify([0, 10, 2, 0, 3, 1]) # 4

# Repeat a sequence 2 times
ncycles(range(0, 3), 2) # 0, 1, 2, 0, 1, 2

# Prepend and element to a sequence
prepend(0, range(10, 13)) # 0, 10, 11, 12

# Get a iterator that returns the items in a string
# without duplicates and preserving the order in which they appear
unique_everseen('BCADABCE') # 'B','C','A','D','E'

# Execute a function n times
repeatfunc(randrange, 4, start=0, stop=10) # 7, 0, 5, 6

# Search the last item in a sequence higher than the previous one
X = [4, 0, 0, -1, 4, 3, 5, 1]
last_true(starmap(lambda x, y: y if y > x else 0, pairwise(X))) # 5
```
There is additionaly a useful tool called ```debugiter``` that will help you debugging your code when working with complex iterators:
```python
from moreitertools import *

# Returns even numbers multiplied by 2 and odd multiplied by 3
it = roundrobin(
    map(lambda x: x * 2, range(0, 100, 2)),
    map(lambda x: x * 3, range(1, 100, 2))
)
print(debugiter(it))
```
The output will be:
```
0, 3, 4, 9, 8, 15, 12, 21, 16, 27, ..., 285, 192, 291, 196, 297  (100 items in total)
```

 debugiter will show part of the content and the number of items inside the iterator

Also you can interactively debug the iterator while iterating over it:

```python
it = debugiter(range(0, 60, 3))
print(it)
print('Next item is: ', next(it))
print(it)
print('Next item is: ', next(it))
print(it)

```
Output:
```
0, 3, 6, 9, 12, 15, 18, 21, 24, 27, ..., 45, 48, 51, 54, 57  (20 items in total)
Next item is 0
3, 6, 9, 12, 15, 18, 21, 24, 27, 30, ..., 45, 48, 51, 54, 57  (19 items in total)
Next item is 3
6, 9, 12, 15, 18, 21, 24, 27, 30, 33, ..., 45, 48, 51, 54, 57  (18 items in total)

```



# Documentation

To list all avaliable functions in this module, you can
execute the next:
```bash
python -c "import moreitertools; print(dir(moreitertools))"
```

Issue the command ```help``` or access the docstrings of the functions to get usage information:

```python
from moreitertools import *
help(first_true)
print(pairwise.__doc__)
```
