#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


class Seeder:
    def __init__(self, host, port, stub):
        self._host = host
        self._port = port
        self._stub = stub

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def stub(self):
        return self._stub

    def __str__(self):
        return "{:}:{:}".format(self._host, self._port)

    def __repr__(self):
        return self.__str__()
