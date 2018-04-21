#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import hashlib

from utils import bytes_to_int


def md5(s: bytes):
    """
    Produces MD5 hash of the input. Assumes platform is little-endian
    """
    return hashlib.md5(s).digest()


def sha256(s: bytes):
    """
    Produces SHA-256 hash of the input. Assumes platform is little-endian
    """
    return hashlib.sha256(s).digest()
