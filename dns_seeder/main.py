#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from dns_seeder import DNSSeeder

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = int(os.getenv("DNS_SEED_PORT")) or 54152


def main():
    dns_seeder = DNSSeeder(
        host=DNS_SEED_HOST,
        port=DNS_SEED_PORT,
        max_workers=3
    )

    dns_seeder.listen()


if __name__ == "__main__":
    main()
