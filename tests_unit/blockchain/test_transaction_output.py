#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

import blockchain


class TestTransactionOutput(TestCase):
    def test_tx_output_bytes(self):
        tx_input = blockchain.TransactionOutput(
            amount=65,
            key=b"publickey"
        )

        # character 'A' has ASCII code 65
        assert b"Apublickey" == tx_input.bytes
