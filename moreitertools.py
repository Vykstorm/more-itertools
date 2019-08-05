
from typing import *
from itertools import islice, chain, filterfalse
from functools import wraps, partial
from collections import deque
from operator import truth


# Type vars for parameter annotations
T_co = TypeVar('T_co', covariant=True)


# Helper classes & methods
class checker:
    def __init__(self, unchecked):
        self.unchecked = unchecked

    def __call__(self, check):
        unchecked = self.unchecked

        @wraps(unchecked)
        def wrapper(*args, **kwargs):
            check(*args, **kwargs)
            return unchecked(*args, **kwargs)

        wrapper.unchecked = unchecked
        return wrapper


def _check_iterable(x, param=None):
    if not isinstance(x, Iterable):
        if param is None:
            raise TypeError(f'{type(x).__name__} is not iterable')
        raise TypeError(f'{param} must be an iterable, got {type(x).__name__}')

def _check_varadics(args, n=1):
    if len(args) > n:
        raise TypeError(f'Expected at most 1 varadic argument, got {len(args)}')

def _check_predicate(x, param=None):
    if x is None:
        return
    _check_callable(x, param)

def _check_callable(x, param=None):
    if not callable(x):
        if param is None:
            raise TypeError(f'{type(x).__name__} is not callable')
        raise TypeError(f'{param} must be a callable, got {type(x).__name__}')

def _check_integer(x, param=None):
    if not isinstance(x, int):
        if param is None:
            raise TypeError(f'{type(x).__name__} is not an integer')
        raise TypeError(f'{param} must be an integer, got {type(x).__name__}')

def _check_quantity(x, param=None):
    if not isinstance(x, int) or x < 0:
        if param is None:
            raise TypeError(f'{type(x).__name__} is not a positive integer')
        raise TypeError(f'{param} must be a positive integer, got {type(x).__name__ if not isinstance(x, int) else str(x)}')


# Recipes

def first(x: Iterable[T_co], *args) -> T_co:
    '''
    Takes an iterable as argument and retrieves the first element.
    Its roughly equivalent to next(iter(x), *args)
    If x has no items, returns the default value if present (provided in the varadic arguments)
    or raises ValueError exception otherwise.
    e.g:
    first([1,2,3]) -> 1
    first([]) -> ValueError
    first([], default=None) -> None
    '''
    try:
        return next(iter(x), *args)
    except StopIteration:
        raise ValueError('Iterable is empty')



def last(x: Iterable[T_co], *args) -> T_co:
    '''
    Takes an iterable as argument and retrieves the last element.
    Its roughly equivalent to next(reversed(tuple(x)), *args)
    If x has no items, returns the default value if provided (in the varadic arguments list)
    or raises a ValueError exception otherwise.
    e.g:
    last([1,2,3]) -> 3
    last([]) -> ValueError
    last([], default=None) -> None

    Note: If the given iterable implements the method __reversed__, this function will
    be more efficient as it doesnt need to consume all the items from the iterable to get
    only the last one.
    '''
    try:
        if isinstance(x, Reversible):
            return next(reversed(x), *args)

        it = iter(x)
        item = next(it)
        try:
            while True:
                item = next(it)
        except StopIteration:
            pass
        return item

    except StopIteration:
        if len(args) > 0:
            return args[0]
        raise ValueError('Iterable is empty')



def first_true(x: Iterable[T_co], *args, pred: Optional[Callable[[T_co], Any]]=None) -> T_co:
    '''
    Returns the first item in the given iterable such that the predicate is evaluated to True.
    If no predicate is specified, bool is used by default.

    Its roughly equivalent to next(filter(pred, x), *args)
    In the case where none of the items satisfies the predicate or the iterable is empty,
    returns the default value if provided (in the varadic arguments) or raises ValueError exception otherwise.
    e.g:
    first_true([None, False, 0, 10]) -> 10
    first_true([1, 4, 9], pred=lambda x: x > 5) -> 9
    first_true([1, 4, 9], pred=lambda x: x > 9) -> ValueError
    first_true([1, 4, 9], None, pred=lambda x: x > 9) -> None
    '''
    try:
        return next(filter(pred, x), *args)
    except StopIteration:
        raise ValueError('No item satisfies the predicate')



