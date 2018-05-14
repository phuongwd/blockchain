#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import sys
import time
from _thread import interrupt_main
from queue import Queue
from threading import Timer, Thread, Condition
from typing import Iterable

import blockchain
import blockchain_rpc
from blockchain import constants
from blockchain.transaction_strategies import favor_higher_fees
from utils import PriorityQueue, int_to_bytes, bin_str, bytes_to_int, console

service = blockchain_rpc.Service()


class FullNode(blockchain_rpc.BlockchainNode):
    def __init__(self, config):
        """
        Implements full node that not only tracks other nodes, but also
        maintains full blockchain, accepts transactions and mines new blocks.
        """
        super(FullNode, self).__init__(config)
        self._hash_prev = None
        self._difficulty = config.difficulty
        self._mining_throttle_ms = config.mining_throttle_ms

        self._blockchain = set()

        # Producer-consumer queues for exchanging data with the mining thread
        self._transaction_queue = PriorityQueue(f_priority=favor_higher_fees)
        self._block_queue = Queue()

        self._mining = config.mining

        # Launch mining and block and transaction discovery
        if self._mining:
            Thread(target=self.mine, name="mine").start()

            Thread(target=self.discover_blocks).start()

            Thread(target=self.share_blocks).start()

            Thread(target=self.discover_transactions).start()

        # Launch transaction generating and sharing
        if self._mining or config.gen_transactions:
            Thread(target=self.generate_transactions).start()

            Thread(target=self.share_transactions).start()

    def add_genesis_block(self):
        """
        Assembles genesis block, the first block in the blockchain.
        It is hardcoded and the same for every mining node.
        """
        coinbase_transaction = self.create_coinbase_transaction(
            dest_key=constants.GENESIS_BLOCK_DEST_KEY
        )

        transactions = [coinbase_transaction]

        genesis_block = blockchain.Block(
            hash_prev=constants.GENESIS_BLOCK_HASH_PREV,
            difficulty=constants.GENESIS_BLOCK_DIFFICULTY,
            hash=constants.GENESIS_BLOCK_HASH,
            merkle_root=constants.GENESIS_BLOCK_MERKLE_ROOT,
            nonce=constants.GENESIS_BLOCK_NONCE,
            extra_nonce=constants.GENESIS_BLOCK_EXTRA_NONCE,
            transactions=transactions
        )

        self._hash_prev = genesis_block.hash
        self._blockchain.add(genesis_block)

    def generate_transactions(self):
        """
        Generates random transactions
        """

        transaction_generator = blockchain.TransactionGeneratorFake(
            blocks=self._blockchain,
            peers=self._known_peers,
            ecdsa=self._ecdsa
        )

        while True:
            if len(self._transaction_queue.items) \
                    < constants.BLOCK_MAX_TRANSACTIONS:
                transaction = transaction_generator.generate()
                self._transaction_queue.put(transaction)
            time.sleep(3)

    def create_coinbase_transaction(self, dest_key=None):
        """
        Creates a coinbase transaction. This transaction is included as the
        first transaction of the block and is creating a fixed amount of coins
        """

        coinbase_output = blockchain.TransactionOutput(
            amount=constants.BLOCK_COINBASE_AMOUNT,
            key=dest_key or self._ecdsa.public_key
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

        self.add_genesis_block()

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

    def mine_one_iteration(self, block: blockchain.Block):
        """
        Perform one iteration of block mining (increments the nonce once)
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
