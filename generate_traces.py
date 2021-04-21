#!/usr/bin/env python3

# A lot of this is ridiculously hacky and makes major assumptions but it's
# still better than drawing traces by hand. :)

import json
import math

# Lookup table for net ids
net_ids = {
    '""': 0,
    '+5V': 1,
    '"Net-(C1-Pad1)"': 2,
    '"Net-(C2-Pad1)"': 3,
    'VCC': 4,
    '"Net-(C8-Pad1)"': 5,
    '"Net-(D1-Pad2)"': 6,
    '/row0': 7,
    '"Net-(D2-Pad2)"': 8,
    '/row1': 9,
    '"Net-(D3-Pad2)"': 10,
    '/row2': 11,
    '"Net-(D4-Pad2)"': 12,
    '/row3': 13,
    '"Net-(D5-Pad2)"': 14,
    '/row4': 15,
    '"Net-(D6-Pad2)"': 16,
    '/row5': 17,
    '"Net-(D7-Pad2)"': 18,
    '"Net-(D8-Pad2)"': 19,
    '"Net-(D9-Pad2)"': 20,
    '"Net-(D10-Pad2)"': 21,
    '"Net-(D11-Pad2)"': 22,
    '"Net-(D12-Pad2)"': 23,
    '"Net-(D13-Pad2)"': 24,
    '"Net-(D14-Pad2)"': 25,
    '"Net-(D15-Pad2)"': 26,
    '"Net-(D16-Pad2)"': 27,
    '"Net-(D17-Pad2)"': 28,
    '"Net-(D18-Pad2)"': 29,
    '"Net-(D19-Pad2)"': 30,
    '"Net-(D20-Pad2)"': 31,
    '"Net-(D21-Pad2)"': 32,
    '"Net-(D22-Pad2)"': 33,
    '"Net-(D23-Pad2)"': 34,
    '"Net-(D24-Pad2)"': 35,
    '"Net-(D25-Pad2)"': 36,
    '"Net-(D26-Pad2)"': 37,
    '"Net-(D27-Pad2)"': 38,
    '"Net-(D28-Pad2)"': 39,
    '"Net-(D29-Pad2)"': 40,
    '"Net-(D30-Pad2)"': 41,
    '"Net-(D31-Pad2)"': 42,
    '"Net-(D32-Pad2)"': 43,
    '"Net-(D33-Pad2)"': 44,
    '"Net-(D34-Pad2)"': 45,
    '"Net-(D35-Pad2)"': 46,
    '"Net-(D36-Pad2)"': 47,
    '"Net-(D37-Pad2)"': 48,
    '"Net-(D38-Pad2)"': 49,
    '"Net-(D39-Pad2)"': 50,
    '"Net-(D40-Pad2)"': 51,
    '"Net-(D41-Pad2)"': 52,
    '"Net-(D42-Pad2)"': 53,
    '"Net-(D43-Pad2)"': 54,
    '"Net-(D44-Pad2)"': 55,
    '"Net-(D45-Pad2)"': 56,
    '"Net-(D46-Pad2)"': 57,
    '"Net-(D47-Pad2)"': 58,
    '"Net-(D48-Pad2)"': 59,
    '"Net-(D49-Pad2)"': 60,
    '"Net-(D50-Pad2)"': 61,
    '"Net-(D51-Pad2)"': 62,
    '"Net-(D52-Pad2)"': 63,
    '"Net-(D53-Pad2)"': 64,
    '"Net-(D54-Pad2)"': 65,
    '"Net-(D55-Pad2)"': 66,
    '"Net-(D56-Pad2)"': 67,
    '"Net-(D57-Pad2)"': 68,
    '"Net-(D58-Pad2)"': 69,
    '"Net-(D59-Pad2)"': 70,
    '"Net-(D60-Pad2)"': 71,
    '"Net-(D61-Pad2)"': 72,
    '"Net-(D62-Pad2)"': 73,
    '"Net-(D63-Pad2)"': 74,
    '"Net-(D64-Pad2)"': 75,
    '"Net-(D65-Pad2)"': 76,
    '"Net-(D66-Pad2)"': 77,
    '"Net-(D67-Pad2)"': 78,
    '"Net-(D68-Pad2)"': 79,
    '"Net-(D69-Pad2)"': 80,
    '"Net-(D70-Pad2)"': 81,
    '"Net-(D71-Pad2)"': 82,
    '"Net-(D72-Pad2)"': 83,
    '"Net-(D73-Pad2)"': 84,
    '"Net-(D74-Pad2)"': 85,
    '"Net-(D75-Pad2)"': 86,
    '"Net-(D76-Pad2)"': 87,
    '"Net-(D77-Pad2)"': 88,
    '"Net-(D78-Pad2)"': 89,
    '"Net-(D79-Pad2)"': 90,
    '"Net-(D80-Pad2)"': 91,
    '"Net-(D81-Pad2)"': 92,
    '"Net-(D82-Pad2)"': 93,
    '"Net-(D83-Pad2)"': 94,
    '"Net-(D84-Pad2)"': 95,
    '"Net-(D85-Pad2)"': 96,
    '"Net-(D86-Pad2)"': 97,
    '"Net-(D87-Pad2)"': 98,
    '"Net-(J1-Pad2)"': 99,
    '"Net-(J1-Pad3)"': 100,
    '"Net-(J1-Pad4)"': 101,
    '/col0': 102,
    '/col1': 103,
    '/col2': 104,
    '/col3': 105,
    '/col4': 106,
    '/col5': 107,
    '/col6': 108,
    '/col7': 109,
    '/col8': 110,
    '/col9': 111,
    '/col10': 112,
    '/col11': 113,
    '/col12': 114,
    '/col13': 115,
    '"Net-(K82-Pad1)"': 116,
    '"Net-(L1-Pad2)"': 117,
    '/rgb': 118,
    '"Net-(L2-Pad2)"': 119,
    '"Net-(L3-Pad2)"': 120,
    '"Net-(L4-Pad2)"': 121,
    '"Net-(L5-Pad2)"': 122,
    '"Net-(L6-Pad2)"': 123,
    '"Net-(L7-Pad2)"': 124,
    '"Net-(L8-Pad2)"': 125,
    '"Net-(L10-Pad4)"': 126,
    '"Net-(L10-Pad2)"': 127,
    '"Net-(L11-Pad2)"': 128,
    '"Net-(L12-Pad2)"': 129,
    '"Net-(R1-Pad1)"': 130,
    '"Net-(R2-Pad2)"': 131,
    '"Net-(R3-Pad1)"': 132,
    '"Net-(R4-Pad1)"': 133,
    '"Net-(U1-Pad1)"': 134,
    '/col14': 135,
    '"Net-(U1-Pad11)"': 136,
    '"Net-(U1-Pad12)"': 137,
    '"Net-(U1-Pad42)"': 138,
}

