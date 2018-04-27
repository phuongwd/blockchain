#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
from concurrent import futures
from threading import Lock
from typing import Iterable

import grpc
import protol
import dotenv

from rpc import Peer, Seeder, format_peer
from utils import wait_forever, console

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV_PATH = os.path.join(CURRENT_PATH, "..", ".env")
dotenv.load_dotenv(dotenv_path=ENV_PATH)

PROTO_PATH = os.path.join(CURRENT_PATH, "..", "protos", "blockchain.proto")
SERVICE_NAME = os.getenv("SERVICE_NAME") or "Blockchain"


def load_service(proto_path, service_name):
    """
    Loads service definition from protobuf file and performs gRPC service
    initialization.

    :param proto_path: Path to protobuf file with service definition
    :param service_name: Service name. Should match name of `service` in proto

    :return: Returns tuple (messages, Servicer, add_service, Stub), where:
        `messages` is an object that contains message definitions
        `Servicer` is a class type to be used as a base class for servers
        `add_service` is a function that adds server implementations to
    the service
        `Stub` is a class type to be used by clients
    """
    messages, service = protol.load(proto_path)
    Servicer = getattr(service, service_name + "Servicer")
    add_service = getattr(service, "add_" + service_name + "Servicer_to_server")
    Stub = getattr(service, service_name + "Stub")
    return messages, Servicer, add_service, Stub


messages, Servicer, add_service, Stub = load_service(PROTO_PATH, SERVICE_NAME)


class BlockchainNode(Servicer):
    def __init__(self, host, port, max_workers=5):
        """
        Base class for servers that implement blockchain service

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(Servicer, self).__init__()
        self._host = host
        self._port = port
        self._messages = messages
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers))
        add_service(self, self._server)
        self._server.add_insecure_port("{:}:{:}".format(host, port))
        self._print_lock = Lock()

        self._address = 0
        self._this_node = self._messages.Node(
            host=host, port=port, address=self._address
        )

        self._known_seeders = []
        self._known_peers = []

    def _log(self, *args):
        self._print_lock.acquire()
        console.log("{:}:{:5d} | ".format(self._host, self._port), *args)
        self._print_lock.release()

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

    def peer_iterator(self, peers: Iterable[Peer]):
        for peer in peers:
            yield peer

    def send_known_peers_to(self, peer: Peer, include_self: bool):
        known_peers = [
            self._messages.Node(
                host=p.host,
                port=p.port,
                address=p.address
            )

            for p in self._known_peers
        ]

        if include_self:
            known_peers += [self._this_node]

        if len(known_peers) > 0:
            peer.stub.send_peers(
                self.peer_iterator(known_peers)
            )

    def connect_to(self, host: str, port: int):
        """
        Connects as a gRPC client to a given gRPC server

        :param host: Server host
        :param port: Server port

        :return: Stub of the service connected to the specified server
        """
        self._log("Connecting to: {:}:{:}".format(host, port))
        return Stub(grpc.insecure_channel("{:}:{:}".format(host, port)))

    def add_peer(self, host, port, address):
        stub = self.connect_to(host, port)
        peer = Peer(host, port, address, stub)
        self._log("Adding peer: {:}".format(peer))
        self._known_peers.append(peer)
        return peer

    def add_seeder(self, host, port):
        stub = self.connect_to(host, port)
        seeder = Seeder(host, port, stub)
        self._log("Adding seeder: {:}".format(seeder))
        self._known_seeders.append(seeder)
        return seeder

    def is_known_peer(self, peer):
        # self._log("is_known_peer _this_node: {:}:{:}/{:}".format(
        #     self._this_node.host, self._this_node.port, self._this_node.address
        # ))
        #
        # self._log("is_known_peer peer: {:}:{:}/{:}".format(
        #     peer.host, peer.port, peer.address
        # ))
        #
        # self._log("is_known_peer equal: {:}:{:}/{:}".format(
        #     peer.host == self._this_node.host,
        #     peer.port == self._this_node.port,
        #     peer.address == self._this_node.address
        # ))

        return (peer == self._this_node) or (peer in self._known_peers)

    def get_peers(self, request, context):
        """
        Server handler that sends known peers in respond to `get_peers` request
        """
        self._log("Received  get_peers request")
        for peer in self._known_peers:
            yield self._messages.Node(
                host=peer.host,
                port=peer.port,
                address=peer.address
            )

    def send_peers(self, peers, context):
        """
        Server handler that accepts peers on `send_peers` request
        """
        self._log("Received send_peers request")
        for peer in peers:
            self._log("Received peer: {:}".format(format_peer(peer)))

            if not self.is_known_peer(peer):
                peer = self.add_peer(peer.host, peer.port, peer.address)

        return self._messages.Empty()
