#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from rpc import BlockchainNode


class DNSSeeder(BlockchainNode):
    def __init__(self, config):
        """
        Implements DNS-seeder, which is the node that provides only peer
        discovery service for other nodes. This node does not participate
        in blockchain maintenance, in serving clients or in mining.
        """
        super(DNSSeeder, self).__init__(config)
