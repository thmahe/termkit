"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import abc
import argparse
import inspect
import os
import sys
import typing

from termkit.parser import TermkitParser


class _TermkitComponent:
    name: str
    help: str

    @property
    def single_line_help(self):
        return self.help.split("\n")[0]

    @abc.abstractmethod
    def _populate(self, parser: argparse.ArgumentParser):
        ...


class _Command(_TermkitComponent):
    def __init__(self, callback: typing.Callable, name: str = None):
        self.callback = callback
        if name is None:
            name = callback.__name__
        self.name = name

        self.help = inspect.getdoc(callback)
        if self.help is None:
            self.help = ""

    def _populate(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "_TERMKIT_CALLBACK", action="store_const", const=self.callback, help="CONST " + self.callback.__name__
        )


class Termkit(_TermkitComponent):
    def __init__(self, name: str = os.path.basename(sys.argv[0]), description: typing.Optional[str] = None):
        self._childs = []
        self._parser = TermkitParser(prog=name, description=description)
        self._populated = False

        self.name = name
        self.help = description if description is not None else ""

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

    def _populate(self, parser: argparse.ArgumentParser):
        if len(self._childs) > 0 and not self._populated:
            sub_parser = parser.add_subparsers(title="Commands", metavar="COMMAND")
            for child in self._childs:
                command_parser = sub_parser.add_parser(
                    name=child.name, help=child.single_line_help, description=child.help
                )
                child._populate(command_parser)
        self._populated = True

    def __call__(self, *args, **kwargs):
        self._populate(self._parser)
        self._parser.parse_args()
        sys.exit(0)
