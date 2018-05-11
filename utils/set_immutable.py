#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from typing import Iterable, TypeVar

T = TypeVar('T')


class SetImmutable:
    def __init__(self, items: Iterable[T]):
        self._set = frozenset()
        self.set(items)

    def get(self):
        # returrns a copy
        return set(self._set)

    def set(self, items: Iterable[T]):
        # sets a copy
        self._set = frozenset(items)
