#!/usr/bin/env python3

from .svg import SvgWritable
import math
import sympy.geometry as spg  # type: ignore
from typing import List, Tuple, Dict
import json


class Vector2D(SvgWritable):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, data: Dict[str, float]) -> "Vector2D":
        return cls(data["x"], data["y"])

    def to_json(self) -> Dict[str, float]:
        return {"x": round(self.x, 3), "y": round(self.y, 3)}

    def scaled(self, magnitude: float) -> "Vector2D":
        v = self.normalized()
        return Vector2D(v.x * magnitude, v.y * magnitude)

    def normalized(self) -> "Vector2D":
        magnitude = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
        return Vector2D(self.x / magnitude, self.y / magnitude)

    def to_svg(self, style: str) -> List[str]:
        return [
            '<circle style="{}" cx="{}" cy="{}" r="0.5" />'.format(
                style, round(self.x, 3), round(self.y, 3)
            )
        ]


class Line2D(SvgWritable):
    def __init__(self, point: Vector2D, direction: Vector2D) -> None:
        self.point = point
        self.direction = direction

    def __str__(self) -> str:
        return '{{"point":{},"direction":{}}}'.format(self.point, self.direction)


class Segment2D(SvgWritable):
    def __init__(self, start: Vector2D, end: Vector2D) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return '{{"start":{},"end":{}}}'.format(self.start, self.end)

    def mid(self) -> Vector2D:
        return Vector2D(
            self.start.x + ((self.end.x - self.start.x) / 2.0),
            self.start.y + ((self.end.y - self.start.y) / 2.0),
        )

    def intersection(self, s: "Segment2D") -> Vector2D:
        l1 = spg.Line(
            spg.Point(self.start.x, self.start.y), spg.Point(self.end.x, self.end.y)
        )
        l2 = spg.Line(spg.Point(s.start.x, s.start.y), spg.Point(s.end.x, s.end.y))

        intersections = l1.intersection(l2)
        if len(intersections) != 1:
            raise Exception("TODO")
        if not isinstance(intersections[0], spg.Point2D):
            raise Exception("TODO")
        return Vector2D(float(intersections[0].x), float(intersections[0].y))

    def to_vector(self) -> Vector2D:
        return Vector2D(self.end.x - self.start.x, self.end.y - self.start.y)

    def to_line(self) -> Line2D:
        return Line2D(self.mid(), self.direction())

    def direction(self) -> Vector2D:
        return self.to_vector().normalized()

    def to_svg(self, style: str) -> List[str]:
        data_str = "M {} {} L {} {}".format(
            round(self.start.x, 3),
            round(self.start.y, 3),
            round(self.end.x, 3),
            round(self.end.y, 3),
        )
        return ['<path style="{}" d="{}" />'.format(style, data_str)]


