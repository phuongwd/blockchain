#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from utils.datetime import datetime


def _console_write_with_datetime(*args, **kwargs):
    f = kwargs["f"]

    # print args into a string
    s = "{} | ".format(datetime())
    for arg in args:
        s += '{}'.format(arg)

    # fill with spaces up to requested size
    fill = kwargs["fill"]
    fill -= len(s)
    if fill > 0:
        s += " " * fill

    # write out to file and flush
    f.write(s)
    f.write("\n")
    f.flush()


def log(*args, fill=0):
    return _console_write_with_datetime(*args, f=sys.stdout, fill=fill)


def error(*args, fill=0):
    return _console_write_with_datetime(*args, f=sys.stderr, fill=fill)
