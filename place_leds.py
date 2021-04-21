#!/usr/bin/env python3

import os
import json
import re
import math


SCRIPT_PATH = os.path.abspath(__file__)
REPO_DIR = os.path.dirname(SCRIPT_PATH)

def sw(switch_data, c, r):
    for s in switch_data:
        if s['row'] == r and s['column'] == c:
            return s


def get_switch_data():
    switch_data_file = os.path.join(REPO_DIR, 'switches.json')
    with open(switch_data_file) as f:
        return json.loads(f.read())


def foo(ref, s1, s2, rot):
    dx = s2['x'] - s1['x']
    dy = s2['y'] - s1['y']

    x = round(s1['x'] + (dx / 2), 3)
    y = round(s1['y'] + (dy / 2), 3)

    print('(at {} {} {})'.format(x, y, rot))


def main():
    d = get_switch_data()

    foo('L1', sw(d,9,0), sw(d,9,1), 190)
    foo('L2', sw(d,11,0), sw(d,11,1), 190)
    foo('L3', sw(d,13,0), sw(d,13,1), 190)
    foo('L4', sw(d,13,4), sw(d,13,5), 10)
    foo('L5', sw(d,11,4), sw(d,11,5), 10)
    foo('L6', sw(d,9,4), sw(d,9,5), 10)
    foo('L7', sw(d,5,4), sw(d,5,5), -10)
    foo('L8', sw(d,3,4), sw(d,3,5), -10)
    foo('L9', sw(d,1,4), sw(d,1,5), -10)
    foo('L10', sw(d,1,0), sw(d,1,1), -190)
    foo('L11', sw(d,3,0), sw(d,3,1), -190)
    foo('L12', sw(d,5,0), sw(d,5,1), -190)





if __name__ == '__main__':
    main()
