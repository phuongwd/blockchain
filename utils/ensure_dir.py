#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os


def ensure_dir(dir_path):
    """ Ensures existence of a directory """
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise IOError(
                "Path exists but is not a directory: '{:}'".format(dir_path)
            )
        else:
            os.makedirs(dir_path)
