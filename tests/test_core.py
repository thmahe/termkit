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
