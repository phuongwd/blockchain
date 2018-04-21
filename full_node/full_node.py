#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from rpc import BlockchainNode


class FullNode(BlockchainNode):
    def __init__(self, host, port, seeders, max_workers=5):
        """
        Implements DNS-seed server, which is a node that provides only two-way
        peer discovery service for other nodes. This node does not participate
        in blockchain maintenance, serving clients or in mining.

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(FullNode, self).__init__(host, port, max_workers)

        for (host, port) in seeders:
            seeder = self.add_seeder(host, port)
            self.send_known_peers_to(seeder)

            peers = seeder.stub.get_peers(self._messages.Empty())

            for peer in peers:
                if not self.is_known_peer(peer):
                    peer = self.add_peer(peer.host, peer.port, peer.address)
                    self.send_known_peers_to(peer)
