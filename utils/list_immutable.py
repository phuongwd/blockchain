#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from typing import Iterable, TypeVar

T = TypeVar('T')


class ListImmutable:
    def __init__(self, items: Iterable[T]):
        self._set = tuple()
        self.set(items)

    def get(self):
        # returrns a copy
        return list(self._set)

    def set(self, items: Iterable[T]):
        # sets a copy
        self._set = tuple(items)