def print_segment(start_x, start_y, end_x, end_y, net_id, layer="Front"):
    start_str   = '(start {x} {y})'.format(x=start_x, y=start_y)
    end_str     = '(end {x} {y})'.format(x=end_x, y=end_y)
    width_str   = '(width 0.2032)'
    layer_str   = '(layer {})'.format(layer)
    net_str     = '(net {net_id})'.format(net_id=net_id)
    if net_id is not None:
        print('(segment {0} {1} {2} {3} {4})'.format(
            start_str, end_str, width_str, layer_str, net_str))
    else:
        print('(segment {0} {1} {2} {3})'.format(
            start_str, end_str, width_str, layer_str))

def print_via(x, y, net_id):
  at_str     = '(at {} {})'.format(x, y)
  size_str   = '(size 0.889)'
  drill_str  = '(drill 0.635)'
  layers_str = '(layers F.Cu B.Cu)'
  net_str    = '(net {})'.format(net_id)
  print('(via {} {} {} {} {})'.format(at_str, size_str, drill_str, layers_str, net_str))

class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __add__(self, rhs):
        return Vec2(self.x + rhs.x, self.y + rhs.y)


class Segment:
    def __init__(self, start = Vec2(), end = Vec2()):
        self.start = start
        self.end = end

    def theta(self):
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y

        # Early out if the segment is parallel to an axis.
        if abs(dy) < 0.001 and dx > 0:
            return (0.0 * math.pi)
        if abs(dx) < 0.001 and dy > 0:
            return (0.5 * math.pi)
        if abs(dy) < 0.001 and dx < 0:
            return (1.0 * math.pi)
        if abs(dx) < 0.001 and dy < 0:
            return (1.5 * math.pi)

        theta = math.atan(dy / dx)

        # Because slope doesn't take direction into account, we have to manually adjust theta for segments whose
        # direction points into quadrants 2 and 3.
        if ((dx < 0 and dy > 0) or (dx < 0 and dy < 0)):
            theta += math.pi

        return theta - (math.pi * 2)  * math.floor(theta / (math.pi * 2))
    
    def __str__(self):
        return "[ {0}, {1} ]".format(self.start, self.end)

    def print(self, net_id=None, layer="Front"):
        print_segment(self.start.x, self.start.y, self.end.x, self.end.y, net_id, layer)

# Given the distance along the x and y axes as well as a rotation, returns a
# vector
def make_vector(x, y, rotation):
    magnitude = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    segment = Segment(Vec2(0, 0), Vec2(x, y))
    theta = segment.theta() + math.radians(rotation)
    return Vec2(
        magnitude * math.cos(theta),
        magnitude * math.sin(theta))

# Given a switch and a distance along the x and y axes (dx, dy), returns a
# vector projected those distances from the switch using its rotation
def project_from_switch(switch, dx, dy):
    # Position vector of the switch
    v1 = Vec2(switch['x'], switch['y'])
    # "Projection" vector
    v2 = make_vector(dx, dy, switch['rotation'])
    return v1 + v2

def foo(switch, dx, dy):
    return project_from_switch(switch, dx, dy)

def calculate_column_segments(switches):
    dx = -3.255
    dy = -3.52

    segments = {}
    for c in [0,1,2,3,4,5,9,10,11,12,13,14]:
        s0 = switches[0][c]
        s1 = switches[5][c]
        segments[c] = Segment(
            project_from_switch(s0, dx, dy),
            project_from_switch(s1, dx, dy))

    for c in [6,8]:
        s0 = switches[0][c]
        s1 = switches[3][c]
        segments[c] = Segment(
            project_from_switch(s0, dx, dy),
            project_from_switch(s1, dx, dy))

    s0 = switches[0][7]
    s1 = switches[4][7]
    segments[7] = Segment(
        project_from_switch(s0, dx, dy),
        project_from_switch(s1, dx, dy))

    return segments


def print_column_segments(column_segments):
    for c in column_segments:
        net_id = net_ids['/col{}'.format(c)]
        column_segments[c].print(net_id, "F.Cu")


def print_switch_to_column_segments(switches):
    for r in [0,1,2,3,4]:
        for c in [0,1,2,3,4,5,7,8,9,10,11,12]:
            s = switches[r][c]
            Segment(foo(s, 3.81, 2.54), foo(s, 7.065, 2.54)).print(net_ids['N-col-{}'.format(c)], "Front")

    s = switches[0][6]
    v1 = foo(s, 3.81, 2.54)
    v2 = foo(s, 7.065, 2.54)
    v3 = foo(s, 7.065, -7.7)
    Segment(v1, v2).print(net_ids['N-col-6'], "Front")
    Segment(v2, v3).print(net_ids['N-col-6'], "Front")

    s = switches[1][6]
    v1 = foo(s, 3.81, 2.54)
    v2 = foo(s, 7.065, 2.54)
    v3 = Vec2(162.255, 125.095)
    Segment(v1, v2).print(net_ids['N-col-6'], "Front")
    Segment(v2, v3).print(net_ids['N-col-6'], "Front")
    print_via(v3.x, v3.y, net_ids['N-col-6'])

    s = switches[2][6]
    v1 = foo(s, 3.81, 2.54)
    v2 = foo(s, 7.065, 2.54)
    v3 = Vec2(202.093, 125.095)
    Segment(v1, v2).print(net_ids['N-col-6'], "Front")
    Segment(v2, v3).print(net_ids['N-col-6'], "Front")
    print_via(v3.x, v3.y, net_ids['N-col-6'])

    v1 = Vec2(162.255, 125.095)
    v2 = Vec2(202.093, 125.095)
    Segment(v1, v2).print(net_ids['N-col-6'], "Back")

    v1 = Vec2(182.065, 108.54)
    v2 = Vec2(182.065, 125.095)
    Segment(v1, v2).print(net_ids['N-col-6'], "Front")
    print_via(v2.x, v2.y, net_ids['N-col-6'])

    v1 = Vec2(182.065, 98.3)
    v2 = Vec2(167.64, 98.3)
    v3 = Vec2(165.735, 96.52)
    v4 = Vec2(165.735, 76.38)
    v5 = Vec2(167.38, 76.38)
    Segment(v1, v2).print(net_ids['N-col-6'], "Front")
    print_via(v2.x, v2.y, net_ids['N-col-6'])
    Segment(v2, v3).print(net_ids['N-col-6'], "Back")
    Segment(v3, v4).print(net_ids['N-col-6'], "Back")
    Segment(v4, v5).print(net_ids['N-col-6'], "Back")


