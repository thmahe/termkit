"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import inspect
import os
import sys
import typing


class _Command:
    def __init__(self, callback: typing.Callable, name: str = None):
        self.callback = callback
        if name is None:
            name = callback.__name__
        self.name = name


class Termkit:
    def __init__(self, name: str = os.path.basename(sys.argv[0])):
        self._childs = []
        self.name = name

    @property
    def _child_names(self):
        return [c.name for c in self._childs]

    def add(self, app_or_command: typing.Union[Termkit, typing.Callable], name: typing.Optional[str] = None):
        if isinstance(app_or_command, Termkit):
            child = app_or_command
        elif inspect.isfunction(app_or_command):
            child = _Command(app_or_command, name)
        else:
            raise TypeError(f"Cannot add object of type '{type(app_or_command)}' to Termkit application.")

        if name is not None:
            child.name = name

        if child.name in self._child_names:
            raise ValueError(f"Name '{child.name}' already taken in '{self.name}' application.")

        self._childs.append(child)

    def command(self, name: str = None):
        def decorator(func: typing.Callable):
            self.add(func, name)
            return func

        return decorator

    def __call__(self, *args, **kwargs):
        print("Hello World")
