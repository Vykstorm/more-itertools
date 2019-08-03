
from typing import *
#from itertools impor

T_co = TypeVar('T', covariant=True)

def first(x: Iterable[T_co]) -> T_co:
    '''
    Takes an iterable as argument and retrieves the first element.
    Its equivalent to next(iter(x))
    If x has no items, raises a ValueError exception
    '''
    if not isinstance(x, Iterable):
        raise TypeError('Argument must be an iterable')

    try:
        return next(iter(x))
    except StopIteration:
        raise ValueError('Iterable is empty')


def last(x: Iterable[T_co]) -> T_co:
    '''
    Takes an iterable as argument and retrieves the last element.
    Its equivalent to tuple(x)[-1]
    If x has no items, raises a ValueError exception

    Note: If the given iterable implements the method __reversed__, this function will
    be more efficient as it doesnt need to consume all the items from the iterable to get
    only the last one.
    '''
    if not isinstance(x, Iterable):
        raise TypeError('Argument must be an iterable')
    try:
        if isinstance(x, Reversible):
            return next(reversed(x))

        it = iter(x)
        item = next(it)
        try:
            while True:
                item = next(it)
        except StopIteration:
            pass
        return item
    except StopIteration:
        raise ValueError('Iterable is empty')


def reversediter(x: Iterable[T_co]) -> Iterator[T_co]:
    '''
    This method takes an iterable as argument and returns and iterator that
    retrieves its items in reversed order.
    Its equivalent to reversed(tuple(x))

    Note: If the given argument implements the method __reversed__, this function is more
    efficient, as it will return reversed(x) directly
    '''
    if not isinstance(x, Iterable):
        raise TypeError('Argument must be an iterable')
    return reversed(x if isinstance(x, Reversible) else tuple(x))
