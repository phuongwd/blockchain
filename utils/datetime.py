#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from time import strftime


def datetime():
    return strftime("%Y-%m-%d %H:%M:%S")
