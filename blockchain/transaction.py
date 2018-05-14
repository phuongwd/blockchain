#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from functools import reduce
from typing import List

import blockchain
from blockchain_rpc import Service

service = Service()


class Transaction:
    """
    Implements a single transaction within the block
    """
    def __init__(
            self,
            inputs: List,
            outputs: List,
            extra_nonce: int = 0,
            hash_f=None
    ):
        self._inputs = inputs
        self._outputs = outputs
        self._extra_nonce = extra_nonce

        self._fee = 0
        self._hash = None
        self._hash_f = hash_f or service.hash_f
        self.update()

    @staticmethod
    def _reduce(arr):
        """
        Converts every array elelemt to bytes and concatenates the results
        """
        return reduce(
            lambda x, y: x + y,
            map(lambda x: x.bytes, arr),
            bytes()
        )

    @property
    def bytes(self):
        """
        Converts everything to bytes and concatenates together
        """
        return self._reduce(self._inputs) + self._reduce(self._outputs) \
               + bytes([self.extra_nonce])

    @property
    def fee(self):
        return self._fee

    @property
    def hash(self):
        return self._hash

    @property
    def extra_nonce(self):
        return self._extra_nonce

    @extra_nonce.setter
    def extra_nonce(self, extra_nonce: int):
        self._extra_nonce = extra_nonce
        self.update()

    def update(self):
        self._hash = self._hash_f(self.bytes)

    def to_proto(self):
        assert 0 <= self._extra_nonce < 2 ** 32, \
            "Extra nonce should be a 32-bit unsigned integer"

        inputs = [i.to_proto() for i in self._inputs]
        outputs = [o.to_proto() for o in self._outputs]

        return service.messages.Transaction(
            version=1,
            hash=self._hash,
            extra_nonce=self._extra_nonce,
            inputs=inputs,
            outputs=outputs
        )

    @staticmethod
    def from_proto(proto):
        inputs = list(
            [blockchain.TransactionInput.from_proto(i) for i in proto.inputs])

        outputs = list(
            [blockchain.TransactionOutput.from_proto(o) for o in proto.outputs])

        return Transaction(
            inputs=inputs,
            outputs=outputs,
            extra_nonce=proto.extra_nonce
        )