class Polygon2D(SvgWritable):
    def __init__(self, vertices: List[Vector2D]) -> None:
        self.vertices = vertices

    def __str__(self) -> str:
        return "[{}]".format(",".join(["{}".format(v) for v in self.vertices]))

    def _segments(self) -> List[Segment2D]:
        segments: List[Segment2D] = []
        for curr in range(0, len(self.vertices)):
            next = (curr + 1) % len(self.vertices)
            if self.vertices[curr] == self.vertices[next]:
                raise Exception("Two duplicate adjacent points encountered in the path")
            segments.append(Segment2D(self.vertices[curr], self.vertices[next]))
        return segments

    def center(self) -> Vector2D:
        min_x = min([v.x for v in self.vertices])
        max_x = max([v.x for v in self.vertices])
        min_y = min([v.y for v in self.vertices])
        max_y = max([v.y for v in self.vertices])
        mid_x = min_x + ((max_x - min_x) / 2.0)
        mid_y = min_y + ((max_y - min_y) / 2.0)
        return Vector2D(mid_x, mid_y)

    def translated(self, d: Vector2D) -> "Polygon2D":
        return Polygon2D([Vector2D(v.x + d.x, v.y + d.y) for v in self.vertices])

    def rotated_around(self, theta, p) -> "Polygon2D":
        c = self.translated(Vector2D(-p.x, -p.y))
        rotated = Polygon2D(
            [
                Vector2D(
                    v.x * math.cos(theta) - v.y * math.sin(theta),
                    v.x * math.sin(theta) + v.y * math.cos(theta),
                )
                for v in c.vertices
            ]
        )
        return rotated.translated(Vector2D(p.x, p.y))

    def rotated(self, theta) -> "Polygon2D":
        return self.rotated_around(theta, self.center())

    def centered(self) -> "Polygon2D":
        mid = self.center()
        return Polygon2D([Vector2D(v.x - mid.x, v.y - mid.y) for v in self.vertices])

    def expanded(self, distance: float) -> "Polygon2D":
        expanded_lines = []
        for s in self._segments():
            # Get the direction vector for the segment
            direction = Vector2D(s.end.x - s.start.x, s.end.y - s.start.y).normalized()

            # Get the perpendicular normal vector
            normal = Vector2D(-direction.y, direction.x)

            # Scale the normal to the desired distance
            diff = normal.scaled(distance)

            # Use the scaled normal vector to create the expanded line
            expanded_line = Line2D(
                Vector2D(s.mid().x + diff.x, s.mid().y + diff.y), direction
            )

            expanded_lines.append(expanded_line)

        # Too lazy to write intersection logic so convert to SymPy's line class
        # and use that to calculate the intersection points
        sympy_lines = [
            spg.Line(
                spg.Point(l.point.x, l.point.y),
                spg.Point(l.point.x + l.direction.x, l.point.y + l.direction.y),
            )
            for l in expanded_lines
        ]

        expanded_vertices = []
        for curr in range(0, len(sympy_lines)):
            prev = curr - 1 if curr > 0 else len(sympy_lines) - 1
            intersections = sympy_lines[prev].intersection(sympy_lines[curr])
            if len(intersections) != 1:
                raise Exception("TODO")
            if not isinstance(intersections[0], spg.Point2D):
                raise Exception("TODO")
            expanded_vertices.append(
                Vector2D(float(intersections[0].x), float(intersections[0].y))
            )

        return Polygon2D(expanded_vertices)

    def to_svg(self, style: str) -> List[str]:
        if len(self.vertices) < 2:
            raise Exception("TODO")
        data_tokens = [
            "M {} {}".format(round(self.vertices[0].x, 3), round(self.vertices[0].y, 3))
        ]
        for i in range(1, len(self.vertices)):
            v = self.vertices[i]
            data_tokens.append("L {} {}".format(round(v.x, 3), round(v.y, 3)))
        data_tokens.append(
            "L {} {}".format(round(self.vertices[0].x, 3), round(self.vertices[0].y, 3))
        )
        data_str = " ".join(data_tokens)
        return ['<path style="{}" d="{}" />'.format(style, data_str)]

    @classmethod
    def from_json(cls, data: List[Tuple[float, float]]) -> "Polygon2D":
        return cls([Vector2D.from_json(v) for v in data])

    def to_json(self) -> List[Tuple[float, float]]:
        return [v.to_json() for v in self.vertices]


class Curve2D(SvgWritable):
    def __init__(self, start: Vector2D, end: Vector2D, control: Vector2D):
        self.start = start
        self.end = end
        self.control = control

    def __str__(self) -> str:
        return '{{"start":{},"end":{},"control":{}}}'.format(
            self.start, self.end, self.control
        )

    def to_svg(self, style: str) -> List[str]:
        return [
            '<path style="{}" d="M {} {} Q {} {} {} {}" />'.format(
                style,
                self.start.x,
                self.start.y,
                self.control.x,
                self.control.y,
                self.end.x,
                self.end.y,
            )
        ]

    def to_json(self) -> Dict[str, Dict[str, float]]:
        return {
            "start": self.start.to_json(),
            "end": self.end.to_json(),
            "control": self.control.to_json(),
        }
