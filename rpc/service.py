#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

import protol
import dotenv

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV_PATH = os.path.join(CURRENT_PATH, "..", ".env")
dotenv.load_dotenv(dotenv_path=ENV_PATH)

PROTO_PATH = os.path.join(CURRENT_PATH, "..", "protos", "blockchain.proto")
SERVICE_NAME = os.getenv("SERVICE_NAME") or "Blockchain"


class Service:
    def __init__(self):
        self.messages, self.service = protol.load(PROTO_PATH)
        self.Servicer = getattr(self.service, SERVICE_NAME + "Servicer")
        self.add_service = getattr(
            self.service, "add_" + SERVICE_NAME + "Servicer_to_server")
        self.Stub = getattr(self.service, SERVICE_NAME + "Stub")

# def load_service(proto_path, service_name):
#     """
#     Loads service definition from protobuf file and performs gRPC service
#     initialization.
#
#     :param proto_path: Path to protobuf file with service definition
#     :param service_name: Service name. Should match name of `service` in proto
#
#     :return: Returns tuple (messages, Servicer, add_service, Stub), where:
#         `messages` is an object that contains message definitions
#         `Servicer` is a class type to be used as a base class for servers
#         `add_service` is a function that adds server implementations to
#     the service
#         `Stub` is a class type to be used by clients
#     """
#     messages, service = protol.load(proto_path)
#     Servicer = getattr(service, service_name + "Servicer")
#     add_service = getattr(service,
#                           "add_" + service_name + "Servicer_to_server")
#     Stub = getattr(service, service_name + "Stub")
#     return messages, Servicer, add_service, Stub
