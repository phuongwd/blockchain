#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from collections import namedtuple


def dict_to_namedtuple(d, name='GenericDict'):
    return namedtuple(name, d.keys())(**d)
