#!/usr/bin/env python3

from typing import List, Dict, Tuple


class SvgWritable:
    def to_svg(self, style: str) -> List[str]:
        raise Exception("Subclass has not implemented SvgWritable.to_svg")


class SvgStyle:
    def __init__(self, style_dictionary: Dict[str, str] = {}):
        self.style_dictionary = style_dictionary

    def __str__(self) -> str:
        return "; ".join(
            [
                "{}: {}".format(key, self.style_dictionary[key])
                for key in self.style_dictionary
            ]
        )


class SvgWriter:
    def __init__(self) -> None:
        self.elements: List[Tuple[SvgWritable, str]] = []

    def write_to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self._write())

    def write_to_stdout(self) -> None:
        print(self._write())

    def _write(self) -> str:
        lines = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<svg width="375mm" height="175mm" viewBox="0 0 375 175" xmlns="http://www.w3.org/2000/svg">',
        ]
        for e in self.elements:
            lines += e[0].to_svg(e[1])
        lines.append("</svg>")
        return "\n".join(lines)

    def append_element(self, element: SvgWritable, style: SvgStyle) -> None:
        self.elements.append((element, style.__str__()))
