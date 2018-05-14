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

from utils import int_to_bytes, console

service = Service()


class TransactionGenerator:
    def __init__(self, blocks, peers, ecdsa):
        self._blocks = blocks,
        self._peers = peers,
        self._ecdsa = ecdsa

    def find_unspent(self):
        raise NotImplementedError

        flat_blocks = [
            (block, tx, out, out_idx)
            for block in self._blocks
            for tx in block.transactions
            for out, out_idx in enumerate(tx.outputs)
        ]

        # Find outputs that belong to this address
        def my_output(flat_block):
            (_, __, out, ___) = flat_block
            return out.key == self._ecdsa.public_key

        my_outputs = filter(my_output, flat_blocks)

        # Find outputs that are unspent
        def unspent(flat_block):
            (_, tx, out, out_idx) = flat_block

            for other_flat_block in flat_blocks:
                (_, input, __, ___) = other_flat_block
                if input.src_idx == tx.hash and input.src_idx == out.key:
                    pass

            # Not spend in any of transactions
            return True

        my_outputs = filter(my_outputs)

        return tx, src_idx, amount_available

    def peers_with_address(self):
        """
        Returns peers with known addresses
        """

        def has_address(peer):
            return peer.address is not None and len(peer.address) > 0

        return filter(has_address, self._peers)

    def generate(self):
        console.info("generating a transaction")

        tx, src_idx, amount_available = self.find_unspent()

        src_hash = tx.hash
        message = src_hash + int_to_bytes(src_idx)
        signature = self._ecdsa.sign(message)
        key = self._ecdsa.public_key

        tx_input = TransactionInput(
            src_hash=src_hash,
            src_idx=src_idx,
            signature=signature,
            key=key
        )

        amount_send = int(amount_available * random.random())
        fee = int((amount_available - amount_send) * random.random())
        amount_rest = amount_available - amount_send - fee

        peers_with_address = self.peers_with_address()

        # If no known peers, we will send to ourselves
        receiver_key = self._ecdsa.public_key

        # Choose coin receiver at random
        try:
            receiver = random.choice(peers_with_address)
            receiver_key = receiver.address
        except IndexError:
            pass

        # Output that transfers `amount_send` coins to the chosen node
        output_send = TransactionOutput(
            amount=amount_send,
            key=receiver_key
        )

        # Output that transfers the rest of the coins back to us.
        # The coins that are not in outputs constitute the transaction fee
        # (will be collected by the miner who will incude this transaction into
        # a new block)
        output_rest = TransactionOutput(
            amount=amount_rest,
            key=self._ecdsa.public_key
        )

        return Transaction(
            inputs=[tx_input],
            outputs=[output_send, output_rest]
        )
