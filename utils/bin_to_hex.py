#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import binascii


def bin_to_hex(binary: bytes, n: int = 32):
    s = binascii.hexlify(binary).decode("utf-8")
    if len(s) > n - 3:
        s = s[:n] + "..."
    return s
