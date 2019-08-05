


import unittest
from unittest import TestCase
from itertools import *
from moreitertools import *
from random import choices
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




if __name__ == '__main__':
    unittest.main()
