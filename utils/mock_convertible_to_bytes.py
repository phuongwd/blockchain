#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class MockConvertibleToBytes:
    def __init__(self, b):
        self._bytes = b

    @property
    def bytes(self):
        return self._bytes
