#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import time


def wait_forever():
    """
    Makes caller thread to wait forever
    """
    while True:
        time.sleep(2 ** 63)
