#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from rpc import BlockchainNode


class DNSSeeder(BlockchainNode):
    def __init__(self, host, port, known_peers, max_workers=5):
        """
        Implements DNS-seed server, which is a node that provides only two-way
        peer discovery service for other nodes. This node does not participate
        in blockchain maintenance, serving clients or in mining.

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(DNSSeeder, self).__init__(host, port, known_peers, max_workers)
