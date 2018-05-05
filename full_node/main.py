#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os
import sys

from full_node import FullNode
from rpc import Peer

HOST = "localhost"

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = os.getenv("DNS_SEED_PORT") or 54152

VIEWER_HOST = "localhost"
VIEWER_PORT = os.getenv("VIEWER_PORT") or 12345


def main():
    host_port = sys.argv[1]
    host, port = host_port.split(":")

    node = FullNode(
        host=host or "localhost",
        port=int(port),
        known_peers=[
            Peer(host=DNS_SEED_HOST, port=DNS_SEED_PORT),
            Peer(host=VIEWER_HOST, port=VIEWER_PORT),
        ],
        max_workers=3
    )

    node.listen()

if __name__ == "__main__":
    main()
