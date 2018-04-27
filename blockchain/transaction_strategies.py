#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from blockchain import Transaction


def favor_higher_fees(tx1: Transaction, tx2: Transaction) -> bool:
    return tx1.fee > tx2.fee
