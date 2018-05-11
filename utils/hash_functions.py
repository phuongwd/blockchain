#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import hashlib
import scrypt as scryptlib

def md5(s: bytes):
    """
    Produces MD5 hash of the input. Assumes platform is little-endian
    """
    return hashlib.md5(s).digest()


md5.bits = 128


def sha256(s: bytes):
    """
    Produces SHA-256 hash of the input. Assumes platform is little-endian
    """
    return hashlib.sha256(s).digest()


sha256.bits = 256


def scrypt(s: bytes):
    """
    Produces SHA-256 hash of the input. Assumes platform is little-endian
    """
    return scryptlib.hash(password=s, salt='')


scrypt.bits = 64 * 8