def print_switch_to_diode_segments(switches):
    i = 1
    for r in [0,1,2,3,4,5]:
        for c in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
            if r in switches and c in switches[r]:
                s = switches[r][c]

                net_id = net_ids['"Net-(D{}-Pad2)"'.format(i)]
                i += 1
                segment = Segment(
                    project_from_switch(s, 2.54, -4.79),
                    project_from_switch(s, 8.0, -3.9))
                segment.print(net_id, "B.Cu")

def print_row_segments(switches):
    for r in [0,1,2,3,4,5]:
        for c in range(1,6):
            s = switches[r][c]
            net_id = net_ids['/row{}'.format(r)]

            left_attachment_segment = Segment(
                project_from_switch(switches[r][c-1], 8.0, 3.9),
                project_from_switch(s, -5.08, 3.9))
            left_attachment_segment.print(net_id, "B.Cu")

            middle_segment = Segment(
                project_from_switch(s, -5.08, 3.9),
                project_from_switch(s,  5.08, 3.9))
            middle_segment.print(net_id, "B.Cu")

            right_attachment_segment = Segment(
                project_from_switch(s, 5.08, 3.9),
                project_from_switch(s,  8.0, 3.9))
            right_attachment_segment.print(net_id, "B.Cu")

        for c in range(10,15):
            s = switches[r][c]
            net_id = net_ids['/row{}'.format(r)]

            left_attachment_segment = Segment(
                project_from_switch(switches[r][c-1], 8.0, 3.9),
                project_from_switch(s, -5.08, 3.9))
            left_attachment_segment.print(net_id, "B.Cu")

            middle_segment = Segment(
                project_from_switch(s, -5.08, 3.9),
                project_from_switch(s,  5.08, 3.9))
            middle_segment.print(net_id, "B.Cu")

            right_attachment_segment = Segment(
                project_from_switch(s, 5.08, 3.9),
                project_from_switch(s,  8.0, 3.9))
            right_attachment_segment.print(net_id, "B.Cu")


    for r in [0,1,2]:
        net_id = net_ids['/row{}'.format(r)]
        segment = Segment(
            project_from_switch(switches[r][6], 8.0, 3.9),
            project_from_switch(switches[r][8], 8.0, 3.9))
        segment.print(net_id, "B.Cu")

    net_id = net_ids['/row5']
    segment = Segment(
        project_from_switch(switches[3][6], 8.0, 3.9),
        project_from_switch(switches[3][8], 8.0, 3.9))
    segment.print(net_id, "B.Cu")


def calculate_vcc_column_segments(switches):
    dx = -7.065
    dy = -3.81

    segments = {}
    for c in [0,1,2,3,4,5,7,8,9,10,11,12]:
        s0 = switches[0][c]
        s1 = switches[4][c]
        segments[c] = Segment(foo(s0, dx, dy), foo(s1, dx, dy))
    return segments


def print_vcc_column_segments(vcc_column_segments):
    for c in vcc_column_segments:
        vcc_column_segments[c].print(net_ids['N-5V-0'], "Front")


def print_switch_to_vcc_column_segments(switches):
    for r in [0,1,2,3,4]:
        for c in [0,1,2,3,4,5,6,7,8,9,10,11,12]:
            if r in switches and c in switches[r]:
                s = switches[r][c]
                Segment(foo(s, -1.27, -5.08), foo(s, -4.445, -3.81)).print(net_ids['N-5V-0'], "Front")
                Segment(foo(s, -4.445, -3.81), foo(s, -7.065, -3.81)).print(net_ids['N-5V-0'], "Front")


