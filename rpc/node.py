#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import threading
from threading import Thread, Lock
from concurrent import futures
from queue import Queue
from typing import Iterable

import grpc

from blockchain import Block, Transaction
from rpc import Peer, Service
from utils import wait_forever, console

service = Service()


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
        self._this_node = Peer(host=config.host, port=config.port)

        self._known_peers = set()
        self._known_peers_lock = Lock()

        for peer in config.known_peers:
            self.maybe_add_peer(peer)

        self.schedule_peer_discovery(config)
        self.schedule_peer_sharing(config)

    def _log(self, *args, verbosity=console.Verbosity.info):
        if self._config.verbosity >= verbosity:
            console.log(*args, fill=64)

    def log_error(self, *args):
        self._log(*args, verbosity=console.Verbosity.error)

    def log_warning(self, *args):
        self._log(*args, verbosity=console.Verbosity.warning)

    def log_info(self, *args):
        self._log(*args, verbosity=console.Verbosity.info)

    def log_debug(self, *args):
        self._log(*args, verbosity=console.Verbosity.debug)

    def start(self):
        """
        Starts the RPC server
        """
        self._server.start()
        self.log_info("Listening on port {:}".format(self._port))

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

    def maybe_add_peer(self, peer: Peer):
        if self.is_known_peer(peer):
            return False

        self.log_info("> add  peer:  {:}".format(peer))
        self._known_peers_lock.acquire()
        self._known_peers.add(peer)
        self._known_peers_lock.release()

        return peer.connect()

    def peer_iterator(self, include_self: bool = True):
        """
        Yields an iterator over known peers
        """

        known_peers = list(self._known_peers)

        peers = [peer.to_proto() for peer in known_peers]

        if include_self:
            peers.append(self._this_node.to_proto())

        for peer in peers:
            yield peer

    def send_peers_to(self, peer: Peer, include_self: bool = True):
        """
        Sends send_peers request to a given peer, effectively broadcasting
        the list of currently known peers.
        """

        # Possibly re-connect
        is_connected = peer.connect()
        if not is_connected:
            return False

        self.log_debug("> send_peers to {:}".format(peer))
        peer.stub.send_peers(self.peer_iterator(include_self))
        return True

    def recv_peers_from(self, peer: Peer):
        """
         Sends get_peers request to a given peer recursively, accepting a list
         of peers currently known to that peer. Then send the same request
         to every peer in the list recursively. Discovers its's peer
         neighborhood.
        """

        # Possibly re-connect
        is_connected = peer.connect()
        if not is_connected:
            return False

        self.log_debug("> get_peers from {:}".format(peer))

        # Receve the initial list
        rcvd_peers = peer.stub.get_peers(service.messages.Empty())
        peer_q = Queue()

        for rcvd_peer in rcvd_peers:
            peer = Peer.from_proto(rcvd_peer)
            if not self.is_known_peer(peer):
                peer_q.put(peer)

        # Explore the initial list recursively
        while not peer_q.empty():
            rcvd_peer = peer_q.get()

            is_connected = self.maybe_add_peer(rcvd_peer)

            if not is_connected:
                continue

            rcvd_peers = rcvd_peer.stub.get_peers(service.messages.Empty())
            for rcvd_peer in rcvd_peers:
                peer = Peer.from_proto(rcvd_peer)
                if not self.is_known_peer(peer):
                    peer_q.put(peer)

        return True

    def discover_peers(self, config):
        """
        Run peer discovery and then schedule it to run periodically.
        Peer discovery consists of requesting known peers from all known peers.
        The initial peer discovery relies on a hardcoded list of initial peers,
        including, possibly, DNS-seeder nodes.
        """

        if config.peer_discovery_interval >= 0:
            self.log_debug("> discovering peers")

            self._known_peers_lock.acquire()
            known_peers = set(self._known_peers)
            self._known_peers_lock.release()

            for peer in known_peers:
                is_connected = peer.connect()

                if not is_connected:
                    continue

                self.recv_peers_from(peer)

            self.schedule_peer_discovery(config)

    def schedule_peer_discovery(self, config):
        """
        Schedules peer discovery on a separate thread
        """
        if config.peer_discovery_interval > 0:
            threading.Timer(
                config.peer_discovery_interval,
                function=self.discover_peers,
                args=[config]
            ).start()

    def share_peers(self, config):
        """
        Run peer sharing and then schedule it to run periodically.
        Peer sharing consist of sending all known peers to all known peers.
        """

        if config.peer_sharing_interval >= 0:
            self.log_debug("> sharing peers")

            self._known_peers_lock.acquire()
            known_peers = set(self._known_peers)
            self._known_peers_lock.release()

            for peer in known_peers:
                is_connected = peer.connect()

                if not is_connected:
                    continue

                self.send_peers_to(peer)

            self.schedule_peer_sharing(config)

    def schedule_peer_sharing(self, config):
        """
        Schedules peer sharing on a separate thread
        """
        if config.peer_sharing_interval > 0:
            threading.Timer(
                config.peer_sharing_interval,
                function=self.share_peers,
                args=[config]
            ).start()

    def is_known_peer(self, peer: Peer) -> bool:
        """
        Verifies if a given peer is already known to us
        """

        self._known_peers_lock.acquire()
        is_known = peer in self._known_peers
        self._known_peers_lock.release()
        return (peer == self._this_node) or is_known

    def ping(self, ping, context):
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
        self.log_debug("< req: get_peers")
        for peer in self.peer_iterator(include_self=False):
            self.log_debug("> sent peer: {:}".format(Peer.from_proto(peer)))
            yield peer

    def send_peers(self, peers, __):
        """
        Server handler that accepts peers on `send_peers` request.
        """
        self.log_debug("< req: send_peers")
        for peer in peers:
            peer = Peer.from_proto(peer)
            self.log_debug("> rcvd peer: {:}".format(peer))
            self.maybe_add_peer(peer)

        return service.messages.Empty()

    def get_transactions(self, _, __):
        """
        RPC server handler triggered on get_transactions RPC call.
        Generic node does not handle this call (sends back an empty list).
        """
        yield from []

    def send_transactions(self, transactions: Iterable[Transaction], _):
        """
        RPC server handler triggered on send_transactions RPC call.
        Generic node does not handle this call (ignores the input).
        """
        return self._messages.Empty()

    def get_blocks(self, _, __):
        """
        RPC server handler triggered on get_blocks RPC call.
        Generic node does not handle this call (sends back an empty list).
        """
        yield from []

    def send_blocks(self, blocks: Iterable[Block], _):
        """
        RPC server handler triggered on send_blocks RPC call.
        Generic node does not handle this call (ignores the input).
        """
        return self._messages.Empty()
