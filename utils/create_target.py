#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def create_target(num_bits, difficulty):
    return (2 << (num_bits - difficulty - 1)) - 1
