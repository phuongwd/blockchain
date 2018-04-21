#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import sys
from typing import List

import protol

from blockchain import (
    Transaction, TransactionOutput, md5, MerkleTree
)
from utils import bin_str, bytes_to_int
from utils.int_to_bytes import int_to_bytes

COINBASE_AMOUNT = 25


class Block:
    def __init__(
            self,
            hash_prev: bytes,
            difficulty: int,
            transactions: List[Transaction],
            key: bytes,
            hash_f
    ):
        self._hash_prev = hash_prev
        self._difficulty = difficulty
        self._target = 2 ** (128 - self._difficulty + 1) - 1
        self._hash_f = hash_f

        # Prepend conbase transaction
        coinbase_output = TransactionOutput(amount=COINBASE_AMOUNT, key=key)

        coinbase_tx = Transaction(
            inputs=[],
            outputs=[coinbase_output],
            hash_f=self._hash_f
        )

        self._transactions = [coinbase_tx] + transactions

        # Data to be computed
        self._nonce = 0
        self._hash = None
        self._merkle_root = None
        self._merkle_tree = None
        self._bytes = None

        # Set first extra nonce (triggers update)
        self.extra_nonce = 0

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def target(self):
        return self._target

    @property
    def extra_nonce(self) -> int:
        return self._transactions[0].extra_nonce

    @extra_nonce.setter
    def extra_nonce(self, extra_nonce: int) -> None:
        self._transactions[0].extra_nonce = extra_nonce
        self._nonce = 0
        self._update()

    def _update(self):
        # Recompute the tree of transactions
        merkle_tree = MerkleTree(
            leaves=[tx.hash for tx in self._transactions],
            f_hash=lambda tx: self._hash_f(tx)
        )
        self._merkle_root = merkle_tree.root_hash
        self._merkle_tree = merkle_tree.data
        self._bytes = \
            self._hash_prev + self._merkle_root + bytes(self._difficulty)

    def to_proto(self):
        assert 0 <= self._nonce < 2 ** 32, \
            "Nonce should be a 32-bit unsigned integer"

        PROTO_PATH = os.path.join("..", "protos", "blockchain.proto")
        messages, _ = protol.load(PROTO_PATH)

        return messages.Block(
            version=1,
            hash=self._hash,
            hash_prev=self._hash_prev,
            difficulty=self._difficulty,
            nonce=self._nonce,
            merkle_root=self._merkle_root,
            transactions=[tx.to_proto() for tx in self._transactions]
        )

    def from_proto(self, block):
        # TODO
        pass

    def mine_one(self):
        hash = self._hash_f(self._bytes + bytes(self._nonce))

        # If target is meet, we found the nonce
        if bytes_to_int(hash) < self.target:
            return True, self._nonce, hash

        # If target is not met proceed with the next nonce on next call
        self._nonce += 1

        # Increment extra nonce if nonce overflows
        if self._nonce >= 2 ** 32 - 1:
            self.extra_nonce += 1
            self._nonce = 0

        return False, self._nonce, hash
