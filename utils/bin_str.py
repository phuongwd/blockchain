#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys


def bin_str(x: int, pad: int, n: int = 32):
    """
    Converts an integer `x` into its binary representation as string,
    zero-padding to length `pad` and taking fitst `n` most significant bits
    (truncating the rest with ellipsis).
    """
    s = "{x:0{pad}b}".format(pad=pad, x=x)

    if n < len(s):
        # Position of most significant bits is different
        # on big-endian and little-endian platforms
        if sys.byteorder == "little":
            return s[:n] + "..."
        elif sys.byteorder == "big":
            return s[len(s) - n:] + "..."

        raise SystemError("Unrecognized byte order: \"{:}\""
                          .format(sys.byteorder))

    return s
