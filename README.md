
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
