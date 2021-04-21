#!/usr/bin/env python3

import os
from .util import get_bloomer_repo_dir, mkdir


class Logger:
    def __init__(self, path: str = "") -> None:

        self.path = os.path.join(get_bloomer_repo_dir(), "temp", "bloomer.log")
        if path != "":
            self.path = path

        mkdir(os.path.dirname(self.path))

        with open(self.path, "w"):
            pass

    def log(self, message: str) -> None:
        with open(self.path, "a") as f:
            f.write("{}\n".format(message))
