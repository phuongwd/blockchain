#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from unittest import TestCase

from blockchain import Block
from utils import MockConvertibleToBytes, bytes_to_int

Bytes = MockConvertibleToBytes


class TestBlock(TestCase):
    def setUp(self):
        self._block = Block(
            hash_prev=b"hello!",
            difficulty=42,
            transactions=[],
            key=b"private_key",
            hash_f=lambda x: x
        )

    # def test_block_inits_extra_nonce_to_zero(self):
    #     assert 0 == self._block.extra_nonce
