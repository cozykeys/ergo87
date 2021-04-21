#!/usr/bin/env python3


def get_kbutil_dll_path() -> str:
    import os

    kbutil_dir = os.path.realpath(os.path.join("..", "kbutil"))
    return os.path.join(
        kbutil_dir, "build", "KbUtil.Console", "bin", "Release", "kbutil.dll"
    )
