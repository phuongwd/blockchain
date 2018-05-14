#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from utils import dict_to_namedtuple

constants = dict_to_namedtuple({
    "BLOCK_COINBASE_AMOUNT": 25000,
    "BLOCK_MAX_TRANSACTIONS": 5,
    "TRANSACTION_MAX_INPUTS": 5,
    "TRANSACTION_MAX_OUTPUTS": 5,
    "GENESIS_BLOCK_HASH_PREV": bytes.fromhex("cafebabe"),
    "GENESIS_BLOCK_DEST_KEY": bytes.fromhex("ba5eba11"),
    "GENESIS_BLOCK_HASH":  bytes.fromhex("a85412322c12b3591f9bcf21ee089dd147b67f15d9ad7f76ca47fe3e65033f00"),
    "GENESIS_BLOCK_MERKLE_ROOT":  bytes.fromhex("386a475ba7f0f47fa9967e8ab17d5349bf19f5903cd262ad6a0bd5a6ed5fa36b"),
    "GENESIS_BLOCK_NONCE": 829,
    "GENESIS_BLOCK_EXTRA_NONCE": 1,
    "GENESIS_BLOCK_DIFFICULTY": 10
})
