#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mines blockchain blocks from random data.

Usage:
  mining.py [--difficulty=<difficulty>] [--hash=<hash>] \
[--min_inputs=<min_inputs>] [--max_inputs=<max_inputs>] \
[--min_outputs=<min_outputs>] [--max_outputs=<max_outputs>]

Options:
  --difficulty=<difficulty>     Mining difficulty [default: 18]
  --hash=<hash>                 Hash function [default: sha256]. \
Supported functions: (sha256, md5, scrypt)
  --min_tx=<min_tx>             Minimum number of transactions in randomly \
  generated blocks [default: 0]
  --max_tx=<max_tx>             Maximum number of transactions in randomly \
  generated blocks [default: 10]
  --min_inputs=<min_inputs>     Minimum number of inputs in randomly \
  generated transactions [default: 0]
  --max_inputs=<max_inputs>     Maximum number of inputs in randomly \
  generated transactions [default: 10]
  --min_outputs=<min_outputs>   Minimum number of outputs in randomly \
  generated transactions [default: 0]
  --max_outputs=<max_outputs>   Maximum number of outputs in randomly \
  generated transactions [default: 10]
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys
import random
import docopt

import blockchain
from blockchain import Block, Transaction, TransactionInput, TransactionOutput
from utils import bin_str, bytes_to_int, int_to_bytes

# def random_transaction(hash_f, min_inputs, max_inputs, min_outputs, max_outputs):
#     inputs = [TransactionInput() for _ in range()]
#     outputs = [TransactionOutput()]
#     return Transaction(inputs=inputs, outputs=outputs, hash_f=hash_f)


def main():
    opts = docopt.docopt(__doc__)

    hash_f = opts["--hash"]
    if not hash_f in ("md5", "sha256", "scrypt"):
        sys.stderr.write(
            "Error:\n  Hash function \"{:}\" not supported\n".format(hash_f))
        sys.stderr.write(__doc__)
        sys.exit(1)

    hash_f = getattr(blockchain, hash_f)

    difficulty = int(opts["--difficulty"])
    if difficulty is None or difficulty < 0:
        sys.stderr.write(
            "Error:\n  Difficulty \n".format(hash_f))
        sys.stderr.write(__doc__)
        sys.exit(1)

    transactions = []

    key = int_to_bytes(random.randint(0, sys.maxsize))
    hash_prev = int_to_bytes(random.randint(0, sys.maxsize))

    while True:
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
            print("\nFound new block! Nonce: {:}\n".format(nonce))
            hash_prev = hash


if __name__ == "__main__":
    main()
