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
    num_bits = i.bit_length()
    num_bytes = (num_bits + 7) // 8

    return i.to_bytes(
        length=num_bytes,
        byteorder=sys.byteorder,
        signed=False
    )