def print_diode_to_row_components(switches):
    for r in range(0,6):
        for c in range(0,15):
            if r in switches and c in switches[r]:
                s = switches[r][c]
                net_id = net_ids['N-row-{}'.format(r)]

                v1 = foo(s, -4.445, -5.474)
                v2 = foo(s, -7.065, -5.474)
                v3 = foo(s, -7.065, 2.54)
                v4 = foo(s, -5.08, 2.54)
                v5 = foo(s, -1.905, 2.54)
                v6 = foo(s, 0.635, 5.08)
                v7 = foo(s, 5.08, 5.08)

                Segment(v1, v2).print(net_id, "Back")
                Segment(v2, v3).print(net_id, "Back")
                Segment(v3, v4).print(net_id, "Back")
                Segment(v4, v5).print(net_id, "Front")
                Segment(v5, v6).print(net_id, "Front")
                Segment(v6, v7).print(net_id, "Front")

                print_via(v4.x, v4.y, net_id)
                print_via(v7.x, v7.y, net_id)

    v1 = Vec2(170.555, 100.526)
    v2 = Vec2(169.92, 99.06)
    v3 = Vec2(169.92, 86.36)
    Segment(v1, v2).print(net_ids['N-row-0'], "Back")
    Segment(v2, v3).print(net_ids['N-row-0'], "Back")

    v1 = Vec2(150.28408, 126.699296)
    v2 = Vec2(150.679, 124.46)
    v3 = Vec2(150.679, 121.285)
    print_via(v2.x, v2.y, net_ids['N-row-1'])
    Segment(v1, v2).print(net_ids['N-row-1'], "Back")
    Segment(v2, v3).print(net_ids['N-row-1'], "Front")
    v4 = Vec2(155.575, 121.285)
    v5 = Vec2(155.575, 92.71)
    v6 = Vec2(155.575, 87.63)
    Segment(v3, v4).print(net_ids['N-row-1'], "Front")
    Segment(v4, v5).print(net_ids['N-row-1'], "Front")
    print_via(v5.x, v5.y, net_ids['N-row-1'])
    Segment(v5, v6).print(net_ids['N-row-2'], "Back")
    print_via(v6.x, v6.y, net_ids['N-row-2'])

    v1 = Vec2(190.960979, 128.243029)
    v2 = Vec2(190.63, 126.365)
    v3 = Vec2(190.63, 121.285)
    print_via(v2.x, v2.y, net_ids['N-row-2'])
    Segment(v1, v2).print(net_ids['N-row-2'], "Back")
    Segment(v2, v3).print(net_ids['N-row-2'], "Front")
    v4 = Vec2(194.31, 121.285)
    v5 = Vec2(194.31, 92.71)
    v6 = Vec2(194.31, 88.9)
    Segment(v3, v4).print(net_ids['N-row-2'], "Front")
    Segment(v4, v5).print(net_ids['N-row-2'], "Front")
    print_via(v5.x, v5.y, net_ids['N-row-2'])
    Segment(v5, v6).print(net_ids['N-row-2'], "Back")
    print_via(v6.x, v6.y, net_ids['N-row-2'])


def print_row_attachment_segments(switches):
    for r in [0,1,2,3,4]:
        net_id = net_ids['N-row-{}'.format(r)]

        for c in [0,1,2,3,4]:
            s1 = switches[r][c]
            s2 = switches[r][c+1]

            v1 = foo(s1, 5.08, 5.08)
            v2 = foo(s2, -7.065, 2.54)

            Segment(v1, v2).print(net_id, "Back")

        for c in [7,8,9,10,11]:
            s1 = switches[r][c]
            s2 = switches[r][c+1]

            v1 = foo(s1, 5.08, 5.08)
            v2 = foo(s2, -7.065, 2.54)

            Segment(v1, v2).print(net_id, "Back")

    for i in range(0,5):
        net_id = net_ids['N-row-{}'.format(i)]
        x = 169.92 + (i * 2.54)
        v1 = Vec2(x, 78.92)
        v2 = Vec2(x, 86.36 + (i * 1.27))
        Segment(v1, v2).print(net_id, "Back")
        print_via(v2.x, v2.y, net_id)

    row = 0
    net_id = net_ids['N-row-0']
    v1 = Vec2(152.303, 60.396)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = bar(v2.x, v2.y, 0, 17.78, 10)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, 1.27, 0, 10)
    v5 = Vec2(154.092, 86.36)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = Vec2(169.92, 86.36)
    Segment(v5, v6).print(net_id, "Front")

    row = 1
    net_id = net_ids['N-row-1']
    v1 = Vec2(148.995, 79.157)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = Vec2(152.578, 87.63)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = Vec2(172.46, 87.63)
    Segment(v3, v4).print(net_id, "Front")

    row = 2
    net_id = net_ids['N-row-2']
    v1 = Vec2(145.687, 97.917)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = Vec2(152.355, 88.9)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = Vec2(175, 88.9)
    Segment(v3, v4).print(net_id, "Front")

    row = 3
    net_id = net_ids['N-row-3']
    v1 = Vec2(142.379, 116.678)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = bar(v2.x, v2.y, 0, -17.78, 10)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, 1.27, 0, 10)
    v5 = Vec2(153.42, 90.17)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = Vec2(177.54, 90.17)
    Segment(v5, v6).print(net_id, "Front")

    row = 4
    net_id = net_ids['N-row-4']
    v1 = Vec2(139.071, 135.439)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = bar(v2.x, v2.y, 0, -17.78, 10)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, 1.27, 0, 10)
    v5 = bar(v4.x, v4.y, 0, -17.78, 10)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = bar(v5.x, v5.y, 1.27, 0, 10)
    v7 = Vec2(154.486, 91.44)
    Segment(v5, v6).print(net_id, "Front")
    Segment(v6, v7).print(net_id, "Front")
    v8 = Vec2(180.08, 91.44)
    Segment(v7, v8).print(net_id, "Front")

    row = 0
    net_id = net_ids['N-row-0']
    va = Vec2(192.772961, 61.264241)
    vb = Vec2(195.3014, 58.239236)
    Segment(va, vb).print(net_id, "Back")
    v1 = Vec2(175 + (175 - 152.303), 60.396)
    v2 = bar(v1.x, v1.y, -5, 0, -10)
    v3 = bar(v2.x, v2.y, 0, 17.78, -10)
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, -1.27, 0, -10)
    v5 = Vec2(175 + (175 - 154.092), 86.36)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = Vec2(169.92, 86.36)
    Segment(v5, v6).print(net_id, "Front")

    row = 1
    net_id = net_ids['N-row-1']
    va = Vec2(196.080961, 80.025241)
    vb = Vec2(198.6094, 77.000236)
    Segment(va, vb).print(net_id, "Back")
    v1 = Vec2(175 + (175 - 148.995), 79.157)
    v2 = bar(v1.x, v1.y, -5, 0, -10)
    v3 = Vec2(175 + (175 - 152.578), 87.63)
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = Vec2(172.46, 87.63)
    Segment(v3, v4).print(net_id, "Front")

    row = 2
    net_id = net_ids['N-row-2']
    va = Vec2(199.388961, 98.785241)
    vb = Vec2(201.9174, 95.760236)
    Segment(va, vb).print(net_id, "Back")
    v1 = Vec2(175 + (175 - 145.687), 97.917)
    v2 = bar(v1.x, v1.y, -5, 0, -10)
    v3 = Vec2(175 + (175 - 152.355), 88.9)
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = Vec2(175, 88.9)
    Segment(v3, v4).print(net_id, "Front")

    row = 3
    net_id = net_ids['N-row-3']
    va = Vec2(202.696961, 117.546241)
    vb = Vec2(205.2254, 114.521236)
    Segment(va, vb).print(net_id, "Back")
    v1 = Vec2(175 + (175 - 142.379), 116.678)
    v2 = bar(v1.x, v1.y, -5, 0, -10)
    v3 = bar(v2.x, v2.y, 0, -17.78, -10)
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, -1.27, 0, -10)
    v5 = Vec2(175 + (175 - 153.42), 90.17)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = Vec2(177.54, 90.17)
    Segment(v5, v6).print(net_id, "Front")

    row = 4
    net_id = net_ids['N-row-4']
    #va = Vec2(206.004961, 136.307241)
    va = Vec2(207.255667, 136.086708)
    vb = Vec2(208.5334, 133.282236)
    Segment(va, vb).print(net_id, "Back")
    v2 = Vec2(207.255667, 136.086708)
    v3 = bar(v2.x, v2.y, 0, -17.78, -10)
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    v4 = bar(v3.x, v3.y, -2.54, 0, -10)
    v5 = bar(v4.x, v4.y, 0, -17.78, -10)
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Front")
    v6 = bar(v5.x, v5.y, -1.27, 0, -10)
    v7 = Vec2(175 + (175 - 154.486), 91.44)
    Segment(v5, v6).print(net_id, "Front")
    Segment(v6, v7).print(net_id, "Front")
    v8 = Vec2(180.08, 91.44)
    Segment(v7, v8).print(net_id, "Front")



