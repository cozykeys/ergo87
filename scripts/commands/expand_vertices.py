#!/usr/bin/env python3

import json
import argparse
from typing import List, Dict, Tuple
from lib import SvgStyle, SvgWriter, Polygon2D


SVG_STYLE_VEC_BEFORE: Dict[str, str] = {
    "fill-opacity": "1.0",
    "fill": "#7f007f",  # Purple
    "stroke": "none",
}
SVG_STYLE_POLY_BEFORE: Dict[str, str] = {
    "fill-opacity": "0.0",
    "stroke": "#7f007f",  # Purple
    "stroke-width": "0.25",
}

SVG_STYLE_VEC_AFTER: Dict[str, str] = {
    "fill-opacity": "1.0",
    "fill": "#007f7f",  # Teal
    "stroke": "none",
}
SVG_STYLE_POLY_AFTER: Dict[str, str] = {
    "fill-opacity": "0.0",
    "stroke": "#007f7f",  # Teal
    "stroke-width": "0.25",
}


def add_expand_vertices_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "expand-vertices", help="Given a set up vertices, expand them"
    )
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    parser.add_argument("distance", type=float)
    parser.add_argument("--debug-svg", type=str, default="")
    parser.set_defaults(func=expand_vertices)


def expand_vertices(args: argparse.Namespace) -> int:
    json_data: List[Tuple[float, float]] = []
    with open(args.input_path, "r") as f:
        json_data = json.loads(f.read())

    original_poly = Polygon2D.from_json(json_data)
    expanded_poly = original_poly.expanded(args.distance)

    svg_writer = SvgWriter()
    svg_writer.append_element(original_poly, SvgStyle(SVG_STYLE_POLY_BEFORE))
    for v in original_poly.vertices:
        svg_writer.append_element(v, SvgStyle(SVG_STYLE_VEC_BEFORE))
    svg_writer.append_element(expanded_poly, SvgStyle(SVG_STYLE_POLY_AFTER))
    for v in expanded_poly.vertices:
        svg_writer.append_element(v, SvgStyle(SVG_STYLE_VEC_AFTER))
    if args.debug_svg != "":
        print('Writing debug svg to "{}"'.format(args.debug_svg))
        svg_writer.write_to_file(args.debug_svg)
    else:
        svg_writer.write_to_stdout()

    with open(args.output_path, "w") as f:
        f.write(json.dumps(expanded_poly.to_json(), indent=4))

    return 0
