"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import typing
from abc import abstractmethod
from typing import Optional

from termkit.groups import _TermkitGroup, get_parser_from_group


class _TermkitArgument:
    _ignored_params = ["flags", "group"]

    @abstractmethod
    def _populate(self, parser: argparse.ArgumentParser, dest: str):
        ...

    @property
    def argparse_params(self):
        out = self.__dict__
        for item in self._ignored_params:
            if item in out.keys():
                del out[item]
        return out


class Positional(_TermkitArgument):
    def __init__(self, type: Optional[type] = str, help: Optional[str] = None, metavar: Optional[str] = None):
        self.type = type
        self.help = help
        self.metavar = metavar

    def _populate(self, parser: argparse.ArgumentParser, dest: str):
        parser.add_argument(dest, **self.argparse_params)


class Option(_TermkitArgument):
    def __init__(
        self,
        *flags: str,
        type: Optional[type] = str,
        help: Optional[str] = None,
        metavar: Optional[str] = None,
        required: bool = False,
        default: Optional[typing.Any] = None,
        group: Optional[_TermkitGroup] = None
    ):
        self.flags = flags
        self.type = type
        self.help = help
        self.metavar = metavar
        self.required = required
        self.default = default
        self.group = group

    def _populate(self, parser: argparse.ArgumentParser, dest: str):
        parser = get_parser_from_group(parser, self.group)
        parser.add_argument(*self.flags, **self.argparse_params, dest=dest)


class Flag(_TermkitArgument):
    _ignored_params = ["flags", "type", "group"]

    def __init__(
        self,
        *flags: str,
        help: Optional[str] = None,
        store: Optional[typing.Any] = True,
        group: Optional[_TermkitGroup] = None
    ):
        self.flags = flags
        self.type = None
        self.help = help
        self.group = group
        if store is True:
            self.action = "store_true"
        if store is False:
            self.action = "store_false"
        else:
            self.action = "store_const"
            self.const = store

    def _populate(self, parser: argparse.ArgumentParser, dest: str):
        parser = get_parser_from_group(parser, self.group)
        parser.add_argument(*self.flags, **self.argparse_params, dest=dest)
