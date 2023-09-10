"""
Copyright 2023, Thomas Mahé <contact@tmahe.dev>
SPDX-License-Identifier: MIT
"""

import argparse


class TermkitParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._optionals.title = "Options"
        self._positionals.title = "Positionals"

        if kwargs.get("formatter_class", None) is None:
            self.formatter_class = argparse.RawTextHelpFormatter
