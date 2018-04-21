#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
from functools import reduce
from typing import List, Callable, Any

import protol

from blockchain import TransactionInput, TransactionOutput


class Transaction:
    def __init__(
            self,
            inputs: List[TransactionInput],
            outputs: List[TransactionOutput],
            hash_f: Callable[[Any], bytes]
    ):
        self._inputs = inputs
        self._outputs = outputs
        self._extra_nonce = 0

        self._hash_f = hash_f
        self._hash = None
        self.update()

    @staticmethod
    def _reduce(arr):
        return reduce(
            lambda x, y: x + y,
            map(lambda x: x.bytes, arr),
            bytes()
        )

    @property
    def bytes(self):
        return self._reduce(self._inputs) + self._reduce(self._outputs) \
               + bytes([self.extra_nonce])

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
        PROTO_PATH = os.path.join("..", "protos", "blockchain.proto")
        messages, _ = protol.load(PROTO_PATH)

        serialized_inputs = [
            messages.TransactionInput()
            for input in self._inputs
        ]

        serialized_outputs = [
            messages.TransactionOutput()
            for output in self._outputs
        ]

        assert 0 <= self._extra_nonce < 2 ** 32, \
            "Extra nonce should be a 32-bit unsigned integer"

        return messages.Transaction(
            version=1,
            hash=self._hash,
            extra_nonce=self._extra_nonce,
            inputs=serialized_inputs,
            outputs=serialized_outputs
        )

    def from_proto(self):
        # TODO
        pass
