#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class TransactionOutput:
    def __init__(self, amount: int, key: bytes):
        self._amount = amount
        self._key = key

    @property
    def bytes(self):
        return bytes([self._amount]) + self._key
