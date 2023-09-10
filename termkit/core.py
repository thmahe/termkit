"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import inspect
import os
import sys
import typing


class Termkit:
    def __init__(self, name: str = os.path.basename(sys.argv[0])):
        self._childs = []
        self.name = name

    def add(self, app_or_command: typing.Union[Termkit, typing.Callable]):
        if isinstance(app_or_command, Termkit):
            self._childs.append(app_or_command)
        elif inspect.isfunction(app_or_command):
            self._childs.append(app_or_command)
        else:
            raise TypeError(f"Cannot add object of type {type(app_or_command)} to termkit.Termkit.")

    def __call__(self, *args, **kwargs):
        print("Hello World")
