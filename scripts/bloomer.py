#!/usr/bin/env python3

import argparse

from lib import setcwd
from commands import add_command_parsers


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="The Bloomer CLI")
    subparsers = parser.add_subparsers(help="sub-command help")
    add_command_parsers(subparsers)
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)
    return args


def main() -> int:
    args = parse_args()
    setcwd()
    return args.func(args)


if __name__ == "__main__":
    exit(main())
