#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

import blockchain


class TestTransactionInput(TestCase):
    def test_tx_input_bytes(self):
        tx_input = blockchain.TransactionInput(
            src_hash=b"hello",
            src_idx=1,
            signature=b"signed_",
            key=b"with_key"
        )

        assert b"hello\x01signed_with_key" == tx_input.bytes
