"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse
import textwrap
from typing import Annotated
from unittest import TestCase

from termkit.arguments import Option, Positional
from termkit.core import Termkit
from termkit.parser import ArgumentHandler
from termkit.tests import TermkitRunner


class TestArgumentHandler(TestCase):
    def test__get_parameter_type(self):
        def func(param_1, param_2: int, param_3="test", param_4=10.8, param_5=True, param_6: int = 10.8):
            ...

        a = ArgumentHandler(parser=argparse.ArgumentParser(), func=func)

        self.assertEqual(str, a._get_parameter_type("param_1"))
        self.assertEqual(int, a._get_parameter_type("param_2"))
        self.assertEqual(str, a._get_parameter_type("param_3"))
        self.assertEqual(float, a._get_parameter_type("param_4"))
        self.assertEqual(bool, a._get_parameter_type("param_5"))
        self.assertEqual(int, a._get_parameter_type("param_6"))

    def test_implicit_positional(self):
        app = Termkit("app-name")

        @app.command()
        def func(name):
            ...

        runner = TermkitRunner(app)
        runner.run("func", "--help")

        output = textwrap.dedent(
            """\
        usage: app-name func [-h] name

        Positionals:
          name

        Options:
          -h, --help  Show this help message and exit
        """
        )

        self.assertEqual(output, runner.captured_output)

    def test_implicit_option(self):
        app = Termkit("app-name")

        @app.command()
        def func(value=10):
            ...

        runner = TermkitRunner(app)
        runner.run("func", "--help")

        output = textwrap.dedent(
            """\
        usage: app-name func [-h] [--value VALUE]

        Options:
          -h, --help     Show this help message and exit
          --value VALUE
        """
        )

        self.assertEqual(output, runner.captured_output)

    def test_explicit_positional(self):
        app = Termkit("app-name")

        @app.command()
        def func(value: Annotated[str, Positional()], value2: Annotated[str, Positional()]):
            """

            :param value:
            :param value2: With custom help
            :return:
            """
            ...

        runner = TermkitRunner(app)
        runner.run("func", "--help")

        output = textwrap.dedent(
            """\
        usage: app-name func [-h] value value2

        Positionals:
          value
          value2      With custom help

        Options:
          -h, --help  Show this help message and exit
        """
        )

        self.assertEqual(output, runner.captured_output)

    def test_explicit_option(self):
        app = Termkit("app-name")

        @app.command()
        def func(
            value: Annotated[str, Option("--value", "-v")],
            value2: Annotated[str, Option("-b", required=True, metavar="STR")],
        ):
            """

            :param value:
            :param value2: With custom help
            :return:
            """
            ...

        runner = TermkitRunner(app)
        runner.run("func", "--help")

        output = textwrap.dedent(
            """\
        usage: app-name func [-h] [-v VALUE] -b STR

        Options:
          -h, --help         Show this help message and exit
          -v, --value VALUE
          -b STR             With custom help
        """
        )

        self.assertEqual(output, runner.captured_output)

    def test_explicit_option_default(self):
        app = Termkit("app-name")

        @app.command()
        def func(
            value: Annotated[str, Option("--value", "-v")] = 10,
        ):
            """

            :param value:
            :param value2: With custom help
            :return:
            """
            print(value)

        runner = TermkitRunner(app)
        runner.run("func", "--value", "Hello")

        output = textwrap.dedent(
            """\
        Hello
        """
        )

        self.assertEqual(output, runner.captured_output)
