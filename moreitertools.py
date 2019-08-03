
from typing import *
from itertools import islice

# Type vars for parameter annotations
T_co = TypeVar('T', covariant=True)


# Helper methods
def _check_iterable(x):
    if not isinstance(x, Iterable):
        raise TypeError(f'{type(x).__name__} is not iterable')

def _check_default(args):
    if len(args) > 1:
        raise TypeError(f'Expected at most one varadic argument, got {len(args)}')

def _check_predicate(pred):
    if pred is not None and not callable(pred):
        raise TypeError(f'{type(x).__name__} is not callable')



def first(x: Iterable[T_co], *args) -> T_co:
    '''
    Takes an iterable as argument and retrieves the first element.
    Its equivalent to next(iter(x), *args)
    If x has no items, returns the default value if it is provided or raises ValueError exception otherwise.
    e.g:
    first([1,2,3]) -> 1
    first([]) -> ValueError
    first([], default=None) -> None
    '''
    _check_iterable(x)
    _check_default(args)

    try:
        return next(iter(x), *args)
    except StopIteration:
        raise ValueError('Iterable is empty')



def last(x: Iterable[T_co], *args) -> T_co:
    '''
    Takes an iterable as argument and retrieves the last element.
    Its equivalent to next(reversed(tuple(x)), *args)
    If x has no items, returns the default value if it is provided or raises ValueError exception otherwise.
    e.g:
    last([1,2,3]) -> 3
    last([]) -> ValueError
    last([], default=None) -> None

    Note: If the given iterable implements the method __reversed__, this function will
    be more efficient as it doesnt need to consume all the items from the iterable to get
    only the last one.
    '''
    _check_iterable(x)
    _check_default(args)

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

    Its equivalent to next(filter(pred, x), *args)
    In the case where none of the items satisfies the predicate, returns the default value if it is provided or
    raises ValueError exception otherwise.
    e.g:
    first_true([None, False, 0, 10]) -> 10
    first_true([1, 4, 9], pred=lambda x: x > 5) -> 9
    first_true([1, 4, 9], pred=lambda x: x > 9) -> ValueError
    first_true([1, 4, 9], None, pred=lambda x: x > 9) -> None
    '''
    _check_iterable(x)
    _check_default(args)
    _check_predicate(pred)

    try:
        return next(filter(pred, x), *args)
    except StopIteration:
        raise ValueError('No item satisfies the predicate')



def nth(x: Iterable[T_co], n: int, *args) -> T_co:
    '''
    Takes an iterable as argument and returns the item at the nth position.
    If the number of items in the iterable is less or equal than n, returns the default value if provided or raises ValueError exception otherwise.
    n can be a negative number. In that case, the result of this call its equivalent to nth(x, len(tuple(x))+n, *args)
    e.g:
    nth('hello', 1) -> 'e'
    nth('world', -2) -> 'l'
    nth([1,2,3], 100) -> ValueError
    nth([1,2,3], 100, -1) -> -1

    Note: If the given argument implements the Sequence interface,
    this method is more efficient as it will retrieve the nth item using __getitem__ method
    '''
    _check_iterable(x)
    _check_default(args)

    if not isinstance(n, int):
        raise TypeError('Second argument must be an integer')

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
    _check_iterable(x)
    return reversed(x if isinstance(x, Reversible) else tuple(x))
