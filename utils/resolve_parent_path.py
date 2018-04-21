#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os


def resolve_parent_path(p):
    """
    Resolves absolute path of the parent directory of a given file or diretory

    :param p:   file or directory path to resolve
    :return:    absolute parent directory path
    """
    realpath = os.path.realpath(p)
    if os.path.isdir(realpath):
        return realpath

    return os.path.dirname(realpath)
