#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
from concurrent import futures

import grpc
import protol
import dotenv

from utils import wait_forever

ENV_PATH = os.path.join('..', '.env')
dotenv.load_dotenv(dotenv_path=ENV_PATH)

PROTO_PATH = os.path.join('..', 'protos', 'blockchain.proto')
SERVICE_NAME = os.getenv("SERVICE_NAME") or 'BC'


def load_service(proto_path, service_name):
    """
    Loads service definition from protobuf file and performs gRPC service
    initialization.

    :param proto_path: Path to protobuf file with service definition
    :param service_name: Service name. Should match name of `service` in proto

    :return: Returns tuple (messages, Servicer, add_service), where:
        `messages` is an object that contains message definitions
        `Servicer` is a servicer object to be used as a base class for servers
        `add_service` is a function that adds server implementations to
    the service
    """
    messages, service = protol.load(proto_path)
    Servicer = getattr(service, service_name + 'Servicer')
    add_service = getattr(service, 'add_' + service_name + 'Servicer_to_server')
    return messages, Servicer, add_service


messages, Servicer, add_service = load_service(PROTO_PATH, SERVICE_NAME)


class BlockchainServer(Servicer):
    def __init__(self, host, port, max_workers=5):
        """
        Base class for servers that implement blockchain service

        :param host: Host on which a server will be listening
        :param port: Port on which a server will be listening
        :param max_workers: Maximium number of worker processess to spawn
        """
        super(Servicer, self).__init__()
        self._port = port
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers))
        add_service(self, self._server)
        self._server.add_insecure_port('{:}:{:}'.format(host, port))

    def start(self):
        """
        Starts the server
        """
        self._server.start()

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
        print('Listening on port {:}'.format(self._port))

        try:
            wait_forever()
        except KeyboardInterrupt:
            self.stop()
