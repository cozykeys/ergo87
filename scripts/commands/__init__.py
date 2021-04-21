import argparse


def add_command_parsers(subparsers: argparse._SubParsersAction) -> None:
    from .expand_vertices import add_expand_vertices_parser

    add_expand_vertices_parser(subparsers)

    from .scratch import add_scratch_parser

    add_scratch_parser(subparsers)
