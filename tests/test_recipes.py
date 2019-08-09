
'''
Tests for all the recipes defined in this library.
To run them, go the root directory and execute the next cmd bash lines:
export PYTHONPATH=$(pwd)
python tests/tests_recipes.py
'''


import unittest
from unittest import TestCase
from itertools import *
from functools import reduce, partial


from src import *
from random import choices, sample
from operator import *


class TestRecipes(TestCase):
    '''
    Tests for functions defined in the script moreitertools
    '''
    def setUp(self):
        super().setUp()

        # Random values that are not iterable
        self.non_iterables = tuple(chain(
            (None, False, True),
            range(0, 10),
            map(float, range(0, 10)),
            (int, str, float, complex)
        ))

        # Empty iterable objects (not iterators)
        self.empty_iterables = (
            [], (), {}, set(), frozenset(), '', b''
        )

        # Iterables with different number of elements (at least 1)
        self.filled_iterables = tuple(chain(
            [tuple(range(0, k)) for k in range(1, 6)],
            [list(map(chr, range(ord('a'), ord('a')+k))) for k in range(1, 6)],
            [tuple(repeat(value, 6)) for value in (False, True, None, 0, 1)]
        ))

        # Callable objects that returns always 1 output and has 1 input (ofany kind)
        self.predicates = tuple(chain(
            (lambda x: False, lambda x: True, lambda x: None),
            (not_, bool),
            (lambda x: isinstance(x, int) and x > 1,)
        ))

        # Iterables of any kind
        self.iterables = self.empty_iterables + self.filled_iterables

        # Random variables of any kind
        self.values = self.non_iterables + self.iterables + self.predicates

        # Non callable objects
        self.non_callables = tuple(filterfalse(callable, self.values))



    def test_first(self):
        # first(X) raises ValueError and first(X, default) == default if len(tuple(X)) == 0
        for X in self.empty_iterables:
            self.assertRaises(ValueError, first, X)
            for default in self.values:
                self.assertIs(first(X, default), default)

        # first(X) == tuple(X)[0] if len(tuple(X)) > 0
        for X in self.filled_iterables:
            self.assertIs(first(X), next(iter(tuple(X))))


    def test_last(self):
        # last(X) raises ValueError and last(X, default) == default if len(tuple(X)) == 0
        for X in self.empty_iterables:
            self.assertRaises(ValueError, last, X)
            for default in self.values:
                self.assertIs(last(X, default), default)

        # last(X) == tuple(X)[-1] if len(tuple(X)) > 0
        for X in self.filled_iterables:
            self.assertIs(last(X), next(reversed(tuple(X))))



    def test_first_true(self):
        # if X is an empty iterable, first_true(X, *args) behaves like first(X, *args)
        for X in self.empty_iterables:
            self.assertRaises(ValueError, first_true, X)
            for default in self.values:
                self.assertIs(first_true(X, default), default)

        # first_true(X, pred=pred) == y where y == next(filter(pred, X)) for a non empty iterable X
        # such that any(map(pred, X)) == True, otherwise, it raises ValueError
        # Also, if first_true(X, pred=pred) raises ValueError -> first_true(X, default, pred=pred) == default
        for X, pred in product(self.filled_iterables, self.predicates):
            if not any(map(pred, X)):
                self.assertRaises(ValueError, first_true, X, pred=pred)
                for default in self.values:
                    self.assertIs(first_true(X, default, pred=pred), default)
            else:
                self.assertIs(first_true(X, pred=pred), next(filter(pred, X)))


        # first_true(X, *args) behaves the same as first_true(X, *args, pred=bool)
        for X in self.filled_iterables:
            if not any(map(bool, X)):
                self.assertRaises(ValueError, first_true, X)
                for default in self.values:
                    self.assertIs(first_true(X, default), default)
            else:
                self.assertIs(first_true(X), first_true(X, pred=bool))



    def test_last_true(self):
        # if X is an empty iterable, last_true(X, *args) behaves like last(X, *args)
        for X in self.empty_iterables:
            self.assertRaises(ValueError, last_true, X)
            for default in self.values:
                self.assertIs(last_true(X, default), default)

        # last_true(X, pred=pred) == y where y == next(filter(pred, reversed(tuple(X)))) for a non empty iterable X
        # such that any(map(pred, X)) == True, otherwise, it raises ValueError
        # Also, if last_true(X, pred=pred) raises ValueError -> last_true(X, default, pred=pred) == default
        for X, pred in product(self.filled_iterables, self.predicates):
            if not any(map(pred, X)):
                self.assertRaises(ValueError, last_true, X, pred=pred)
                for default in self.values:
                    self.assertIs(last_true(X, default, pred=pred), default)
            else:
                self.assertIs(last_true(X, pred=pred), next(filter(pred, reversed(tuple(X)))))

        # last_true(X, *args) behaves the same as last_true(X, *args, pred=bool)
        for X in self.filled_iterables:
            if not any(map(bool, X)):
                self.assertRaises(ValueError, last_true, X)
                for default in self.values:
                    self.assertIs(last_true(X, default), default)
            else:
                self.assertIs(last_true(X), last_true(X, pred=bool))



    def test_first_false(self):
        # first_false(X, *args, pred=pred) behaves like first_true(X, *args, pred=lambda x: not pred(x))
        for X in self.empty_iterables:
            self.assertRaises(ValueError, first_false, X)
            for default in self.values:
                self.assertIs(first_false(X, default), default)

        for X, pred in product(self.filled_iterables, self.predicates):
            if all(map(pred, X)):
                self.assertRaises(ValueError, first_false, X, pred=pred)
                for default in self.values:
                    self.assertIs(first_false(X, default, pred=pred), default)
            else:
                self.assertIs(first_false(X, pred=pred), first_true(X, pred=lambda x: not pred(x)))

        # first_false(X, *args) behaves like first_false(X, *args, pred=bool)
        for X in self.filled_iterables:
            if all(map(bool, X)):
                self.assertRaises(ValueError, first_false, X)
                for default in self.values:
                    self.assertIs(first_false(X, default), default)
            else:
                self.assertIs(first_false(X), first_false(X, pred=bool))


    def test_last_false(self):
        # last_false(X, *args, pred=pred) behaves like last_true(X, *args, pred=lambda x: not pred(x))
        for X in self.empty_iterables:
            self.assertRaises(ValueError, last_false, X)
            for default in self.values:
                self.assertIs(last_false(X, default), default)

        for X, pred in product(self.filled_iterables, self.predicates):
            if all(map(pred, X)):
                self.assertRaises(ValueError, last_false, X, pred=pred)
                for default in self.values:
                    self.assertIs(last_false(X, default, pred=pred), default)
            else:
                self.assertIs(last_false(X, pred=pred), last_true(X, pred=lambda x: not pred(x)))

        # last_false(X, *args) behaves like last_false(X, *args, pred=bool)
        for X in self.filled_iterables:
            if all(map(bool, X)):
                self.assertRaises(ValueError, last_false, X)
                for default in self.values:
                    self.assertIs(last_false(X, default), default)
            else:
                self.assertIs(last_false(X), last_false(X, pred=bool))



    def test_nth(self):
        # nth(X, k) raises IndexError and nth(X, k, default) == default if X is an empty iterable
        # and k an integer >= 0
        for X, k in product(self.empty_iterables, range(0, 4)):
            self.assertRaises(IndexError, nth, X, k)
            for default in self.values:
                self.assertIs(nth(X, k, default), default)

        # nth(X, k) == tuple(X)[k] for 0 <= k < len(tuple(X)) and for any non empty iterable X
        for X in self.filled_iterables:
            for k in range(len(tuple(X))):
                self.assertIs(nth(X, k), tuple(X)[k])

        # nth(X, -k) == nth(X, len(tuple(X))-k) for 0 < k <= len(tuple(X)) and for any non empty iterable X
        for X in self.filled_iterables:
            for k in range(1, len(tuple(X))+1):
                self.assertIs(nth(X, -k), nth(X, len(tuple(X))-k))

        # nth(X, k) raises IndexError and nth(X, k, default) is default
        # if k >= len(tuple(X)) or k < -len(tuple(X)) and X is not an empty iterable
        for X in self.filled_iterables:
            n = len(tuple(X))
            for k in chain(map(neg, range(n+1, n+4)), range(n, n+4)):
                self.assertRaises(IndexError, nth, X, k)
                for default in self.values:
                    self.assertIs(nth(X, k, default), default)



    def test_reversediter(self):
        # tuple(reversediter(X)) == tuple(reversed(tuple(X))) for any iterable X
        for X in self.iterables:
            self.assertEqual(tuple(reversediter(X)), tuple(reversed(tuple(X))))



    def test_head(self):
        # tuple(head(X, n)) == tuple(X)[:n] with n >= 0 for any iterable X
        for X, n in zip(self.iterables, range(0, 6)):
            self.assertTrue(all(starmap(is_, zip(head(X, n), islice(X, n)))))

        # tuple(head(X, n)) == tuple(tail(X, -n)) with n < 0 for any iterable X
        for X, n in zip(self.iterables, map(neg, range(1, 6))):
            self.assertTrue(all(starmap(is_, zip(head(X, n), tail(X, -n)))))



    def test_tail(self):
        # tuple(tail(X, n)) == tuple(X)[-n:] with n >= 0 for any iterable X
        for X, n in zip(self.iterables, range(0, 6)):
            self.assertTrue(all(starmap(is_, zip(tail(X, n), tuple(X)[-n:]))))

        # tuple(tail(X, n)) == tuple(head(X, -n)) with n < 0 for any iterable X
        for X, n in zip(self.iterables, map(neg, range(1, 6))):
            self.assertTrue(all(starmap(is_, zip(tail(X, n), head(X, -n)))))



    def test_quantify(self):
        # quantify(X, pred) == len(tuple(filter(pred, X))) for any iterable X and a predicate pred
        for X, pred in product(self.iterables, self.predicates):
            self.assertEqual(quantify(X, pred), len(tuple(filter(pred, X))))

        # quantify(X) == quantify(X, bool) for any iterable X
        for X in self.iterables:
            self.assertEqual(quantify(X), quantify(X, bool))



    def test_ncycles(self):
        # len(tuple(ncycles(X, 0))) == 0 for any iterable X
        for X in chain(self.iterables, map(iter, self.iterables)):
            self.assertEqual(len(tuple(ncycles(X, 0))), 0)

        # tuple(ncycles(X, n)) == tuple(chain.from_iterable(repeat(tuple(x), n)))
        # for any iterable X and n > 0
        for X, n in product(chain(self.iterables, map(iter, self.iterables)), range(1, 4)):
            self.assertTrue(all(starmap(is_, zip(
                ncycles(X, n),
                chain.from_iterable(repeat(tuple(X), n))
            ))))



    def test_repeatfunc(self):
        # tuple(repeatfunc(f, n, *args, **kwargs)) == tuple(map(lambda f: f(*args, **kwargs), repeat(f, n)))
        k = 0
        def foo():
            nonlocal k
            prev, k = k, k+1
            return prev

        def bar(x):
            nonlocal k
            prev, k = k, k+x
            return prev

        for n in range(0, 10):
            self.assertEqual(tuple(repeatfunc(foo, n)), tuple(range(0, n)))
            k = 0
            for x in range(1, 4):
                self.assertEqual(tuple(repeatfunc(bar, n, x)), tuple(islice(count(0, x), n)))
                k = 0
                self.assertEqual(tuple(repeatfunc(bar, n, x=x)), tuple(islice(count(0, x), n)))
                k = 0

        # TODO n==None


    def test_unique_everseen(self):
        # len(tuple(unique_everseen(X))) == 0 if X is an empty iterable
        for X in self.empty_iterables:
            self.assertEqual(len(tuple(unique_everseen(X))), 0)

        # If X is an iterable where all items are hashable...
        for X in self.filled_iterables:
            try:
                X = frozenset(X)
            except TypeError:
                # If X contains non hashable items, unique_everseen(X) raises TypeError
                self.assertRaises(TypeError, unique_everseen, X)
                continue
            # set(unique_everseen(X)) == set(X)
            self.assertEqual(X, frozenset(unique_everseen(X)))

            # tuple(map(tuple(X).index, unique_everseen(X))) is a sorted array in ascendent order
            indices = tuple(map(tuple(X).index, unique_everseen(X)))
            self.assertEqual(indices, tuple(sorted(indices)))



    def test_unique_justseen(self):
        # len(tuple(unique_justseen(X))) == 0 if X is an empty iterable
        for X in self.empty_iterables:
            self.assertEqual(len(tuple(unique_justseen(X))), 0)

        # If X is an iterable where all items are hashable...
        for X in self.filled_iterables:
            try:
                X = frozenset(X)
            except TypeError:
                # If X contains non hashable items, unique_justseen(X) raises TypeError
                self.assertRaises(TypeError, unique_justseen, X)
                continue

            # There is no consecutive repeated elements in unique_justseen(X)
            self.assertTrue(all(starmap(lambda k, g: len(tuple(g)) == 1, groupby(unique_justseen(X)))))

            # set(unique_justseen(X)) <= set(X)
            self.assertLessEqual(frozenset(unique_justseen(X)), frozenset(X))

            # tuple(map(tuple(X).index, unique_everseen(unique_justseen(X)))) is a sorted array in ascendent order
            indices = tuple(map(tuple(X).index, unique_everseen(unique_justseen(X))))
            self.assertEqual(indices, tuple(sorted(indices)))



    def test_roundrobin(self):
        # rounbrobin() returns an empty iterator
        self.assertEqual(len(tuple(roundrobin())), 0)

        # roundrobin(X) for any iterable X returns iter(X)
        for X in self.iterables:
            self.assertTrue(all(starmap(is_, zip(tuple(X), tuple(roundrobin(X))))))

        # len(tuple(roundrobin(x1, x2, ..., xn))) == len(tuple(chain(x1, x2, ..., xn)))
        for k in range(1, 10):
            args = sample(self.iterables, k)
            self.assertEqual(reduce(add, map(len, args)), len(tuple(roundrobin(*args))))


        # tuple(roundrobin(x1, x2, ..., xn)) returns elements inside tuple(chain(x1, x2, ..., xn))
        for k in range(1, 10):
            args = sample(self.iterables, k)
            items = tuple(chain.from_iterable(args))
            self.assertTrue(all(map(items.__contains__, roundrobin(*args))))


        # roundrobin([0], [1, 4], [2, 5, 7], [3, 6, 8, 9]) -> range(0, 10)
        self.assertEqual(tuple(roundrobin([0], [1, 4], [2, 5, 7], [3, 6, 8, 9])), tuple(range(10)))

        # roundrobin([0, 4, 7, 9], [1, 5, 8], [2, 6], [3]) -> range(0, 10)
        self.assertEqual(tuple(roundrobin([0, 4, 7, 9], [1, 5, 8], [2, 6], [3])), tuple(range(10)))



    def test_length(self):
        # length(X) == len(tuple(X)) for any iterable X
        for X in self.iterables:
            self.assertEqual(length(X), len(tuple(X)))



    def test_prepend(self):
        for X, y in product(self.iterables, sample(self.values, 10)):
            # first(prepend(y, X)) == y for any iterable X
            self.assertIs(first(prepend(y, X)), y)

            # tuple(prepend(y, X))[1:] == tuple(X) for any iterable X
            self.assertTrue(all(starmap(is_, zip(islice(prepend(y, X), 1, None), X))))



    def test_append(self):
        for X, y in product(self.iterables, sample(self.values, 10)):
            # last(append(X, y)) == y for any iterable X
            self.assertIs(last(append(X, y)), y)

            # tuple(append(y, X))[:-1] == tuple(X) for any iterable X
            self.assertTrue(all(starmap(is_, zip(tuple(append(X, y))[:-1] , X))))



    def test_partition(self):
        for X, pred in product(self.iterables, self.predicates):
            # tuple(partition(pred, X)[0]) == tuple(filter(pred, X))
            self.assertTrue(all(starmap(is_, zip(partition(pred, X)[0], filter(pred, X)))))

            # tuple(partition(pred, X)[1]) == tuple(filterfalse(pred, X))
            self.assertTrue(all(starmap(is_, zip(partition(pred, X)[1], filterfalse(pred, X)))))



    def test_pairwise(self):
        for n in range(0, 10):
            # tuple(map(itemgetter(0), pairwise(range(n)))) == tuple(range(0, n-1))
            self.assertEqual(tuple(map(itemgetter(0), pairwise(range(n)))), tuple(range(0, n-1)))

            # tuple(map(itemgetter(1), pairwise(range(n)))) == tuple(range(1, n))
            self.assertEqual(tuple(map(itemgetter(1), pairwise(range(n)))), tuple(range(1, n)))



    def test_debugiter(self):
        # tuple(debugiter(X)) == tuple(iter(X))
        for X in self.iterables:
            self.assertTrue(all(starmap(is_, zip(tuple(X), tuple(debugiter(X))))))

        # str(debugiter(repeat(k))) does halt, but tuple(debugiter(repeat(k))) runs forever
        str(debugiter(repeat(0)))
        repr(debugiter(repeat(0)))





if __name__ == '__main__':
    unittest.main()
