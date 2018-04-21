#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys
import random

from blockchain import md5, Block, sha256, scrypt
from utils import bin_str, bytes_to_int, int_to_bytes


def main():
    hash_prev = int_to_bytes(3940898798)
    difficulty = 7
    hash_f = scrypt
    transactions = []
    key = int_to_bytes(3776076139)

    while True:
        hash_prev = int_to_bytes(random.randint(0, 3776076139))

        block = Block(hash_prev, difficulty, transactions, key, hash_f)

        print("Mining")
        print("Difficulty               : {:}".format(block.difficulty))
        print("Target                   : {:}".format(
            bin_str(block.target, pad=hash_f.bits))
        )

        is_mining = True
        found = False
        nonce = None
        hash = None
        while is_mining and not found:
            found, nonce, hash = block.mine_one()
            hash_str = bin_str(bytes_to_int(hash), pad=hash_f.bits)
            sys.stdout.write(
                "Nonce: {:010d} | Hash : {:}\r".format(nonce, hash_str)
            )

        if found:
            print("\nFound new block! Nonce: {:}".format(nonce))


if __name__ == "__main__":
    main()
