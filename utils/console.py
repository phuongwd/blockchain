#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

from utils.datetime import datetime


def _console_write_with_datetime(*args, **kwargs):
    f = kwargs["f"]
    f.write("{} | ".format(datetime()))
    for arg in args:
        f.write('{}'.format(arg))
    f.write("\n")
    f.flush()


def log(*args):
    return _console_write_with_datetime(*args, f=sys.stdout)


def error(*args):
    return _console_write_with_datetime(*args, f=sys.stderr)
