#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

from blockchain import Transaction
from utils import MockConvertibleToBytes, bytes_to_int

Bytes = MockConvertibleToBytes


class TestTransaction(TestCase):
    def setUp(self):
        pass

    def test_tx_reduce_empty(self):
        assert b"" == Transaction._reduce([])

    def test_tx_reduce_list(self):
        inputs = [Bytes(b"one"), Bytes(b"two"), Bytes(b"three")]
        assert b"onetwothree" == Transaction._reduce(inputs)

    def test_tx_bytes(self):
        inputs = [Bytes(b"one"), Bytes(b"two"), Bytes(b"three")]
        outputs = [Bytes(b"abc"), Bytes(b"xyz")]

        tx = Transaction(
            inputs=inputs,
            outputs=outputs,
            hash_f=lambda x: x
        )

        assert b"onetwothreeabcxyz\x00" == tx.bytes

    def test_tx_hash(self):
        inputs = [Bytes(b"one"), Bytes(b"two"), Bytes(b"three")]
        outputs = [Bytes(b"abc"), Bytes(b"xyz")]

        tx = Transaction(
            inputs=inputs,
            outputs=outputs,
            hash_f=lambda x: b"(" + x + b")"
        )

        assert b"(onetwothreeabcxyz\x00)" == tx.hash

    def test_tx_hash_with_extra_nonce(self):
        inputs = [Bytes(b"one"), Bytes(b"two"), Bytes(b"three")]
        outputs = [Bytes(b"abc"), Bytes(b"xyz")]

        tx = Transaction(
            inputs=inputs,
            outputs=outputs,
            hash_f=lambda x: b"(" + x + b")"
        )

        tx.extra_nonce = bytes_to_int(bytes("X".encode("utf-8")))

        assert b"(onetwothreeabcxyzX)" == tx.hash
