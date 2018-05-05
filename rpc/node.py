#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import threading
from threading import Lock
from concurrent import futures
from queue import Queue

import grpc

from rpc import Peer, Service
from utils import wait_forever, console

service = Service()


class BlockchainNode(service.Servicer):
    def __init__(self, host, port, known_peers, max_workers=5):
        """
        Base class for servers that implement blockchain service

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(BlockchainNode, self).__init__()
        self._host = host
        self._port = int(port)
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers))
        service.add_service(self, self._server)
        self._server.add_insecure_port("{:}:{:}".format(host, port))

        self._address = 0
        self._this_node = Peer(host=host, port=port)

        self._known_peers = set(known_peers)
        self._lock = Lock()

        self.discover_peers()
        self.share_peers()

    def _log(self, *args):
        console.log("{:}:{:5d} | ".format(self._host, self._port), *args)

    def start(self):
        """
        Starts the server
        """
        self._server.start()
        self._log("Listening on port {:}".format(self._port))

    def stop(self):
        """
        Stops the server immediately
        """
        self._server.stop(grace=0)

    def listen(self):
        """
        Listens for incoming messages until ^C
        """

        self.start()

        try:
            wait_forever()
        except KeyboardInterrupt:
            self.stop()

    def peer_iterator(self, include_self: bool = True):
        peers = [p.to_proto() for p in self._known_peers]

        if include_self:
            peers.append(self._this_node.to_proto())

        for peer in peers:
            yield peer

    def send_peers_to(self, peer: Peer, include_self: bool = True):
        self._log("> send_peers")
        peer.stub.send_peers(self.peer_iterator(include_self))

    def recv_peers_from(self, peer: Peer):
        self._log("> get_peers from {:}".format(peer))

        if not peer.is_connected:
            return False

        rcvd_peers = peer.stub.get_peers(service.messages.Empty())
        peer_q = Queue()

        for rcvd_peer in rcvd_peers:
            peer = Peer.from_proto(rcvd_peer)
            if not self.is_known_peer(peer):
                peer_q.put(peer)

        while not peer_q.empty():
            rcvd_peer = peer_q.get()

            if self.is_known_peer(peer):
                continue

            is_connected = rcvd_peer.connect()
            if not is_connected:
                continue

            self._log("> add  peer:  {:}".format(peer))
            self._known_peers.add(rcvd_peer)

            rcvd_peers = rcvd_peer.stub.get_peers(service.messages.Empty())
            for rcvd_peer in rcvd_peers:
                peer = Peer.from_proto(rcvd_peer)
                if not self.is_known_peer(peer):
                    peer_q.put(peer)

        return True

    def discover_peers(self):
        self._log("> discovering peers")

        self._lock.acquire()
        known_peers = set(self._known_peers)
        self._lock.release()

        for peer in known_peers:
            is_connected = peer.connect()

            if not is_connected:
                continue

            self.recv_peers_from(peer)

        threading.Timer(3, self.discover_peers).start()

    def share_peers(self):
        self._log("> sharing peers")

        self._lock.acquire()
        known_peers = set(self._known_peers)
        self._lock.release()

        for peer in known_peers:
            is_connected = peer.connect()

            if not is_connected:
                continue

            self.send_peers_to(peer)

        threading.Timer(3, self.share_peers).start()

    def is_known_peer(self, peer: Peer) -> bool:
        return (peer == self._this_node) or (peer in self._known_peers)

    def ping(self, ping, context):
        return service.messages.Pong(message=ping.message)

    def get_peers(self, _, __):
        """
        Server handler that sends known peers in respond to `get_peers` request
        """
        self._log("< req: get_peers")
        for peer in self.peer_iterator(include_self=False):
            self._log("> sent peer: {:}".format(Peer.from_proto(peer)))
            yield peer

    def send_peers(self, peers, __):
        """
        Server handler that accepts peers on `send_peers` request
        """
        self._log("< req: send_peers")
        for peer in peers:
            peer = Peer.from_proto(peer)
            self._log("> rcvd peer:  {:}".format(peer))

            if self.is_known_peer(peer):
                continue

            self._log("> add  peer:  {:}".format(peer))
            self._known_peers.add(peer)

        return service.messages.Empty()
