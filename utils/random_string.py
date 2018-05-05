#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import random
import string


def random_string(length):
    return ''.join([
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    ])
