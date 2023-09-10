"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import inspect
import os
import sys


class Termkit:
    def __init__(self, name: str = os.path.basename(sys.argv[0])):
        self.name = name

    def __call__(self, *args, **kwargs):
        print('Hello World')
