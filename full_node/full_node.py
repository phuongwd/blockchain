#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import sys
import time
from queue import Queue
from typing import Iterable

import blockchain
from blockchain import Transaction, favor_higher_fees, Block
from blockchain.fake_transaction_generator import FakeTransactionGenerator
from rpc import BlockchainNode
from utils import PriorityQueue, int_to_bytes, bin_str, bytes_to_int


class FullNode(BlockchainNode):
    def __init__(self, config):
        """
        Implements full node that not only tracks other nodes, but also
        maintains full blockchain, accepts transactions and mines new blocks.
        """
        super(FullNode, self).__init__(config)

        self._blockchain = list()
        self._transactions = list()

        self._public_key = int_to_bytes(random.randint(0, sys.maxsize))
        self._hash_f = getattr(blockchain, config.hash_f)
        self._hash_prev = int_to_bytes(0)
        self._difficulty = config.difficulty
        self._mining_throttle_ms = config.mining_throttle_ms

        # Producer-consumer queues for exchanging data with the mining thread
        self._transaction_queue = PriorityQueue(f_priority=favor_higher_fees)
        self._block_queue = Queue()

        # FIXME: fake transaction source
        self._transaction_generator = FakeTransactionGenerator(self._hash_f)

        # Launch mining thread (consumes transactions, produces blocks)
        # Thread(target=self.mine).start()

    def mine(self):
        """
        Mines new blocks
        """

        while True:
            transactions = []
            for _ in range(5):
                transaction = self._transaction_generator.generate()
                # transaction = self._transaction_queue.get()
                transactions.append(transaction)

            block = Block(
                hash_prev=self._hash_prev,
                difficulty=self._difficulty,
                transactions=transactions,
                key=self._public_key,
                hash_f=self._hash_f
            )

            self.log_info(
                "Mining a new block:" + " " * 32 +
                "\n{:}\n".format(block.summary)
            )

            found = False
            while not found:
                found = self.mine_one_iteration(block)

                # Throttle mining to reduce CPU load (for the demo)
                time.sleep(self._mining_throttle_ms / 1000)

    def mine_one_iteration(self, block):
        """
        Perform one iteration of a block mining (increments nonce once)
        """

        found, nonce, curr_hash = block.mine_one()

        sys.stdout.write("Nonce: {:010d} | Hash : {:}\r".format(
            nonce,
            bin_str(bytes_to_int(curr_hash), pad=self._hash_f.bits)
        ))

        if found:
            self.log_info("Found a new block:" + " " * 32 +
                          "\n{:}\n".format(block.details))
            self._block_queue.put(block)
            self._hash_prev = block.hash

        return found

    # def discover_blocks(self, config):
    #     if config.block_discovery_interval >= 0:
    #         self.log_debug("> discovering blocks")
    #
    #         self._known_peers_lock.acquire()
    #         known_peers = list(self._known_peers)
    #         self._known_peers_lock.release()
    #
    #         for peer in known_peers:
    #             self.recv_peers_from(peer)
    #
    #         self.schedule_peer_discovery(config)
    #
    # def schedule_peer_discovery(self, config):
    #     """
    #     Schedules peer discovery on a separate thread
    #     """
    #     if config.peer_discovery_interval > 0:
    #         threading.Timer(
    #             config.peer_discovery_interval,
    #             function=self.discover_peers,
    #             args=[config]
    #         ).start()
    #
    # def share_peers(self, config):
    #     """
    #     Run peer sharing and then schedule it to run periodically.
    #     Peer sharing consist of sending all known peers to all known peers.
    #     """
    #
    #     if config.peer_sharing_interval >= 0:
    #         self.log_debug("> sharing peers")
    #
    #         self._known_peers_lock.acquire()
    #         known_peers = set(self._known_peers)
    #         self._known_peers_lock.release()
    #
    #         for peer in known_peers:
    #             is_connected = peer.connect()
    #
    #             if not is_connected:
    #                 continue
    #
    #             self.send_peers_to(peer)
    #
    #         self.schedule_peer_sharing(config)
    #
    # def schedule_peer_sharing(self, config):
    #     """
    #     Schedules peer sharing on a separate thread
    #     """
    #     if config.peer_sharing_interval > 0:
    #         threading.Timer(
    #             config.peer_sharing_interval,
    #             function=self.share_peers,
    #             args=[config]
    #         ).start()

    def get_transactions(self, _, __):
        """
        RPC server handler triggered on get_transactions RPC call
        """

        for transaction in self._transaction_queue:
            yield transaction.to_proto()

    def send_transactions(self, transactions: Iterable[Transaction], _):
        """
        RPC server handler triggered on send_transactions RPC call
        """

        for transaction in transactions:
            transaction = Transaction.from_proto(transaction)
            if transaction is not None:
                self._transaction_queue.put(transaction)

        return self._messages.Empty()

    def get_blocks(self, _, __):
        """
        RPC server handler triggered on get_blocks RPC call
        """
        for block in self._blockchain:
            yield block.to_proto()

    def send_blocks(self, blocks: Iterable[Block], _):
        """
        RPC server handler triggered on send_blocks RPC call
        """
        for block in blocks:
            block = Block.from_proto(block)
            if block is not None:
                self._block.put(block)

        return self._messages.Empty()
