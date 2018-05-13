#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import sys
import time
from queue import Queue
from threading import Timer, Thread
from typing import Iterable

import blockchain
import blockchain_rpc
from blockchain import constants
from blockchain.transaction_strategies import favor_higher_fees
from blockchain.fake_transaction_generator import FakeTransactionGenerator
from utils import PriorityQueue, int_to_bytes, bin_str, bytes_to_int, console

service = blockchain_rpc.Service()


class FullNode(blockchain_rpc.BlockchainNode):
    def __init__(self, config):
        """
        Implements full node that not only tracks other nodes, but also
        maintains full blockchain, accepts transactions and mines new blocks.
        """
        super(FullNode, self).__init__(config)

        self._blockchain = set()

        self._public_key = int_to_bytes(random.randint(0, sys.maxsize))

        self._hash_prev = int_to_bytes(0)
        self._difficulty = config.difficulty
        self._mining_throttle_ms = config.mining_throttle_ms

        # Producer-consumer queues for exchanging data with the mining thread
        self._transaction_queue = PriorityQueue(f_priority=favor_higher_fees)
        self._block_queue = Queue()

        self._mining = True

        # Launch mining thread (consumes transactions, produces blocks)
        Thread(target=self.mine, name="mine").start()

        # Launch transaction generating thread (produces transactions)
        Thread(target=self.generate_transactions,
               name="generate_transactions").start()

        # Launch discovery/sharing services
        Thread(target=self.discover_blocks,
               name="discover_blocks").start()

        Thread(target=self.share_blocks,
               name="share_blocks").start()

        Thread(target=self.discover_transactions,
               name="discover_transactions").start()

        Thread(target=self.share_transactions,
               name="share_transactions").start()

    def generate_transactions(self):
        transaction_generator = FakeTransactionGenerator()

        for _ in range(5):
            transaction = transaction_generator.generate()
            self._transaction_queue.put(transaction)

        while self._mining:
            if len(self._transaction_queue.items) < 15:
                transaction = transaction_generator.generate()
                self._transaction_queue.put(transaction)
            time.sleep(3)

    def create_coinbase_transaction(self):
        coinbase_output = blockchain.TransactionOutput(
            amount=constants.BLOCK_COINBASE_AMOUNT,
            key=self._public_key
        )

        coinbase_tx = blockchain.Transaction(
            inputs=[],
            outputs=[coinbase_output],
        )

        return coinbase_tx

    def mine(self):
        """
        Mines new blocks
        """

        i = 0
        while self._mining:
            coinbase_transaction = self.create_coinbase_transaction()
            transactions = [coinbase_transaction]

            for _ in range(constants.BLOCK_MAX_TRANSACTIONS - 1):
                # transaction = self._transaction_generator.generate()
                transaction = self._transaction_queue.get()
                transactions.append(transaction)

            block = blockchain.Block(
                hash_prev=self._hash_prev,
                difficulty=self._difficulty,
                transactions=transactions,
            )

            console.info(
                "Mining a new block:" + " " * 32 +
                "\n{:}\n".format(block.summary)
            )

            found = False
            while not found:
                found = self.mine_one_iteration(block)
                # Throttle mining to reduce CPU load (for the demo)
                time.sleep(self._mining_throttle_ms / 1000)

            i += 1

            if i > 3:
                self._mining = False
                print("Not mining")

    def mine_one_iteration(self, block: blockchain.Block):
        """
        Perform one iteration of a block mining (increments nonce once)
        """

        found, nonce, curr_hash = block.mine_one()

        sys.stdout.write("Nonce: {:010d} | Hash : {:}\r".format(
            nonce,
            bin_str(bytes_to_int(curr_hash), pad=service.hash_f.bits)
        ))

        if found:
            console.info("Found a new block:" + " " * 32 + "\n{:}\n".format(
                block.details))
            self._blockchain.add(block)
            self._hash_prev = block.hash

        return found

    def discover_transactions(self):
        if self._config.transaction_discovery_interval >= 0:
            while True:
                known_peers = set(self._known_peers)
                for peer in known_peers:
                    transactions = peer.get_transactions()
                    for transaction in transactions:
                        self._transaction_queue.put(transaction)
                time.sleep(self._config.transaction_discovery_interval)

    def share_transactions(self):
        if self._config.transaction_sharing_interval >= 0:
            while True:
                known_peers = set(self._known_peers)
                transactions = self._transaction_queue.items
                for peer in known_peers:
                    peer.send_transactions(transactions)
                time.sleep(self._config.transaction_sharing_interval)

    def discover_blocks(self):
        if self._config.block_discovery_interval >= 0:
            while True:
                known_peers = set(self._known_peers)
                for peer in known_peers:
                    blocks = peer.get_blocks()
                    for block in blocks:
                        self._blockchain.add(block)
                time.sleep(self._config.block_discovery_interval)

    def share_blocks(self):
        if self._config.block_sharing_interval >= 0:
            while True:
                known_peers = set(self._known_peers)
                blocks = list(self._blockchain)
                for peer in known_peers:
                    peer.send_blocks(blocks)
                time.sleep(self._config.block_sharing_interval)

    def get_transactions(self, _, __):
        """
        RPC server handler triggered on get_transactions RPC call
        """

        transactions = list(self._transaction_queue.items)
        for transaction in transactions:
            yield transaction.to_proto()

    def send_transactions(self, transactions: Iterable, _):
        """
        RPC server handler triggered on send_transactions RPC call
        """

        for transaction in transactions:
            transaction = blockchain.Transaction.from_proto(transaction)
            if transaction is not None:
                self._transaction_queue.put(transaction)

        return service.messages.Empty()

    def get_blocks(self, _, __):
        """
        RPC server handler triggered on get_blocks RPC call
        """
        blocks = list(self._blockchain)
        for block in blocks:
            yield block.to_proto()

    def send_blocks(self, blocks: Iterable, _):
        """
        RPC server handler triggered on send_blocks RPC call
        """
        for block in blocks:
            block = blockchain.Block.from_proto(block)
            if block is not None:
                self._blockchain.add(block)

        return service.messages.Empty()
