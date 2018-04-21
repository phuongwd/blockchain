#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys


def int_to_bytes(i: int) -> bytes:
    """
    Re-interprets an integer as array of bytes. Endianness-independent.
    """
    return i.to_bytes(
        length=(i.bit_length() + 7) // 8,
        byteorder=sys.byteorder,
        signed=False
    )
