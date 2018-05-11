#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def favor_higher_fees(tx1, tx2):
    return tx1.fee > tx2.fee
