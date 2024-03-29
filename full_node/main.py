#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import sys

from blockchain_rpc import Peer
from blockchain_rpc.node_full import NodeFull
from utils import dict_to_namedtuple, Verbosity
from utils.console import Console

HOST = "localhost"

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = os.getenv("DNS_SEED_PORT") or 54152

VIEWER_HOST = "localhost"
VIEWER_PORT = os.getenv("VIEWER_PORT") or 12345


def main():
    host_port = sys.argv[1]
    host, port = host_port.split(":")

    config = dict_to_namedtuple({
        "host": host or "localhost",
        "port": int(port),
        "mining": True,
        "gen_transactions": True,
        "known_peers": [
            Peer(host=DNS_SEED_HOST, port=DNS_SEED_PORT),
            Peer(host=VIEWER_HOST, port=VIEWER_PORT)
        ],
        "peer_discovery_interval": 5,
        "peer_sharing_interval": 5,
        "transaction_discovery_interval": 5,
        "transaction_sharing_interval": 5,
        "block_discovery_interval": 5,
        "block_sharing_interval": 5,
        "max_workers": 3,
        "difficulty": 10,
        "mining_throttle_ms": 10,
        "key_path": "../.data/{:}_{:}/ecdsa_secp256k1.pem".format(host, port)
    })

    # Console.verbosity = Verbosity.debug

    node = NodeFull(config)
    node.listen()


if __name__ == "__main__":
    main()
