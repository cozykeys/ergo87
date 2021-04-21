#!/usr/bin/env python3

import json
import os
import argparse
import math
from typing import List, Dict, Tuple
from lib import (
    SvgStyle,
    SvgWriter,
    Vector2D,
    Segment2D,
    Polygon2D,
    get_bloomer_repo_dir,
    SwitchData,
    Corner,
)


SVG_STYLE_POLY: Dict[str, str] = {
    "fill-opacity": "0.0",
    "stroke": "#7f007f",  # Purple
    "stroke-width": "0.25",
}
SVG_STYLE_VEC: Dict[str, str] = {
    "fill-opacity": "1.0",
    "fill": "#7f007f",  # Purple
    "stroke": "none",
}
SVG_STYLE_VEC_1: Dict[str, str] = {
    "fill-opacity": "1.0",
    "fill": "#ff0000",  # Purple
    "stroke": "none",
}
SVG_STYLE_HOLE: Dict[str, str] = {
    "fill-opacity": "1.0",
    "fill": "#007f7f",  # Teal
    "stroke": "none",
}


def add_scratch_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "scratch", help="Scratchpad, dumping ground for temporary code"
    )
    parser.set_defaults(func=scratch)


def scratch(args: argparse.Namespace) -> int:
    bloomer_dir = get_bloomer_repo_dir()

    print("Bloomer repo directory: {}".format(bloomer_dir))

    sd = SwitchData()
    switches = sd.get_switches()

    p1 = sd.get_corner((0, 0), Corner.TOP_LEFT)
    p2 = (p1[0] + 1.0, p1[1])
    s1 = Segment2D(Vector2D(p1[0], p1[1]), Vector2D(p2[0], p2[1]))

    p3 = sd.get_corner((0, 3), Corner.TOP_RIGHT)
    p4 = sd.get_corner((0, 3), Corner.BOTTOM_RIGHT)
    s2 = Segment2D(Vector2D(p3[0], p3[1]), Vector2D(p4[0], p4[1]))

    i1 = s1.intersection(s2)

    dx = i1.x - p3[0]
    dy = i1.y - p3[1]

    p3 = (i1.x, i1.y)
    p4 = sd.get_corner((0, 5), Corner.TOP_RIGHT)
    i2 = (p4[0] + dx + 10, p4[1] + dy)

    p5 = sd.get_corner((0, 9), Corner.TOP_LEFT)
    i3 = (p5[0] - dx - 10, p5[1] + dy)

    p6 = sd.get_corner((0, 11), Corner.TOP_LEFT)
    i4 = (p6[0] - dx, p6[1] + dy)


    p1 = sd.get_corner((5, 14), Corner.BOTTOM_RIGHT)
    p2 = sd.get_corner((5, 9), Corner.BOTTOM_RIGHT)
    s1 = Segment2D(Vector2D(p1[0], p1[1]), Vector2D(p2[0], p2[1]))

    p3 = sd.get_corner((4, 8), Corner.TOP_LEFT)
    p4 = sd.get_corner((4, 8), Corner.BOTTOM_LEFT)
    s2 = Segment2D(Vector2D(p3[0], p3[1]), Vector2D(p4[0], p4[1]))

    i5 = s1.intersection(s2)
    dx = i5.x - p4[0]
    dy = i5.y - p4[1]

    p = sd.get_corner((4, 6), Corner.BOTTOM_RIGHT)
    i6 = (p[0] - dx, p[1] + dy)


    vertices = [
        sd.get_corner((0, 0), Corner.TOP_LEFT),
        (i1.x, i1.y),
        i2,
        i3,
        i4,
        sd.get_corner((0, 14), Corner.TOP_RIGHT),
        sd.get_corner((5, 14), Corner.BOTTOM_RIGHT),
        (i5.x, i5.y),
        i6,
        sd.get_corner((5, 0), Corner.BOTTOM_LEFT),
    ]

    print("{} -> {}".format(vertices[2], vertices[3]))

    perimeter = Polygon2D([ Vector2D(v[0], v[1]) for v in vertices ])

    svg_writer = SvgWriter()

    for switch in switches:
        poly = Polygon2D(
            [
                Vector2D(switch["x"] - 9.525, switch["y"] - 9.525),
                Vector2D(switch["x"] + 9.525, switch["y"] - 9.525),
                Vector2D(switch["x"] + 9.525, switch["y"] + 9.525),
                Vector2D(switch["x"] - 9.525, switch["y"] + 9.525),
            ]
        ).rotated_around(
            math.radians(switch["rotation"]), Vector2D(switch["x"], switch["y"])
        )
        svg_writer.append_element(poly, SvgStyle(SVG_STYLE_POLY))

    # svg_writer.append_element(perimeter.vertices[2], SvgStyle(SVG_STYLE_VEC))
    svg_writer.append_element(perimeter, SvgStyle(SVG_STYLE_POLY))

    svg_writer.write_to_file("{}/temp/render.svg".format(bloomer_dir))

    vertices = [(round(v[0], 3), round(v[1], 3)) for v in vertices]
    with open(os.path.join(bloomer_dir, "temp", "pcb_edge_vertices.json"), "w") as f:
        f.write(json.dumps(vertices, indent="    "))

    return 0