def first_false(x: Iterable[T_co], *args, pred: Optional[Callable[[T_co], Any]]=None) -> T_co:
    '''
    Its the counterpart of the function first_true: Returns the first item in the given iterable
    that make the predicate evaluate to False.
    Its roughly equivalent to next(filterfalse(pred, x), *args)
    In the case where all the items satisfies the predicate or the iterable is empty,
    returns the default value if provided (in the varadic arguments) or raises ValueError exception otherwise.
    e.g:
    first_false([1, 0, 2]) -> 0
    first_false([1, 2, 3]) -> Value error
    first_false([1, 2, 3], pred=lambda x: x < 2) -> 2
    first_false([1, 2, 3], None) -> None
    '''
    try:
        return next(filterfalse(pred, x), *args)
    except StopIteration:
        raise ValueError('All items satisfies the predicate')



def last_true(x: Iterable[T_co], *args, pred: Optional[Callable[[T_co], Any]]=None) -> T_co:
    '''
    Returns the last item in the given iterable such that the predicate is evaluated to True.
    If no predicate is specified, bool is used by default.

    Its roughly equivalent to next(filter(pred, reversed(tuple(x))), *args)
    In the case where none of the items satisfies the predicate or the iterable is empty,
    returns the default value if provided (in the varadic arguments) or raises ValueError exception otherwise.

    e.g:
    last_true([False, 1, 0, None]) -> 1
    last_true([1, 3, 5, 9], pred=lambda x: x > 3) -> 9
    last_true([False, 0]) -> ValueError
    last_true([False, 0], None) -> None
    '''
    return first_true.unchecked(reversediter(x), *args, pred=pred)



def last_false(x: Iterable[T_co], *args, pred: Optional[Callable[[T_co], Any]]=None) -> T_co:
    '''
    Its the counterpart of the function last_true: Returns the last item in the given iterable
    such that the predicate is evaluated to True.
    If no predicate is specified, bool is used by default.

    Its roughly equivalent to next(filterfalse(pred, reversed(tuple(x))), *args)
    In the case where all the items satisfies the predicate or the iterable is empty,
    returns the default value if provided (in the varadic arguments) or raises ValueError exception otherwise.

    e.g:
    last_false([1, 0, 2, False, 3]) -> False
    last_false([1, 2, 3]) -> ValueError
    last_false([4, 5, 6], pred=lambda x: x > 5) -> 5
    '''
    return first_false.unchecked(reversediter(x), *args, pred=pred)



def nth(x: Iterable[T_co], n: int, *args) -> T_co:
    '''
    Takes an iterable as argument and returns the item at the nth position.
    n can be a negative number. In that case, this call is transformed into nth(x, len(tuple(x))+n, *args)
    If the number of items in the iterable is less or equal than n, returns the default value if provided (in the varadic arguments list)
    or raises IndexError exception otherwise.

    e.g:
    nth('hello', 1) -> 'e'
    nth('world', -2) -> 'l'
    nth([1,2,3], 100) -> ValueError
    nth([1,2,3], 100, -1) -> -1

    Note: If the given argument implements the Sequence interface,
    this method is more efficient as it will retrieve the nth item using __getitem__ method
    '''
    try:
        if isinstance(x, Sized):
            l = len(x)
            if n < 0:
                n += l
            if n < 0 or n >= l:
                raise IndexError

            if isinstance(x, Sequence):
                return x[n]

            if isinstance(x, Reversible) and n >= l//2:
                n, x = l-n-1, reversed(x)

        elif n < 0:
            return tuple(x)[n]

        try:
            return next(islice(x, n, None))
        except StopIteration:
            raise IndexError

    except IndexError:
        if len(args) > 0:
            return args[0]
        raise IndexError('index out of range')



def reversediter(x: Iterable[T_co]) -> Iterator[T_co]:
    '''
    This method takes an iterable as argument and returns and iterator that
    retrieves its items in reversed order.
    Its equivalent to reversed(tuple(x))

    Note: If the given argument implements the method __reversed__, this function is more
    efficient, as it will return reversed(x) directly
    '''
    return reversed(x if isinstance(x, Reversible) else tuple(x))



