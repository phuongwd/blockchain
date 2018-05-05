#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import sys

from full_node import FullNode
from rpc import Peer
from utils import dict_to_namedtuple

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
        "known_peers": [
            Peer(host=DNS_SEED_HOST, port=DNS_SEED_PORT),
            Peer(host=VIEWER_HOST, port=VIEWER_PORT),
        ],
        "peer_discovery_interval": 3,
        "peer_sharing_interval": 3,
        "max_workers": 3
    })

    node = FullNode(config)
    node.listen()


if __name__ == "__main__":
    main()
