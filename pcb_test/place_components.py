#!/usr/bin/env python3


import os
import json
import re
import math


SCRIPT_PATH = os.path.abspath(__file__)
foo = os.path.dirname(SCRIPT_PATH)
baz = os.path.dirname(foo)

REPO_DIR = baz

# index => (column, row)
pos_lookup_table = {
     '1':  (0,0),  '2':  (0,1),  '3':  (0,2),  '4':  (0,3),  '5':  (0,4),  '6':  (0,5),
     '7':  (1,0),  '8':  (1,1),  '9':  (1,2), '10':  (1,3), '11':  (1,4), '12':  (1,5),
    '13':  (2,0), '14':  (2,1), '15':  (2,2), '16':  (2,3), '17':  (2,4), '18':  (2,5),
    '19':  (3,0), '20':  (3,1), '21':  (3,2), '22':  (3,3), '23':  (3,4), '24':  (3,5),
    '25':  (4,0), '26':  (4,1), '27':  (4,2), '28':  (4,3), '29':  (4,4), '30':  (4,5),
    '31':  (5,0), '32':  (5,1), '33':  (5,2), '34':  (5,3), '35':  (5,4), '36':  (5,5),
    '37':  (6,0), '38':  (6,1), '39':  (6,2),               '40':  (6,3), '41':  (6,4),
    '42':  (7,0), '43':  (7,1), '44':  (7,2),               '45':  (7,3), '46':  (7,4),
    '47':  (8,0), '48':  (8,1), '49':  (8,2),               '50':  (8,3), '51':  (8,4),
    '52':  (9,0), '53':  (9,1), '54':  (9,2), '55':  (9,3), '56':  (9,4), '57':  (9,5),
    '58': (10,0), '59': (10,1), '60': (10,2), '61': (10,3), '62': (10,4), '63': (10,5),
    '64': (11,0), '65': (11,1), '66': (11,2), '67': (11,3), '68': (11,4), '69': (11,5),
    '70': (12,0), '71': (12,1), '72': (12,2), '73': (12,3), '74': (12,4), '75': (12,5),
    '76': (13,0), '77': (13,1), '78': (13,2), '79': (13,3), '80': (13,4), '81': (13,5),
    '82': (14,0), '83': (14,1), '84': (14,2), '85': (14,3), '86': (14,4), '87': (14,5),
}


def get_switch(ref, switch_data):
    (c, r) = pos_lookup_table[ref]
    for s in switch_data:
        if s['row'] == r and s['column'] == c:
            return s


def get_switch_data():
    switch_data_file = os.path.join(REPO_DIR, 'switches.json')
    with open(switch_data_file) as f:
        return json.loads(f.read())

def get_pcb_data():
    pcb_data_file = os.path.join(REPO_DIR, 'pcb_test', 'bloomer.kicad_pcb')
    with open(pcb_data_file) as f:
        return f.readlines()

def switch_module_get_ref(pcb_data, i):
    ref_offset = 5
    match = re.search(r'reference K([0-9]{1,2})', pcb_data[i+ref_offset])
    if not match:
        raise Exception('Couldn\'t determine switch module reference')
    return match.group(1)

def switch_module_set_pos(pcb_data, i, s):
    at_offset = 1 # Offset from first line to the '(at X Y)' line
    at_line = pcb_data[i+at_offset]
    match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', at_line)
    if not match:
        raise Exception('Couldn\'t determine switch module reference')
    x = match.group(1)
    y = match.group(2)
    at_line = at_line.replace(x, '{}'.format(s['x']))
    at_line = at_line.replace(y, '{}'.format(s['y']))
    at_line = at_line.replace(')', ' {})'.format(0 - s['rotation']))
    pcb_data[i+at_offset] = at_line

def process_switch_module(switch_data, pcb_data, i):
    # Ensure module line count
    match = re.search(r'^ *\) *$', pcb_data[i+46])
    if not match:
        raise Exception('Module line count doesn\'t match expected!')

    # Get the reference, i.e. K1 -> 1
    ref = switch_module_get_ref(pcb_data, i)

    # Get the switch data corresponding to this switch module
    s = get_switch(ref, switch_data)

    # Update the module's position
    switch_module_set_pos(pcb_data, i, s)

    j = 2
    while j < 46:
        line = pcb_data[i+j]

        # Add rotation to lines with "(at X Y)"
        match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
        if match:
            pcb_data[i+j] = line.replace(
                '(at {} {})'.format(match.group(1), match.group(2)),
                '(at {} {} {})'.format(match.group(1), match.group(2), 0 - s['rotation']))
        else:
            # Add rotation to lines with "(at X Y R)"
            match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
            if match:
                print('Replacing line {}:'.format(i+j+1))
                print('(at {} {} {})'.format(match.group(1), match.group(2), match.group(3)))
                print('With:')
                print('(at {} {} {})'.format(match.group(1), match.group(2), float(match.group(3)) - s['rotation']))

                pcb_data[i+j] = line.replace(
                    '(at {} {} {})'.format(match.group(1), match.group(2), match.group(3)),
                    '(at {} {} {})'.format(match.group(1), match.group(2), float(match.group(3)) - s['rotation']))
        
        j += 1
    
