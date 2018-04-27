#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class TransactionInput:
    def __init__(self, src_hash: bytes, src_idx: int, signature: bytes):
        self._src_hash = src_hash
        self._src_idx = src_idx
        self._signature = signature

    @property
    def bytes(self):
        return self._src_hash + bytes([self._src_idx]) + self._signature