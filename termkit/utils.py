"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import copy

__RESERVED_PREFIXES__ = ["_TERMKIT_"]

import typing


def filter_args(ns: argparse.Namespace) -> typing.Dict:
    out = copy.copy(ns)
    for arg in ns.__dict__.keys():
        for reserved_prefix in __RESERVED_PREFIXES__:
            if reserved_prefix in arg:
                delattr(out, arg)
    return out.__dict__