def print_column_attachment_segments(switches):
    y1 = 9.525 - 1.27
    y2 = 9.525
    y3 = 9.525 + 1.27
    x = 7.62
    col_x = -3.255

    # Columns 0, 1, and 2 are attached to the center between rows 2 and 3
    r = 2

    # Column 0
    net_id = net_ids['/col0']
    vectors = []
    vectors.append(project_from_switch(switches[r][0], col_x, y3))
    vectors.append(project_from_switch(switches[r][0], x, y3))
    for c in range(1,6):
        vectors.append(project_from_switch(switches[r][c], -x, y3))
        vectors.append(project_from_switch(switches[r][c],  x, y3))
    vectors.append(Vec2(138.43 + (1.27 * 0), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37))
    vectors.append(Vec2(149.24, 112.37))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 1
    net_id = net_ids['/col1']
    vectors = []
    vectors.append(project_from_switch(switches[r][1], col_x, y2))
    vectors.append(project_from_switch(switches[r][1], x, y2))
    for c in range(2,6):
        vectors.append(project_from_switch(switches[r][c], -x, y2))
        vectors.append(project_from_switch(switches[r][c],  x, y2))
    vectors.append(Vec2(138.43 + (1.27 * 1), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    vectors.append(Vec2(vectors[-1].x, 112.37 + (.8 * 1)))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'F.Cu')
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    vectors.append(Vec2(149.24, vectors[-1].y))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 2
    net_id = net_ids['/col2']
    vectors = []
    vectors.append(project_from_switch(switches[r][2], col_x, y1))
    vectors.append(project_from_switch(switches[r][2], x, y1))
    for c in range(3,6):
        vectors.append(project_from_switch(switches[r][c], -x, y1))
        vectors.append(project_from_switch(switches[r][c],  x, y1))
    vectors.append(Vec2(138.43 + (1.27 * 2), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    vectors.append(Vec2(vectors[-1].x, 112.37 + (.8 * 2)))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'F.Cu')
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    vectors.append(Vec2(149.24, vectors[-1].y))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Columns 3, 4, and 5 are attached to the center between rows 1 and 2
    r = 1

    # Column 3
    net_id = net_ids['/col3']
    vectors = []
    vectors.append(project_from_switch(switches[r][3], col_x, y3))
    vectors.append(project_from_switch(switches[r][3], x, y3))
    for c in range(4,6):
        vectors.append(project_from_switch(switches[r][c], -x, y3))
        vectors.append(project_from_switch(switches[r][c],  x, y3))
    vectors.append(Vec2(138.43 + (1.27 * 3), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    vectors.append(Vec2(vectors[-1].x, 112.37 + (.8 * 3)))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'F.Cu')
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    vectors.append(Vec2(149.24, vectors[-1].y))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 4
    net_id = net_ids['/col4']
    vectors = []
    vectors.append(project_from_switch(switches[r][4], col_x, y2))
    vectors.append(project_from_switch(switches[r][4], x, y2))
    for c in range(5,6):
        vectors.append(project_from_switch(switches[r][c], -x, y2))
        vectors.append(project_from_switch(switches[r][c],  x, y2))
    vectors.append(Vec2(138.43 + (1.27 * 4), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    vectors.append(Vec2(vectors[-1].x, 112.37 + (.8 * 4 )))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'F.Cu')
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    vectors.append(Vec2(149.24, vectors[-1].y))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 5
    net_id = net_ids['/col5']
    vectors = []
    vectors.append(project_from_switch(switches[r][5], col_x, y1))
    vectors.append(project_from_switch(switches[r][5], x, y1))
    vectors.append(Vec2(138.43 + (1.27 * 5), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    vectors.append(Vec2(vectors[-1].x, 112.37 + (.8 * 5)))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'F.Cu')
    print_via(vectors[-1].x, vectors[-1].y, net_id)
    vectors.append(Vec2(149.24, vectors[-1].y))
    Segment(vectors[-2], vectors[-1]).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Columns 9, 10, and 11 are attached to the center between rows 2 and 3
    r = 1

    # Column 9
    net_id = net_ids['/col9']
    vectors = []
    vectors.append(project_from_switch(switches[r][9], col_x, y1))
    vectors.append(project_from_switch(switches[r][9], -x, y1))
    vectors.append(Vec2(231.57 - (1.27 * 5), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 10
    net_id = net_ids['/col10']
    vectors = []
    vectors.append(project_from_switch(switches[r][10], col_x, y2))
    vectors.append(project_from_switch(switches[r][10], -x, y2))
    for c in [9]:
        vectors.append(project_from_switch(switches[r][c],  x, y2))
        vectors.append(project_from_switch(switches[r][c], -x, y2))
    vectors.append(Vec2(231.57 - (1.27 * 4), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 11
    net_id = net_ids['/col11']
    vectors = []
    vectors.append(project_from_switch(switches[r][11], col_x, y3))
    vectors.append(project_from_switch(switches[r][11], -x, y3))
    for c in [10,9]:
        vectors.append(project_from_switch(switches[r][c],  x, y3))
        vectors.append(project_from_switch(switches[r][c], -x, y3))
    vectors.append(Vec2(231.57 - (1.27 * 3), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Columns 12, 13, and 14 are attached to the center between rows 2 and 3
    r = 2

    # Column 12
    net_id = net_ids['/col12']
    vectors = []
    vectors.append(project_from_switch(switches[r][12], col_x, y1))
    vectors.append(project_from_switch(switches[r][12], -x, y1))
    for c in [11,10,9]:
        vectors.append(project_from_switch(switches[r][c],  x, y1))
        vectors.append(project_from_switch(switches[r][c], -x, y1))
    vectors.append(Vec2(231.57 - (1.27 * 2), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 13
    net_id = net_ids['/col13']
    vectors = []
    vectors.append(project_from_switch(switches[r][13], col_x, y2))
    vectors.append(project_from_switch(switches[r][13], -x, y2))
    for c in [12,11,10,9]:
        vectors.append(project_from_switch(switches[r][c],  x, y2))
        vectors.append(project_from_switch(switches[r][c], -x, y2))
    vectors.append(Vec2(231.57 - (1.27 * 1), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)

    # Column 14
    net_id = net_ids['/col14']
    vectors = []
    vectors.append(project_from_switch(switches[r][14], col_x, y3))
    vectors.append(project_from_switch(switches[r][14], -x, y3))
    for c in [13,12,11,10,9]:
        vectors.append(project_from_switch(switches[r][c],  x, y3))
        vectors.append(project_from_switch(switches[r][c], -x, y3))
    vectors.append(Vec2(231.57 - (1.27 * 0), vectors[len(vectors) - 1].y))
    vectors.append(Vec2(vectors[len(vectors) - 1].x, 112.37 - 1.27))
    for i in range(0, len(vectors) - 1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        Segment(v1, v2).print(net_id, 'B.Cu')
    print_via(vectors[0].x, vectors[0].y, net_id)




def print_mosfet_attachment_segments(switches):
    r = 4
    for c in [1,2,3,4,5,7,8,9,10,11,12]:
        s = switches[r][c]
        v1 = foo(s, -8.335, 7.7)
        v2 = foo(s, 8.335, 7.7)
        Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    for c in [0,1,2,3,4,5,7,8,9,10,11,12]:
        s = switches[r][c]
        v1 = foo(s, 8.335, 7.7)
        v2 = foo(s, 8.335, -3.18)
        Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    for c in [0,1,2,3,4]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 8.335, 7.7)
        v2 = foo(s2, -8.335, 7.7)
        Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    for c in [7,8,9,10,11]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 8.335, 7.7)
        v2 = foo(s2, -8.335, 7.7)
        Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    for r in [1,2]:
        s = switches[r][6]
        v1 = foo(s, -8.335, 7.7)
        v2 = foo(s, 8.335, 7.7)
        Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    s1 = switches[4][5]
    s2 = switches[1][6]
    v1 = foo(s1, 8.335, 7.7)
    v2 = foo(s2, -8.335, 7.7)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    s1 = switches[1][6]
    s2 = switches[2][6]
    v1 = foo(s1, 8.335, 7.7)
    v2 = foo(s2, -8.335, 7.7)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    s1 = switches[2][6]
    s2 = switches[4][7]
    v1 = foo(s1, 8.335, 7.7)
    v2 = foo(s2, -8.335, 7.7)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    v1 = Vec2(162.471574, 131.177669)
    v2 = Vec2(160.582282, 141.892377)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    v1 = Vec2(203.945171, 128.282954)
    v2 = Vec2(205.834464, 138.997662)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")

    v1 = Vec2(183.335, 102.82)
    v2 = Vec2(183.335, 141.892377)
    Segment(v1, v2).print(net_ids['N-MOSFET-0'], "Front")



def print_vcc_attachment_segments(switches):
    r = 0
    for c in [0,1,2,3,4,5,7,8,9,10,11,12]:
        s = switches[r][c]
        if c == 0 or c == 7:
            v1 = foo(s, -7.065, -7.065)
        else:
            v1 = foo(s, -7.7, -7.065)
        if c == 12:
            v2 = foo(s, -7.065, -7.065)
        else:
            v2 = foo(s, 7.7, -7.065)
        Segment(v1, v2).print(net_ids['N-5V-0'], "Front")

    for c in [0,1,2,3,4,5,7,8,9,10,11,12]:
        s = switches[r][c]
        v1 = foo(s, -7.065, -3.81)
        v2 = foo(s, -7.065, -7.065)
        Segment(v1, v2).print(net_ids['N-5V-0'], "Front")

    for c in [0,1,2,3,4]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 7.7, -7.065)
        v2 = foo(s2, -7.7, -7.065)
        Segment(v1, v2).print(net_ids['N-5V-0'], "Front")

    for c in [7,8,9,10,11]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 7.7, -7.065)
        v2 = foo(s2, -7.7, -7.065)
        Segment(v1, v2).print(net_ids['N-5V-0'], "Front")

    v1 = Vec2(167.935, 102.19)
    v2 = Vec2(167.935, 123.825)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Front")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    s = switches[1][6]
    v1 = foo(s, -1.27, -5.08)
    v2 = Vec2(154.015, 123.825)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Front")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    s = switches[2][6]
    v1 = foo(s, -1.27, -5.08)
    v2 = Vec2(193.406, 123.825)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Front")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    v1 = Vec2(154.015, 123.825)
    v2 = Vec2(193.406, 123.825)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")

    v1 = Vec2(193.406, 123.825)
    v2 = Vec2(203.2, 123.825)
    v3 = Vec2(206.725, 123.026)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    Segment(v2, v3).print(net_ids['N-5V-0'], "Back")

    # RGB 1
    v1 = Vec2(74.657058, 46.496823)
    #v2 = Vec2(84.096, 48.161)
    v2 = Vec2(84.595, 45.329)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 2
    v1 = Vec2(59.432942, 105.195177)
    v2 = Vec2(54.839, 104.385)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 3
    v1 = Vec2(113.567058, 45.233823)
    v2 = Vec2(122.507, 49.73)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 4
    v1 = Vec2(98.342942, 103.933177)
    v2 = Vec2(93.749, 103.123)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 5
    v1 = Vec2(149.178058, 62.683823)
    v2 = bar(v1.x, v1.y, 2.54, 0, 10)
    v3 = Vec2(139.857, 61.04)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    Segment(v2, v3).print(net_ids['N-5V-0'], "Front")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 6
    v1 = Vec2(133.953942, 121.382177)
    v2 = Vec2(129.36, 120.572)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 7
    v1 = Vec2(205.549019, 61.850312)
    v2 = Vec2(214.156, 55.466)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 8
    v1 = Vec2(211.318981, 122.215688)
    v2 = Vec2(206.725, 123.026)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 9
    v1 = Vec2(241.160019, 44.400312)
    v2 = Vec2(250.932, 44.624)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 10
    v1 = Vec2(246.929981, 104.766688)
    v2 = Vec2(242.336, 105.577)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 11
    v1 = Vec2(280.070019, 45.663312)
    v2 = Vec2(289.51, 43.999)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # RGB 12
    v1 = Vec2(285.839981, 106.028688)
    v2 = Vec2(281.246, 106.839)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Back")
    print_via(v2.x, v2.y, net_ids['N-5V-0'])

    # Attach left half to controller VCC pin
    v1 = Vec2(156.991844, 48.890424)
    v2 = Vec2(167.38, 58.6)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Front")

    # Attach right half to controller VCC pin
    v1 = Vec2(194.198734, 51.985707)
    v2 = Vec2(189.23, 48.26)
    v3 = Vec2(180.34, 48.26)
    v4 = Vec2(170.18, 58.42)
    v5 = Vec2(167.38, 58.6)
    Segment(v1, v2).print(net_ids['N-5V-0'], "Front")
    Segment(v2, v3).print(net_ids['N-5V-0'], "Front")
    Segment(v3, v4).print(net_ids['N-5V-0'], "Front")
    Segment(v4, v5).print(net_ids['N-5V-0'], "Front")


def print_gnd_attachment_segments(switches):
    net_id = net_ids['N-GND-0']
    r = 0
    y = -8.335
    for c in [1,2,3,4,5,7,8,9,10,11]:
        s = switches[r][c]
        v1 = foo(s, -7.7, y)
        if c == 1:
            v1 = foo(s, -8.335, y)
        v2 = foo(s, 7.7, y)
        Segment(v1, v2).print(net_id, "Back")

    for c in [1,2,3,4]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 7.7, y)
        v2 = foo(s2, -7.7, y)
        Segment(v1, v2).print(net_id, "Back")

    for c in [7,8,9,10,11]:
        s1 = switches[r][c]
        s2 = switches[r][c+1]
        v1 = foo(s1, 7.7, y)
        v2 = foo(s2, -7.7, y)
        if c == 11:
            v2 = Vec2(285.444, 28.256)
        Segment(v1, v2).print(net_id, "Back")

    # RGB 1
    c = 1
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = foo(s, -8.335, y)
    v3 = Vec2(63.512, 47.883)
    v4 = Vec2(69.356942, 48.913177)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 2
    c = 2
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(86.09, 29.536)
    v3 = Vec2(73.242, 102.403)
    v4 = Vec2(64.733058, 102.778823)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 3
    c = 3
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(105.659, 28.263)
    v3 = Vec2(102.422, 46.62)
    v4 = Vec2(108.266942, 47.650177)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 4
    c = 4
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(123.71, 35.595)
    v3 = Vec2(111.832, 102.961)
    # Hacky workaround for trace collision
    v4 = Vec2(111.125, 104.14)
    v5 = Vec2(103.643058, 101.516823)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v4.x, v4.y, net_id)

    # RGB 5
    c = 5
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(141.572, 43.999)
    v3 = Vec2(138.033, 64.07)
    v4 = Vec2(143.877942, 65.100177)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 6
    # We have to do some hacky stuff here because we can't run ground down
    # column 6
    v1 = Vec2(138.033, 64.07)
    v2 = Vec2(128.396, 118.727)
    v3 = bar(v2.x, v2.y, 2.54, 0, 10)
    v4 = bar(v3.x, v3.y, 11, 0, 10)
    v5 = Vec2(139.254058, 118.965823)
    #v5 = Vec2(TODO, TODO)
    #v2 = Vec2(136.604, 120.174)
    #v3 = bar(136.604, 120.174, -10, 0, 10)
    Segment(v1, v2).print(net_id, "Front")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Back")
    print_via(v3.x, v3.y, net_id)
    Segment(v3, v4).print(net_id, "Front")
    print_via(v4.x, v4.y, net_id)
    Segment(v4, v5).print(net_id, "Back")
    #Segment(v3, v5).print(net_id, "Front")
    #v6 = bar(v5.x, v5.y, 13.5, 0, 10)
    #Segment(v5, v6).print(net_id, "Front")
    #print_via(v6.x, v6.y, net_id)
    #v7 = Vec2(139.254058, 118.965823)
    #Segment(v6, v7).print(net_id, "Back")

    # RGB 7
    c = 7
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(192.205, 47.995)
    v3 = Vec2(195.55, 66.964)
    v4 = Vec2(201.394981, 65.933688)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 8
    c = 8
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(210.205, 40.375)
    v3 = Vec2(223.084, 113.413)
    v4 = Vec2(215.473019, 118.132312)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 9
    c = 9
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(227.955, 31.329)
    v3 = Vec2(231.367, 50.683)
    v4 = Vec2(237.005981, 48.483688)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 10
    c = 10
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(247.251, 31.06)
    v3 = Vec2(259.273, 99.239)
    v4 = Vec2(258.445, 100.33)
    v5 = Vec2(251.084019, 100.683312)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Front")
    Segment(v4, v5).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v4.x, v4.y, net_id)

    # RGB 11
    c = 11
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(266.593, 31.05)
    v3 = Vec2(270.071, 50.777)
    v4 = Vec2(275.915981, 49.746688)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # RGB 11
    c = 12
    s = switches[r][c]
    v1 = foo(s, -8.335, 0)
    v2 = Vec2(285.444, 28.256)
    v3 = Vec2(298.183, 100.501)
    v4 = Vec2(289.994019, 101.945312)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v1, v3).print(net_id, "Front")
    Segment(v3, v4).print(net_id, "Back")
    print_via(v1.x, v1.y, net_id)
    print_via(v3.x, v3.y, net_id)

    # Attach left half to controller GND pin
    v1 = Vec2(157.212377, 47.639718)
    v2 = Vec2(158.23, 48.26)
    v3 = Vec2(167.38, 53.52)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v2, v3).print(net_id, "Back")

    # Attach right half to controller GND pin
    v1 = Vec2(192.787623, 47.639718)
    v2 = Vec2(191.77, 48.26)
    v3 = Vec2(182.62, 56.06)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v2, v3).print(net_id, "Back")

    # Attach controller GND pins together
    v1 = Vec2(175, 53.52)
    v2 = Vec2(175, 58.6)
    Segment(v1, v2).print(net_id, "Back")
    v1 = Vec2(167.38, 53.52)
    v2 = Vec2(175, 53.52)
    Segment(v1, v2).print(net_id, "Back")
    v1 = Vec2(182.62, 56.06)
    v2 = Vec2(175, 56.06)
    Segment(v1, v2).print(net_id, "Back")
    v1 = Vec2(182.62, 58.6)
    v2 = Vec2(175, 58.6)
    Segment(v1, v2).print(net_id, "Back")


def print_rgb_data_attachment_segments(switches):
    net_id = net_ids['N-RGB-D0']
    v1 = Vec2(182.3914, 78.92)
    v2 = Vec2(191.958672, 78.92)
    v3 = Vec2(191.958672, 64.246657)
    v4 = Vec2(200.821942, 62.683823)
    Segment(v1, v2).print(net_id, "Front")
    Segment(v2, v3).print(net_id, "Front")
    print_via(v3.x, v3.y, net_id)
    Segment(v3, v4).print(net_id, "Back")

    net_id = net_ids['N-RGB-D1']
    v1 = Vec2(206.122058, 65.100177)
    v2 = Vec2(236.432942, 45.233823)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D2']
    v1 = Vec2(241.733058, 47.650177)
    v2 = Vec2(275.342942, 46.496823)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D3']
    v1 = Vec2(69.929981, 45.663312)
    v4 = Vec2(60.005981, 101.945312)
    v2 = bar(v1.x, v1.y, -7.125, 0, 10)
    v3 = bar(v4.x, v4.y, -7.125, 0, 10)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    print_via(v3.x, v3.y, net_id)
    Segment(v3, v4).print(net_id, "Back")

    net_id = net_ids['N-RGB-D4']
    v1 = Vec2(251.657058, 103.933177)
    v2 = Vec2(285.266942, 102.778823)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D5']
    v1 = Vec2(216.046058, 121.382177)
    v2 = Vec2(246.356942, 101.516823)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D6']
    v1 = Vec2(138.681019, 122.215688)
    v2 = bar(v1.x, v1.y, 5, 0, 10)
    v3 = Vec2(151.765, 122.555)
    v4 = Vec2(198.235, 122.555)
    v6 = Vec2(210.745942, 118.965823)
    v5 = bar(v6.x, v6.y, -5, 0, 10)
    Segment(v1, v2).print(net_id, "Back")
    Segment(v2, v3).print(net_id, "Back")
    Segment(v3, v4).print(net_id, "Back")
    Segment(v4, v5).print(net_id, "Back")
    Segment(v5, v6).print(net_id, "Back")

    net_id = net_ids['N-RGB-D7']
    v1 = Vec2(103.070019, 104.766688)
    v2 = Vec2(134.526981, 118.132312)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D8']
    v1 = Vec2(64.160019, 106.028688)
    v2 = Vec2(98.915981, 100.683312)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D9']
    v1 = Vec2(280.643058, 48.913177)
    v4 = Vec2(290.567058, 105.195177)
    v2 = bar(v1.x, v1.y, 7.125, 0, -10)
    v3 = bar(v4.x, v4.y, 7.125, 0, -10)
    Segment(v1, v2).print(net_id, "Back")
    print_via(v2.x, v2.y, net_id)
    Segment(v2, v3).print(net_id, "Front")
    print_via(v3.x, v3.y, net_id)
    Segment(v3, v4).print(net_id, "Back")

    net_id = net_ids['N-RGB-D10']
    v1 = Vec2(74.084019, 49.746688)
    v2 = Vec2(108.839981, 44.400312)
    Segment(v1, v2).print(net_id, "Back")

    net_id = net_ids['N-RGB-D11']
    v1 = Vec2(112.994019, 48.483688)
    v2 = Vec2(144.450981, 61.850312)
    Segment(v1, v2).print(net_id, "Back")


def main():
    raw_switch_data = []
    with open('switches.json', 'r') as f:
        raw_switch_data = json.loads(f.read())

    switches = {}
    for switch in raw_switch_data:
        row = switch['row']
        column = switch['column']

        if not row in switches:
            switches[row] = {}
        switches[row][column] = switch

    column_segments = calculate_column_segments(switches)
    print_column_segments(column_segments)
    print_column_attachment_segments(switches)

    print_switch_to_diode_segments(switches)

    print_row_segments(switches)
    #print_diode_to_row_components(switches)
    #print_row_attachment_segments(switches)

    #vcc_column_segments = calculate_vcc_column_segments(switches)
    #print_vcc_column_segments(vcc_column_segments)
    #print_switch_to_vcc_column_segments(switches)



    #print_mosfet_attachment_segments(switches)
    #print_vcc_attachment_segments(switches)
    #print_gnd_attachment_segments(switches)

    #print_rgb_data_attachment_segments(switches)



if __name__ == '__main__':
    main()

