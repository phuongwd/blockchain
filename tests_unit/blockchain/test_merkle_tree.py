#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

from blockchain import MerkleTree


class TestMerkleTree(TestCase):
    """
    Implements a set of unit tests for Merkle Tree
    """

    def setUp(self):
        # In this test suite we use a hash function that surrounds input with
        # parentheses: (e.g. "abc" will be hashed to "(abc)"), and a reduction
        # function that concatenates inputs (e.g. "a" and "b" will become "ab").
        # Example: binary hash for inputs "a", "bc" will be "(a,bc)".
        self.mt = MerkleTree(
            leaves=[],
            f_hash=lambda x: "({:})".format(x),
            f_reduce=lambda x, y: "{:},{:}".format(x, y)
        )

    def test_merkle_tree_pairs_even(self):
        assert [(0, 1), (2, 3)] == MerkleTree.pairs([0, 1, 2, 3])

    def test_merkle_tree_pairs_odd(self):
        assert [(0, 1), (2, 3), (4, 4)] == MerkleTree.pairs([0, 1, 2, 3, 4])

    def test_merkle_tree_pairs_single(self):
        assert [(0, 0)] == MerkleTree.pairs([0])

    def test_merkle_tree_pairs_empty(self):
        assert [] == MerkleTree.pairs([])

    def test_merkle_tree_reduce_one_level_even(self):
        assert ["(0,1)", "(2,3)"] == self.mt.reduce_one_level([0, 1, 2, 3])

    def test_merkle_tree_reduce_one_level_odd(self):
        assert ["(0,1)", "(2,3)", "(4,4)"] == self.mt.reduce_one_level(
            [0, 1, 2, 3, 4])

    def test_merkle_tree_reduce_one_level_single(self):
        assert ["(0,0)"] == self.mt.reduce_one_level([0])

    def test_merkle_tree_reduce_one_level_empty(self):
        assert [] == self.mt.reduce_one_level([])

    def test_merkle_tree_reduce_even(self):
        self.mt.add_leaves([0, 1, 2, 3])
        assert "((0,1),(2,3))" == self.mt.reduce()

    def test_merkle_tree_reduce_odd(self):
        self.mt.add_leaves([0, 1, 2, 3, 4])
        assert "(((0,1),(2,3)),((4,4),(4,4)))" == self.mt.reduce()

    def test_merkle_tree_reduce_single(self):
        self.mt.add_leaves([0])
        assert "(0,0)" == self.mt.reduce()

    def test_merkle_tree_reduce_empty(self):
        assert None is self.mt.reduce()

    def test_merkle_tree_root_hash_even(self):
        self.mt.add_leaves([0, 1, 2, 3])
        assert "((0,1),(2,3))" == self.mt.root_hash

    def test_merkle_tree_root_hash_odd(self):
        self.mt.add_leaves([0, 1, 2, 3, 4])
        assert "(((0,1),(2,3)),((4,4),(4,4)))" == self.mt.root_hash

    def test_merkle_tree_root_hash_single(self):
        self.mt.add_leaves([0])
        assert "(0,0)" == self.mt.root_hash

    def test_merkle_tree_root_hash_empty(self):
        assert None is self.mt.root_hash
