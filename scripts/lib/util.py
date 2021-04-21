#!/usr/bin/env python3

import os
import errno
import subprocess

from typing import List


def get_bloomer_repo_dir() -> str:
    """Get the root directory of the Bloomer repository

    This function makes a hard assumption about the path of the util.py script.
    If the script moves, this function **must** be updated!
    """
    import os

    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    return os.path.realpath(os.path.join(script_dir, "..", ".."))


def setcwd() -> None:
    """Set the current working directory to the repository root
    """

    base_dir = get_bloomer_repo_dir()

    print("Changing current working directory to {}".format(base_dir))
    os.chdir(base_dir)


def sh(cmd: List[str]) -> int:
    """Run a shell command synchronously

    Returns true if the command exits with a return code of 0 and false
    otherwise.

    This expects the command to be provided in the form of a sanitized list of
    tokens.
    """
    print("Executing shell command: {}".format(" ".join(cmd)))
    return subprocess.call(cmd)


def mkdir(path: str) -> None:
    """Make a directory recursively

    Functionality should be equivalent to `mkdir -p`.
    """
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(path):
            raise