def head(x: Iterable[T_co], n: int) -> Iterator[T_co]:
    '''
    Creates an iterator that retrieves the first n items from the given iterable.
    Its equivalent to islice(x, n) if n is greater or equal than zero.
    Otherwise, its equivalent to tail(x, -n)

    e.g:
    head(range(0, 50), 3) -> 1, 2, 3
    head(range(0, 50, 2), -2) -> 46, 48
    '''
    if n >= 0:
        return islice(x, n)

    n = -n
    d = deque(maxlen=n)

    if isinstance(x, Reversible):
        d.extendleft(islice(reversed(x), n))
    else:
        d.extend(x)
    return iter(d)



def tail(x: Iterable[T_co], n: int) -> Iterator[T_co]:
    '''
    Creates an iterator that retrieves the last n items from the given iterable.
    Its equivalent to iter(tuple(x)[-n:]) if n is greater than zero. Otherwise, its the same as head(x, -n)

    e.g:
    ''.join(tail('hello world', 5)) -> 'world'
    tail(range(20), 3) -> 17, 18, 19
    '''
    return head.unchecked(x, -n)



def quantify(x: Iterable[T_co], pred: Optional[Callable[[T_co], Any]]=None) -> int:
    '''
    Count the number of times that the predicate is evaluated to True for the items
    in the given iterable. If no predicate is specified, bool is used
    Equivalent to len(tuple(filter(pred, x)))
    e.g:
    quantify([1, 4, 5, 9, 10], lambda x: x % 2 == 0) -> 2
    quantify('Hello World', str.isupper) -> 2
    '''
    if pred is None:
        pred = truth

    c = 0
    for item in x:
        if pred(item):
            c += 1
    return c



def ncycles(x: Iterable[T_co], n: int) -> Iterator[T_co]:
    '''
    Returns a sequence with all the elements given in the iterable n times.
    Equivalent to chain.from_iterable(repeat(tuple(x), n))

    e.g:
    ''.join(ncycles('abc', 2)) -> 'abcabc'
    ncycles(range(0, 3), 2) -> 0, 1, 2, 0, 1, 2

    Note: For n > 1, this method is more memory efficient if the given input iterable is
    a collection (implements the Collection interface) as it doesnt need to store the items temporally.
    '''
    if n == 0:
        return
    if n == 1:
        yield from iter(x)
        return

    if not isinstance(x, Collection):
        x = tuple(x)

    for k in range(n):
        yield from iter(x)



def repeatfunc(f, n: int, *args, **kwargs) -> Iterator:
    '''
    Calls the given function repeteadly n times with the given positional and keyword arguments.
    Equivalent to map(lambda f: f(*args, **kwargs), repeat(f, n))

    e.g:
    repeatfunc(random.randrange, 5, 0, 10) -> 7, 3, 9, 1, 5
    '''
    if n == 0:
        return

    f = partial(f, *args, **kwargs)
    for k in range(n):
        yield f()


# Recipe input argument checkers

@checker(first)
def first(x, *args):
    _check_iterable(x)
    _check_varadics(args)


@checker(last)
def last(x, *args):
    _check_iterable(x)
    _check_varadics(args)


@checker(first_true)
def first_true(x, *args, pred=None):
    _check_iterable(x)
    _check_varadics(args)
    _check_predicate(pred)


@checker(first_false)
def first_false(x, *args, pred=None):
    _check_iterable(x)
    _check_varadics(args)
    _check_predicate(pred)


@checker(last_true)
def last_true(x, *args, pred=None):
    _check_iterable(x)
    _check_varadics(args)
    _check_predicate(pred)


@checker(last_false)
def last_false(x, *args, pred=None):
    _check_iterable(x)
    _check_varadics(args)
    _check_predicate(pred)


@checker(nth)
def nth(x, n, *args):
    _check_iterable(x)
    _check_varadics(args)
    _check_integer(n, 'n')


@checker(reversediter)
def reversediter(x):
    _check_iterable(x)


@checker(head)
def head(x, n):
    _check_iterable(x)
    _check_integer(n, 'n')


@checker(tail)
def tail(x, n):
    _check_iterable(x)
    _check_integer(n, 'n')


@checker(quantify)
def quantify(x, pred=None):
    _check_iterable(x)
    _check_predicate(pred)


@checker(ncycles)
def ncycles(x, n):
    _check_iterable(x)
    _check_quantity(n, 'n')


@checker(repeatfunc)
def repeatfunc(func, n):
    _check_callable(func)
    _check_quantity(n, 'n')
