#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from utils import int_to_bytes


class TransactionOutput:
    def __init__(self, amount: int, key: bytes):
        self._amount = amount
        self._key = key

    @property
    def bytes(self):
        return int_to_bytes(self._amount) + self._key
