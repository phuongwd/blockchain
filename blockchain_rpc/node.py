#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import threading
from threading import Lock
from concurrent import futures
from queue import Queue
from typing import Iterable

import grpc

import blockchain_rpc
from utils import wait_forever, console

service = blockchain_rpc.Service()


class BlockchainNode(service.Servicer):
    def __init__(self, config):
        """
        Base class for servers that implement blockchain service
        """
        super(BlockchainNode, self).__init__()
        self._config = config
        self._host = config.host
        self._port = int(config.port)
        self._server = grpc.server(
            futures.ThreadPoolExecutor(config.max_workers))
        service.add_service(self, self._server)
        self._server.add_insecure_port(
            "{:}:{:}".format(config.host, config.port))

        self._address = 0
        self._this_node = blockchain_rpc.Peer(host=config.host,
                                              port=config.port)

        self._known_peers = set()
        self._known_peers_lock = Lock()

        for peer in config.known_peers:
            self.maybe_add_peer(peer)

        self.schedule_peer_discovery()
        self.schedule_peer_sharing()

    def start(self):
        """
        Starts the RPC server
        """
        self._server.start()
        console.info("Listening on port {:}".format(self._port))

    def stop(self):
        """
        Stops the RPC server immediately
        """
        self._server.stop(grace=0)

    def listen(self):
        """
        Make RPC server to listen for incoming messages until ^C
        """

        self.start()

        try:
            wait_forever()
        except KeyboardInterrupt:
            self.stop()

    def maybe_add_peer(self, peer: blockchain_rpc.Peer):
        if self.is_known_peer(peer):
            return False

        console.info("> add  peer:  {:}".format(peer))
        with self._known_peers_lock:
            self._known_peers.add(peer)

        return peer.connect()

    def send_peers_to(self, peer: blockchain_rpc.Peer,
                      include_self: bool = True):
        """
        Sends send_peers request to a given peer, effectively broadcasting
        the list of currently known peers.
        """
        peers = list(self._known_peers)
        if include_self:
            peers.append(self._this_node)
        return peer.send_peers(peers)

    def recv_peers_from(self, peer: blockchain_rpc.Peer):
        """
         Sends get_peers request to a given peer recursively, accepting a list
         of peers currently known to that peer. Then send the same request
         to every peer in the list recursively. Discovers its's peer
         neighborhood.
        """

        is_connected = peer.connect()
        if not is_connected:
            return False

        console.debug("> get_peers from {:}".format(peer))

        # Receve the initial list
        rcvd_peers = peer.get_peers()
        peer_queue = Queue()

        for rcvd_peer in rcvd_peers:
            if not self.is_known_peer(rcvd_peer):
                peer_queue.put(rcvd_peer)

        # Explore the initial list recursively
        while not peer_queue.empty():
            rcvd_peer = peer_queue.get()
            self.maybe_add_peer(rcvd_peer)
            rcvd_peers = rcvd_peer.get_peers()
            for rcvd_peer in rcvd_peers:
                if not self.is_known_peer(rcvd_peer):
                    peer_queue.put(rcvd_peer)

        return True

    def discover_peers(self):
        """
        Run peer discovery and then schedule it to run periodically.
        Peer discovery consists of requesting known peers from all known peers.
        The initial peer discovery relies on a hardcoded list of initial peers,
        including, possibly, DNS-seeder nodes.
        """

        if self._config.peer_discovery_interval >= 0:
            console.debug("> discovering peers")

            with self._known_peers_lock:
                known_peers = set(self._known_peers)

            for peer in known_peers:
                self.recv_peers_from(peer)

            self.schedule_peer_discovery()

    def schedule_peer_discovery(self):
        """
        Schedules peer discovery on a separate thread
        """
        if self._config.peer_discovery_interval > 0:
            threading.Timer(
                self._config.peer_discovery_interval,
                function=self.discover_peers
            ).start()

    def share_peers(self):
        """
        Run peer sharing and then schedule it to run periodically.
        Peer sharing consist of sending all known peers to all known peers.
        """

        if self._config.peer_sharing_interval >= 0:
            console.debug("> sharing peers")

            with self._known_peers_lock:
                known_peers = set(self._known_peers)

            for peer in known_peers:
                self.send_peers_to(peer)

            self.schedule_peer_sharing()

    def schedule_peer_sharing(self):
        """
        Schedules peer sharing on a separate thread
        """
        if self._config.peer_sharing_interval > 0:
            threading.Timer(
                self._config.peer_sharing_interval,
                function=self.share_peers
            ).start()

    def is_known_peer(self, peer: blockchain_rpc.Peer) -> bool:
        """
        Verifies if a given peer is already known to us
        """

        with self._known_peers_lock:
            is_known = peer in list(self._known_peers)

        return (peer == self._this_node) or is_known

    def ping(self, ping, __):
        """
        RPC server handler triggered on `ping` RPC call.
        Replies with a `pong` reply. Ping-pong protocol is used to verify
        connection state between nodes.
        """
        return service.messages.Pong(message=ping.message)

    def get_peers(self, _, __):
        """
        Server handler that sends known peers in respond to `get_peers` request.
        """

        with self._known_peers_lock:
            known_peers = list(self._known_peers)

        console.debug("< req: get_peers")
        for peer in known_peers:
            console.debug("> sent peer: {:}".format(peer))
            yield peer.to_proto()

    def send_peers(self, peers, __):
        """
        Server handler that accepts peers on `send_peers` request.
        """
        console.debug("< req: send_peers")
        for peer in peers:
            peer = blockchain_rpc.Peer.from_proto(peer)
            console.debug("> rcvd peer: {:}".format(peer))
            self.maybe_add_peer(peer)

        return service.messages.Empty()

    def get_transactions(self, _, __):
        """
        RPC server handler triggered on get_transactions RPC call.
        Generic node does not handle this call (sends back an empty list).
        """
        yield from []

    def send_transactions(self, transactions: Iterable, _):
        """
        RPC server handler triggered on send_transactions RPC call.
        Generic node does not handle this call (ignores the input).
        """
        return service.messages.Empty()

    def get_blocks(self, _, __):
        """
        RPC server handler triggered on get_blocks RPC call.
        Generic node does not handle this call (sends back an empty list).
        """
        yield from []

    def send_blocks(self, blocks: Iterable, _):
        """
        RPC server handler triggered on send_blocks RPC call.
        Generic node does not handle this call (ignores the input).
        """
        return service.messages.Empty()
