#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from typing import Callable, List, Any


class MerkleTree:
    def __init__(
            self,
            leaves: List[Any],
            f_hash: Callable[[Any], Any],
            f_reduce: Callable[[Any, Any], Any] = lambda x, y: x + y
    ):
        """
        Implments "Merkle tree" data structure. Merkle tree is a variation of
        hash trees. It allows for inclusion tests (that is, checkin whether a
        given element is present) in log(N) time, given only the hash value
        of the element.

        See also: https://en.wikipedia.org/wiki/Merkle_tree

        :param leaves: list of values to be inserted into the tree
        :param f_hash: unary function that produces the hash of the input
        :param f_reduce: binary function that given two inputs, reduces them
            into one output. Default: addition operation ("+").
        """

        # Binary hash function first reduced the two inputs to one output and
        # then applies the hash function to that output
        self._f_reduce_hash = lambda x, y: f_hash(f_reduce(x, y))

        self._leaves = leaves
        self._root_hash = None
        self._dirty = True

    @staticmethod
    def pairs(a: List[Any]):
        """
        Converts  a list of values into a list of pairwise groups of
        neighbor elements. If the number of elements is odd, the result is
        as if the last element was duplicated (effectively making the number
        of elements even)

        Example: given a list [0, 1, 2, 3, 4] this function will output:
        [(0, 1), (2, 3), (4, 4)]

        :param a: list of values
        :return: list of pairs
        """
        pairs = list(zip(a[:-1:2], a[1::2]))

        if len(a) % 2 != 0:
            pairs.append((a[-1], a[-1]))

        return pairs

    def reduce_one_level(self, a: List[Any]):
        pairs = MerkleTree.pairs(a)
        return [self._f_reduce_hash(x, y) for x, y in pairs]

    def reduce(self):
        if self._leaves is None or len(self._leaves) == 0:
            return None

        hashes = self.reduce_one_level(self._leaves)
        while len(hashes) > 1:
            hashes = self.reduce_one_level(hashes)

        return hashes[0]

    def add_leaf(self, leaf: Any):
        self._leaves.append(leaf)
        self._dirty = True

    def add_leaves(self, leaves: List[Any]):
        if self._leaves is None:
            self._leaves = leaves
        else:
            self._leaves.extend(leaves)
        self._dirty = True

    @property
    def root_hash(self):
        if self._dirty:
            self._root_hash = self.reduce()
            self._dirty = False
        return self._root_hash

    @property
    def data(self):
        return self._leaves
