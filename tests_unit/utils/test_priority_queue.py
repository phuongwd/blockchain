#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

from utils import PriorityQueue


class TestPriorityQueue(TestCase):
    def test_iteration_on_empty(self):
        q = PriorityQueue(items=[])
        assert [] == [i for i in q.items]

    def test_iteration_on_one(self):
        q = PriorityQueue(items=[3])
        assert [3] == [i for i in q.items]

    def test_iteration_on_multiple(self):
        q = PriorityQueue(items=[3, 2, 1, 0])
        assert [0, 1, 2, 3] == [i for i in q.items]

    def test_contains_on_empty(self):
        q = PriorityQueue()
        assert not q.contains(0)

    def test_contains_on_single(self):
        q = PriorityQueue(items=[7])
        assert q.contains(7)

    def test_contains_not_on_single(self):
        q = PriorityQueue(items=[7])
        assert not q.contains(1)

    def test_contains_on_multiple(self):
        q = PriorityQueue(items=[42, 7, 0, 25])
        assert q.contains(7)

    def test_contains_not_on_multipl(self):
        q = PriorityQueue(items=[42, 7, 0, 25])
        assert not q.contains(10)
