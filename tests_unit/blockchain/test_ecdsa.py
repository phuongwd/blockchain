#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import binascii
from unittest import TestCase

from blockchain import ECDSA
from utils import bin_to_hex


class TestECDSA(TestCase):
    """
    Implements a set of unit tests for ECDSA
    """

    def setUp(self):
        self.ecdsa = ECDSA(
            "../.tmp/unit_tests"
        )

    def test_ecdsa_signature_and_verification(self):
        message = "Hello, world!".encode("utf-8")
        signature = self.ecdsa.sign(message)
        public_key = self.ecdsa.public_key
        assert ECDSA.verify(public_key, signature, message)
