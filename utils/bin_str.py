#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys


def bin_str(x: int, n: int = 32):
    """
    Converts an integer x into its binary representation as string, taking
    fitst n most significant bits.
    """
    s = "{:0128b}".format(x)

    if n < len(s):
        # Position of most significant bits is different
        # on big-endian and little-endian platforms
        if sys.byteorder == "little":
            return s[:n] + "..."
        elif sys.byteorder == "big":
            return s[len(s) - n:] + "..."

        raise SystemError("Unrecognized endianness: \"{:}\"".format(sys.byteorder))

    return s
