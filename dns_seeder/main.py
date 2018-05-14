#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from blockchain_rpc import NodeBase
from utils import dict_to_namedtuple, Verbosity
from utils.console import Console

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = int(os.getenv("DNS_SEED_PORT")) or 54152


def main():
    host = DNS_SEED_HOST
    port = DNS_SEED_PORT

    config = dict_to_namedtuple({
        "host": host,
        "port": port,
        "mining": False,
        "gen_transactions": False,
        "known_peers": [],
        "peer_discovery_interval": 3,
        "peer_sharing_interval": 3,
        "max_workers": 3,
        "key_path": "../.data/{:}_{:}/ecdsa_secp256k1.pem".format(host, port),
    })

    # Console.verbosity = Verbosity.debug

    dns_seeder = NodeBase(config)
    dns_seeder.listen()


if __name__ == "__main__":
    main()
