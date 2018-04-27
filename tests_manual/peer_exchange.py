#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from dns_seeder import DNSSeeder
from full_node import FullNode
from utils import wait_forever

DNS_SEED_HOST = "localhost"
DNS_SEED_PORT = int(os.getenv("DNS_SEED_PORT")) or 54152

# from multiprocessing import Condition, Process


# class WaitForSeeder:
#     def __init__(self):
#         self._seeder_ready = False
#         self._cond = Condition()
#
#     def ready(self):
#         self._cond.acquire()
#         self._seeder_ready = True
#         self._cond.notify()
#         self._cond.release()
#
#     def wait(self):
#         self._cond.acquire()
#         while not self._seeder_ready:
#             self._cond.wait()
#         self._cond.release()
#
#
# def run_seeder(w):
#     dns_seeder = DNSSeeder(
#         host=DNS_SEED_HOST,
#         port=DNS_SEED_PORT,
#         max_workers=3
#     )
#
#     dns_seeder.start()
#     w.ready()
#     try:
#         wait_forever()
#     except KeyboardInterrupt:
#         return
#
#
# def run_full_node(port):



def main():
    dns_seeder = DNSSeeder(
        host=DNS_SEED_HOST,
        port=DNS_SEED_PORT,
        max_workers=3
    )

    dns_seeder.start()


    pid = os.fork()
    if pid == 0:
        node = FullNode(
            host="localhost",
            port=5000,
            seeders=[(DNS_SEED_HOST, DNS_SEED_PORT)],
            max_workers=3
        )

        node.listen()
        print("Node exits")

    # os.waitpid(pid)

    try:
        wait_forever()
    except KeyboardInterrupt:
        return

    print("Seeder exits")


    # full_node_threads = []
    # for i in range(2):
    #     t = Process(target=run_full_node, args=(5000 + i,))
    #     full_node_threads.append(t)
    #     t.start()
    #
    # seeder_thread.join()
    # for t in full_node_threads:
    #     t.join()

    # print("Exit")


if __name__ == "__main__":
    main()
