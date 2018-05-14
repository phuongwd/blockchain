#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from blockchain_rpc import Service
from utils import int_to_bytes

service = Service()


class TransactionOutput:
    """
    Implements a single output within a transaction
    """

    def __init__(self, amount: int, key: bytes):
        self._amount = amount
        self._key = key

    @property
    def bytes(self):
        return int_to_bytes(self._amount) + self._key

    @property
    def amount(self):
        return self._amount

    @property
    def key(self):
        return self._key

    @staticmethod
    def from_proto(proto):
        return TransactionOutput(
            amount=proto.amount,
            key=proto.key
        )

    def to_proto(self):
        return service.messages.TransactionOutput(
            amount=self.amount,
            key=self.key
        )