def diode_module_get_ref(pcb_data, i):
    ref_offset = 4
    match = re.search(r'reference D([0-9]{1,2})', pcb_data[i+ref_offset])
    if not match:
        raise Exception('Couldn\'t determine diode module reference')
    return match.group(1)

def diode_module_set_pos(pcb_data, i, s):
    at_offset = 1
    at_line = pcb_data[i + at_offset]
    match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', at_line)
    if not match:
        raise Exception('TODO')

    x = match.group(1)
    y = match.group(2)

    x_new = None
    y_new = None
    rot = None
    if s['rotation'] == 0.0:
        x_new = s['x'] + 8.0
        y_new = s['y'] + 0
        rot = 90
    elif s['rotation'] == 10.0:
        x_new = s['x'] + 7.878462024097664
        y_new = s['y'] + 1.389185421335443
        rot = 80
    elif s['rotation'] == -10.0:
        x_new = s['x'] + 7.878462024097664
        y_new = s['y'] - 1.389185421335443
        rot = 100
    else:
        raise Exception('TODO')

    pcb_data[i + at_offset] = at_line.replace(
        '(at {} {})'.format(x, y),
        '(at {} {} {})'.format(x_new, y_new, rot))

    return rot

def process_diode_module(switch_data, pcb_data, i):
    # Ensure module line count
    match = re.search(r'^ *\) *$', pcb_data[i+31])
    if not match:
        raise Exception('Module line count doesn\'t match expected!')

    # Get the reference, i.e. D1 -> 1
    ref = diode_module_get_ref(pcb_data, i)

    # Get the switch data corresponding to this diode module
    s = get_switch(ref, switch_data)

    # Update the module's position
    rot = diode_module_set_pos(pcb_data, i, s)

    j = 2
    while j < 31:
        line = pcb_data[i+j]

        # Add rotation to lines with "(at X Y)"
        match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
        if match:
            pcb_data[i+j] = line.replace(
                '(at {} {})'.format(match.group(1), match.group(2)),
                '(at {} {} {})'.format(match.group(1), match.group(2), rot))
        else:
            # Add rotation to lines with "(at X Y R)"
            match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
            if match:
                # We shouldn't encounter this
                raise Exception('TODO')
        
        j += 1
    
def led_module_get_ref(pcb_data, i):
    ref_offset = 6
    match = re.search(r'reference L([0-9]{1,2})', pcb_data[i+ref_offset])
    if not match:
        raise Exception('Couldn\'t determine LED module reference')
    return match.group(1)
    

def process_led_module(pcb_data, i):
    # Ensure module line count
    match = re.search(r'^ *\) *$', pcb_data[i+44])
    if not match:
        raise Exception('Module line count doesn\'t match expected!')

    lookup = {
        '1':   190, '2':   190, '3':   190,
        '4':    10, '5':    10, '6':    10,
        '7':   -10, '8':   -10, '9':   -10,
        '10': -190, '11': -190, '12': -190,
    }

    # Get the reference, i.e. K1 -> 1
    ref = led_module_get_ref(pcb_data, i)
    rot = lookup[ref]

    j = 2
    while j < 44:
        line = pcb_data[i+j]

        # Add rotation to lines with "(at X Y)"
        match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
        if match:
            pcb_data[i+j] = line.replace(
                '(at {} {})'.format(match.group(1), match.group(2)),
                '(at {} {} {})'.format(match.group(1), match.group(2), rot))
        else:
            # Add rotation to lines with "(at X Y R)"
            match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+) ([0-9\-\.]+)\)', line)
            if match:
                # We shouldn't encounter this
                raise Exception('TODO')
        
        j += 1


def main():
    switch_data = get_switch_data()
    pcb_data = get_pcb_data()

    x = 20
    y = -20
    for i in range(0, len(pcb_data)):
        line = pcb_data[i]

        #match = re.search(r'\(module keebs:Mx_Alps_100', line)
        #if match:
            #process_switch_module(switch_data, pcb_data, i)
            #continue

        #match = re.search(r'\(module keyboard_parts:D_SOD123_axial', line)
        #if match:
            #process_diode_module(switch_data, pcb_data, i)
            #continue

        #match = re.search(r'\(module LED_SMD:LED_WS2812B_PLCC4_5', line)
        #if match:
            #process_led_module(pcb_data, i)

        #match = re.search(r'\(module ', line)
        #if match:
            #match = re.search(r'\(at ([0-9\-\.]+) ([0-9\-\.]+)\)', pcb_data[i+1])
            #if match:
                #print("Replacing:")
                #print('(at {} {})'.format(match.group(1), match.group(2)))
                #print("With:")
                #print('(at {} {})'.format(x, y))
                #pcb_data[i+1] = pcb_data[i+1].replace(
                    #'(at {} {})'.format(match.group(1), match.group(2)),
                    #'(at {} {})'.format(x, y))
                #x += 10
                #if x > 200:
                    #x = 20
                    #y += 10



    with open('bloomer.test.kicad_pcb', 'w') as f:
        f.writelines(pcb_data)
    

if __name__ == '__main__':
    main()
