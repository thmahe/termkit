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

    def test_add(self):
        def dummy_command():
            ...

        app = Termkit()
        sub_app = Termkit()
        app.add(sub_app)
        app.add(dummy_command)

        class Complex:
            ...

        with self.assertRaises(TypeError) as e:
            app.add(Complex)
        self.assertEqual(
            ("Cannot add object of type <class 'type'> to termkit.Termkit.",),
            e.exception.args,
        )
