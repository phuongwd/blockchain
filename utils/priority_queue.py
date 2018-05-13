#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from queue import Empty, PriorityQueue as BuiltinPriorityQueue
from threading import Lock
from typing import Iterable, Callable, TypeVar

T = TypeVar('T')


class _PriorityQueueItem:
    def __init__(
            self,
            item: T,
            less: Callable[[T, T], bool] = lambda x, y: x < y
    ):
        self._item = item
        self._less = less

    @property
    def item(self):
        return self._item

    def __lt__(self, other: object):
        return self._less(self._item, other._item)

    def __eq__(self, other):
        return self._item == other._item


class PriorityQueue:
    def __init__(
            self,
            f_priority: Callable[[T, T], bool] = lambda x, y: x < y,
            items: Iterable[T] = None
    ):
        self._f_priority = f_priority
        self._q = BuiltinPriorityQueue()
        self._lock = Lock()

        for item in (items or []):
            self.put(item)

    @property
    def items(self):
        with self._lock:
            return list([i.item for i in self._q.queue])

    def put(self, item: T):
        # Wrap the item into priority item with a custom comparison function
        with self._lock:
            self._q.put(_PriorityQueueItem(item, self._f_priority))

    def get(self):
        try:
            prio_item = self._q.get()

            # Unwrap the item
            return prio_item.item

        except Empty:
            return None

    def contains(self, item):
        items = self.items
        return item in items

    def is_empty(self):
        with self._lock:
            return len(self.items) > 0

    # def __getitem__(self, index):
    #     return self.items[index]
    #
    # def __len__(self):
    #     return len(self.items)
    #
    # def __iter__(self):
    #     self._i = 0
    #     return self
    #
    # def __next__(self):
    #     prio_items = self.items
    #     if self._i < len(self.items):
    #         prio_item = prio_items[self._i]
    #         self._i += 1
    #         return prio_item.item
    #     else:
    #         raise StopIteration
