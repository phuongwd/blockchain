#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import sys

from blockchain_rpc import Peer, NodeFull
from utils import dict_to_namedtuple, Verbosity
from utils.console import Console

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = os.getenv("DNS_SEED_PORT") or 54152


def main():
    host_port = sys.argv[1]
    host, port = host_port.split(":")
    host = host or "localhost"
    port = int(port) or 5000

    config = dict_to_namedtuple({
        "host": host,
        "port": port,
        "mining": False,
        "gen_transactions": True,
        "known_peers": [
            Peer(host=DNS_SEED_HOST, port=DNS_SEED_PORT)
        ],
        "peer_discovery_interval": 5,
        "peer_sharing_interval": 5,
        "transaction_discovery_interval": 5,
        "transaction_sharing_interval": 5,
        "block_discovery_interval": 5,
        "block_sharing_interval": 5,
        "max_workers": 3,
        "key_path": "../.data/{:}_{:}/ecdsa_secp256k1.pem".format(host, port)
    })

    # Console.verbosity = Verbosity.debug

    node = NodeFull(config)
    node.listen()


if __name__ == "__main__":
    main()
