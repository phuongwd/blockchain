#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

import protol
import dotenv

import utils

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

ENV_PATH = os.path.join(CURRENT_PATH, "..", ".env")
dotenv.load_dotenv(dotenv_path=ENV_PATH)

PROTO_PATH = os.path.join(CURRENT_PATH, "..", "protos", "blockchain.proto")
SERVICE_NAME = os.getenv("SERVICE_NAME") or "Blockchain"
HASH_FUNCTION = os.getenv("HASH_FUNCTION") or "sha256"


class Service:
    def __init__(self):
        self.messages, self.service = protol.load(PROTO_PATH)
        self.Servicer = getattr(self.service, SERVICE_NAME + "Servicer")
        self.add_service = getattr(
            self.service, "add_" + SERVICE_NAME + "Servicer_to_server")
        self.Stub = getattr(self.service, SERVICE_NAME + "Stub")
        self.hash_f = getattr(utils.hash_functions, "sha256")
