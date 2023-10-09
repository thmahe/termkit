import getpass
import sys
from typing import Optional, Union


def ask(prompt: Optional[str] = None, confirm: Optional[bool] = False) -> Union[bool, str]:
    if confirm:
        if input(prompt + " [Y/n] ").lower() not in ["y", "yes"]:
            print("Aborted.", file=sys.stderr)
            sys.exit(1)
        else:
            return True
    else:
        return input(f"{prompt} ")


def ask_secret(prompt: Optional[str] = None):
    return getpass.getpass(f"{prompt} ")
