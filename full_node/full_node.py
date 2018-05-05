#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from typing import Iterable

from blockchain import Transaction, favor_higher_fees, Block
from rpc import BlockchainNode
from utils import PriorityQueue


class FullNode(BlockchainNode):
    def __init__(self, host, port, known_peers, max_workers=5):
        """
        Implements DNS-seed server, which is a node that provides only two-way
        peer discovery service for other nodes. This node does not participate
        in blockchain maintenance, serving clients or in mining.

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(FullNode, self).__init__(host, port, known_peers, max_workers)

        self._transactions = PriorityQueue(f_priority=favor_higher_fees)
        self._blocks = list()


    def get_transactions(self, _, __):
        for transaction in self._transactions:
            yield transaction.to_proto()

    def send_transactions(self, transactions: Iterable[Transaction], _):
        for transaction in transactions:
            transaction = Transaction.from_proto(transaction)
            if transaction is not None:
                self._transactions.put(transaction)

        return self._messages.Empty()

    def get_blocks(self, _, __):
        for block in self._blocks:
            yield block.to_proto()

    def send_blocks(self, blocks: Iterable[Block], _):
        for block in blocks:
            block = Block.from_proto(block)
            if block is not None:
                self._block.put(block)

        return self._messages.Empty()
