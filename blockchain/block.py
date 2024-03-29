#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from typing import List

import blockchain
from blockchain_rpc import Service

from utils import (
    bin_str, bytes_to_int, create_target, bin_to_hex, int_to_bytes
)

service = Service()


class Block:
    def __init__(
            self,
            hash_prev: bytes,
            difficulty: int,
            transactions: List,
            nonce: int = 0,
            extra_nonce: int = 0,
            hash: bytes = None,
            merkle_root=None
    ):
        self._hash_prev = hash_prev
        self._difficulty = difficulty
        self._target = create_target(service.hash_f.bits, difficulty)
        self._transactions = transactions
        self._nonce = nonce
        self.extra_nonce = extra_nonce
        self._hash = hash
        self._merkle_root = merkle_root
        self._merkle_tree = None
        self._bytes = None

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def target(self):
        return self._target

    @property
    def hash_prev(self):
        return self._hash_prev

    @property
    def hash(self):
        return self._hash

    @property
    def nonce(self):
        return self._nonce

    @property
    def coinbase_transaction(self):
        return self._transactions[0]

    @property
    def transactions(self):
        return self._transactions

    @property
    def extra_nonce(self) -> int:
        return self.coinbase_transaction.extra_nonce

    @extra_nonce.setter
    def extra_nonce(self, extra_nonce: int) -> None:
        self._transactions[0].extra_nonce = extra_nonce

    @property
    def merkle_root(self):
        return self._merkle_root

    def update_merkle_tree(self):
        # Recompute the tree of transactions
        merkle_tree = blockchain.MerkleTree(
            leaves=[tx.hash for tx in self._transactions],
            f_hash=lambda tx: service.hash_f(tx)
        )
        self._merkle_root = merkle_tree.root_hash
        self._merkle_tree = merkle_tree.data
        self._bytes = \
            self._hash_prev + self._merkle_root + bytes(self._difficulty)

    def to_proto(self):
        assert 0 <= self._nonce < 2 ** 32, \
            "Nonce should be a 32-bit unsigned integer"

        return service.messages.Block(
            version=1,
            hash_prev=self._hash_prev,
            hash=self._hash,
            difficulty=self._difficulty,
            nonce=self._nonce,
            merkle_root=self._merkle_root,
            transactions=[tx.to_proto() for tx in self._transactions]
        )

    @staticmethod
    def from_proto(proto):
        transactions = [
            blockchain.Transaction.from_proto(tx)
            for tx in proto.transactions
        ]

        # Block should contain at least 1 transaction: a coinbase transaction
        if 1 < len(transactions) < blockchain.constants.BLOCK_MAX_TRANSACTIONS:
            return None

        extra_nonce = proto.transactions[0].extra_nonce

        block = Block(
            hash=proto.hash,
            hash_prev=proto.hash_prev,
            difficulty=proto.difficulty,
            nonce=proto.nonce,
            extra_nonce=extra_nonce,
            merkle_root=proto.merkle_root,
            transactions=transactions
        )

        return block

    @property
    def summary(self):
        return \
            "Num. transactions        : {:}\n" \
            "Difficulty               : {:}\n" \
            "Previous block           : {:}\n" \
            "Target                   : {:}\n" \
                .format(
                len(self._transactions),
                self._difficulty,
                bin_to_hex(self.hash_prev),
                bin_str(self.target, pad=service.hash_f.bits),
            )

    @property
    def details(self):
        return self.summary + \
               "Hash (bin)               : {:}\n" \
               "Hash (hex)               : {:}\n" \
               "Nonce                    : {:010d}\n" \
               "Extra-nonce              : {:010d}\n" \
               "Merkle root              : {:}\n" \
                   .format(
                   bin_str(bytes_to_int(self.hash), pad=service.hash_f.bits),
                   bin_to_hex(self.hash),
                   self.nonce,
                   self.extra_nonce,
                   bin_to_hex(self.merkle_root)
               )

    def __str__(self):
        return self.details

    def mine_one(self):
        # Increment extra nonce if nonce overflows and update merkle tree
        if self._nonce == 0 or self._nonce >= 2 ** 32 - 1:
            self.extra_nonce += 1
            self._nonce = 0
            self.update_merkle_tree()

        # Calculate hash with current nonce and extra_nonce
        curr_hash = service.hash_f(self._bytes + int_to_bytes(self._nonce))

        # If target is meet, we found the nonce
        if bytes_to_int(curr_hash) < self.target:
            self._hash = curr_hash
            return True, self._nonce, self._hash

        # If target is not met proceed with the next nonce on next call
        self._nonce += 1

        return False, self._nonce, curr_hash
