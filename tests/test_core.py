"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import textwrap
from unittest import TestCase

from termkit.core import Termkit
from termkit.tests import TermkitRunner


class TestCore(TestCase):
    def test_name(self):
        self.assertEqual("app-name", Termkit("app-name").name)

    def test_add_termkit_sub_app(self):
        app = Termkit()
        app2 = Termkit()
        app.add(app2)

    def test_add_command(self):
        app = Termkit("app-name")

        def command():
            ...

        app.add(command)
        app.add(command, name="command-2")

        with self.assertRaises(ValueError) as e:
            app.add(command, name="command-2")
        self.assertEqual(("Name 'command-2' already taken in 'app-name' application.",), e.exception.args)

    def test_add_termkit_command_with_decorator(self):
        app = Termkit("app-name")

        @app.command()
        def func_name():
            ...

        self.assertEqual(["func_name"], app._child_names)

    def test_add_command_with_wrong_type(self):
        app = Termkit()

        class Complex:
            ...

        with self.assertRaises(TypeError) as e:
            app.add(Complex)
        self.assertEqual(
            ("Cannot add object of type '<class 'type'>' to Termkit application.",),
            e.exception.args,
        )

    def test_standalone_app_helper(self):
        app = Termkit("my-app")
        runner = TermkitRunner(app)

        @app.command()
        @app.command("command-2")
        def command():
            ...

        runner.run("--help")

        stdout = textwrap.dedent(
            """\
        usage: my-app [-h] COMMAND ...

        Options:
          -h, --help  show this help message and exit

        Commands:
          command-2
          command
        """
        )

        self.assertEqual(stdout, runner.captured_output)

        runner.run("command", "--help")

        stdout = textwrap.dedent(
            """\
        usage: my-app command [-h]

        Options:
          -h, --help  show this help message and exit
        """
        )

        self.assertEqual(stdout, runner.captured_output)
        self.assertEqual(0, runner.exit_code)
        self.assertEqual(SystemExit, type(runner.exception))

    def test_sub_app_helper(self):
        app = Termkit("my-app")
        second_app = Termkit("sub-app", description="First line help\nSecond line help")
        app.add(second_app)

        @second_app.command()
        def func():
            """
            First line from docstring
            Second line from docstring
            """
            ...

        runner = TermkitRunner(app)

        runner.run("--help")

        stdout = textwrap.dedent(
            """\
        usage: my-app [-h] COMMAND ...

        Options:
          -h, --help  show this help message and exit

        Commands:
          sub-app .... First line help
        """
        )

        self.assertEqual(stdout, runner.captured_output)

        runner.run("sub-app", "--help")

        stdout = textwrap.dedent(
            """\
        usage: my-app sub-app [-h] COMMAND ...

        First line help
        Second line help

        Options:
          -h, --help  show this help message and exit

        Commands:
          func .... First line from docstring
        """
        )

        self.assertEqual(stdout, runner.captured_output)
        self.assertEqual(0, runner.exit_code)
        self.assertEqual(SystemExit, type(runner.exception))

        runner.run("sub-app", "func", "--help")

        stdout = textwrap.dedent(
            """\
        usage: my-app sub-app func [-h]

        First line from docstring
        Second line from docstring

        Options:
          -h, --help  show this help message and exit
        """
        )

        self.assertEqual(stdout, runner.captured_output)
        self.assertEqual(0, runner.exit_code)
        self.assertEqual(SystemExit, type(runner.exception))
