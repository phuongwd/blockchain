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

from blockchain_rpc import Service

from utils import int_to_bytes

service = Service()


class TransactionGeneratorFake:
    """
    Generates fake transactions that do not verify signatures or amounts spend
    """

    def __init__(self, blocks, peers, ecdsa):
        self._ecdsa = ecdsa

    def generate(self):
        inputs = \
            [
                TransactionInput(
                    src_hash=int_to_bytes(
                        random.randint(0, sys.maxsize)),
                    src_idx=random.randint(
                        0, constants.TRANSACTION_MAX_OUTPUTS),
                    signature=int_to_bytes(
                        random.randint(0, sys.maxsize)),
                    key=self._ecdsa.public_key
                )
                for _ in range(constants.TRANSACTION_MAX_INPUTS)
            ]

        outputs = \
            [
                TransactionOutput(
                    amount=random.randint(0, 1000),
                    key=int_to_bytes(random.randint(0, sys.maxsize)),
                )
                for _ in range(constants.TRANSACTION_MAX_OUTPUTS)
            ]

        return Transaction(
            inputs=inputs,
            outputs=outputs
        )
