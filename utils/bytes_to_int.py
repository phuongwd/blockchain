#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys


def bytes_to_int(b: bytes) -> int:
    """
    Re-interprets array of bytes as an integer. Endianness-independent.
    """
    return int.from_bytes(
        bytes=b,
        byteorder=sys.byteorder,
        signed=False
    )
