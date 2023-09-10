"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

from unittest import TestCase

from termkit.core import Termkit


class TestCore(TestCase):
    def test_name(self):
        self.assertEqual("app-name", Termkit("app-name").name)

    def test_call(self):
        app = Termkit("test")
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            app()

        self.assertEqual("Hello World\n", stdout.getvalue())

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
