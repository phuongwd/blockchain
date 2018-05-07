#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from utils import dict_to_namedtuple

constants = dict_to_namedtuple({
    "BLOCK_COINBASE_AMOUNT": 25,
    "BLOCK_MAX_TRANSACTIONS": 5,
    "TRANSACTION_MAX_INPUTS": 5,
    "TRANSACTION_MAX_OUTPUTS": 5
})
