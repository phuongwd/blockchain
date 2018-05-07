#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from dns_seeder import DNSSeeder
from utils import dict_to_namedtuple, console

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = int(os.getenv("DNS_SEED_PORT")) or 54152


def main():
    config = dict_to_namedtuple({
        "host": DNS_SEED_HOST or "localhost",
        "port": DNS_SEED_PORT,
        "known_peers": [],
        "peer_discovery_interval": 3,
        "peer_sharing_interval": 3,
        "max_workers": 3,
        "verbosity": console.Verbosity.info
    })

    dns_seeder = DNSSeeder(config)
    dns_seeder.listen()


if __name__ == "__main__":
    main()
