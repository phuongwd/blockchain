#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import sys

from blockchain import (
    TransactionInput, constants, TransactionOutput, Transaction
)

from utils import int_to_bytes


class FakeTransactionGenerator:
    def __init__(self, hash_f):
        self._hash_f = hash_f

    def generate(self):
        inputs = \
            [
                TransactionInput(
                    src_hash=int_to_bytes(random.randint(0, sys.maxsize)),
                    src_idx=random.randint(0, sys.maxsize),
                    signature=int_to_bytes(random.randint(0, sys.maxsize)),
                )
                for _ in range(constants.TRANSACTION_MAX_INPUTS)
            ]

        outputs = \
            [
                TransactionOutput(
                    amount=random.randint(0, sys.maxsize),
                    key=int_to_bytes(random.randint(0, sys.maxsize)),
                )
                for _ in range(constants.TRANSACTION_MAX_OUTPUTS)
            ]

        return Transaction(
            inputs=inputs,
            outputs=outputs,
            hash_f=self._hash_f
        )
