#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import threading

from rpc import BlockchainNode


class DNSSeeder(BlockchainNode):
    def __init__(self, host, port, max_workers=5):
        """
        Implements DNS-seed server, which is a node that provides only two-way
        peer discovery service for other nodes. This node does not participate
        in blockchain maintenance, serving clients or in mining.

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(DNSSeeder, self).__init__(host, port, max_workers)
        threading.Timer(3, self.share_peers).start()

    def share_peers(self):
        for peer in self._known_peers:
            self._log("Sharing peers with {:}".format(peer))
            self.send_known_peers_to(peer, include_self=False)
            threading.Timer(3, self.share_peers).start()
