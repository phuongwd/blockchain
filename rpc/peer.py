#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import grpc

from rpc import Service
from utils import random_string

service = Service()


class Peer:
    def __init__(self, host, port):
        self._host = host
        self._port = int(port)
        self._address = None
        self._channel = None
        self._stub = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def address(self):
        return self._address

    @property
    def stub(self):
        return self._stub

    @property
    def is_connected(self):
        if self._stub is None:
            return False

        try:
            message = random_string(8)
            res = self._stub.ping(service.messages.Ping(message=message))
            if res is None or res.message != message:
                return False
        except:
            self._channel = None
            self._stub = None
            return False

        return True

    def __eq__(self, other):
        return self.host == other.host \
               and self.port == other.port \
               and self.address == other.address

    def __lt__(self, other):
        return self.host < other.host \
               or self.port < other.port \
               or self.address < other.address

    def __str__(self):
        s = "{:}:{:}".format(self.host, self.port)

        if self.address is not None:
            s += "/{:}".format(self.address)

        return s

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.__str__().__hash__()

    @staticmethod
    def from_proto(peer_proto):
        return Peer(host=peer_proto.host, port=peer_proto.port)

    def to_proto(self):
        return service.messages.Node(
            host=self.host,
            port=self.port,
            address=self.address
        )

    def connect(self):
        if self.is_connected:
            return True

        self._channel = grpc.insecure_channel(
            "{:}:{:}".format(self.host, self.port))
        self._stub = service.Stub(self._channel)

        return self.is_connected
