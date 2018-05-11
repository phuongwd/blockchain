#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import blockchain_rpc
from utils import int_to_bytes

service = blockchain_rpc.Service()


class TransactionInput:
    def __init__(self, src_hash: bytes, src_idx: int, signature: bytes):
        self._src_hash = src_hash
        self._src_idx = src_idx
        self._signature = signature

    @property
    def bytes(self):
        return self._src_hash + int_to_bytes(self._src_idx) + self._signature

    @property
    def src_hash(self):
        return self._src_hash

    @property
    def src_idx(self):
        return self._src_idx

    @property
    def signature(self):
        return self._signature

    @staticmethod
    def from_proto(proto):
        return TransactionInput(
            src_hash=proto.src_hash,
            src_idx=proto.src_idx,
            signature=proto.signature
        )

    def to_proto(self):
        try:
            return service.messages.TransactionInput(
                src_hash=int_to_bytes(0),
                src_idx=0,
                signature=int_to_bytes(0)
            )
        except:
            print(self)
            exit(0)
