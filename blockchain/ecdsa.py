#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import binascii
import hashlib
import os

import base58
import ecdsa

from utils import ensure_dir, int_to_bytes


class ECDSA:
    def __init__(self, key_path):
        """
        Implements Elliptic Curve Digital Signature Algorithm (ECDSA)
        for creating cryptographic key pairs, signing messages and verifying
        signatures later
        """
        ensure_dir(os.path.dirname(key_path))

        # Generate or read the private key
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                self._private_key = ecdsa.SigningKey.from_string(
                    f.read(), curve=ecdsa.SECP256k1
                )
        else:
            self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            with open(key_path, 'wb') as f:
                f.write(self._private_key.to_string())

        # Retrieve public key
        self._public_key = self._private_key.get_verifying_key()

        # Generate address from public key
        self._address = self.address_from_key(self.public_key)

    @property
    def public_key(self) -> bytes:
        return self._public_key.to_string()

    @property
    def address(self):
        return self._address

    def sign(self, message: bytes) -> bytes:
        """
        Sign a message using the key
        """
        signature = self._private_key.sign(message)
        return signature

    @staticmethod
    def address_from_key(public_key: bytes) -> bytes:
        address = hashlib.new('sha256', public_key).digest()
        address = hashlib.new('ripemd160', address).digest()
        address = base58.b58encode_check(bytes(address))
        return address

    @staticmethod
    def verify(public_key: bytes, signature: bytes, message: bytes) -> bool:
        """
        Verify that the signature is valid for a given key
        """
        public_key = ecdsa.VerifyingKey.from_string(
            public_key, curve=ecdsa.SECP256k1)
        return public_key.verify(signature, message)
