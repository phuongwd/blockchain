#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys
import random

from blockchain import md5, sha256, scrypt
from utils import bin_str, bytes_to_int, int_to_bytes, create_target

difficulty = 18
hash_f = sha256
target = create_target(hash_f.bits, difficulty)

print("Difficulty               : {:}".format(difficulty))
print("Target                   : {:}".format(bin_str(target, pad=hash_f.bits)))

found = False
nonce = 0
hash = None
while True:
    hash = hash_f(int_to_bytes(nonce))
    hash_str = bin_str(bytes_to_int(hash), pad=hash_f.bits)
    sys.stdout.write(
        "Nonce: {:010d} | Hash : {:}\r".format(nonce, hash_str)
    )

    if bytes_to_int(hash) < target:
        print("\nFound new block! Nonce: {:}".format(nonce))

    sys.stdout.flush()
    nonce += 1
