#!/usr/bin/env python3

"""
Import the top level CLB interconnect information from Project X-Ray database
files.
"""

import argparse
import os
import re
import sys

import lxml.etree as ET


##########################################################################
# Work out valid arguments for Project X-Ray database                    #
##########################################################################
mydir = os.path.dirname(__file__)
prjxray_db = os.path.abspath(os.path.join(mydir, "..", "third_party", "prjxray-db"))

db_types = set()
clb_tiles = set()
for d in os.listdir(prjxray_db):
    if d.startswith("."):
        continue
    dpath = os.path.join(prjxray_db, d)
    if not os.path.isdir(dpath):
        continue

    if not os.path.exists(os.path.join(dpath, "settings.sh")):
        continue

    db_types.add(d)

    for f in os.listdir(dpath):
        fpath = os.path.join(dpath, f)
        if not os.path.isfile(fpath):
            continue
        if not fpath.endswith('.db'):
            continue
        if not f.startswith('ppips_'):
            continue

        assert f.startswith('ppips_')
        assert f.endswith('.db')
        tile = f[len('ppips_'):-len('.db')]

        if not tile.startswith('clb'):
            continue

        assert len(tile.split('_')) == 2, tile.split('_')
        clb_tiles.add(tile.upper())


parser = argparse.ArgumentParser(
    description=__doc__,
    fromfile_prefix_chars='@',
    prefix_chars='-~'
)

parser.add_argument(
    '--part', choices=db_types,
    help="""Project X-Ray database to use.""")

parser.add_argument(
    '--tile', choices=clb_tiles,
    help="""CLB tile to generate for""")

parser.add_argument(
    '--output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
    help="""File to write the output too.""")

args = parser.parse_args()

prjxray_part_db = os.path.join(prjxray_db, args.part)

tile_type, tile_dir = args.tile.split('_')

##########################################################################
# Read in the Project X-Ray database and do some processing              #
##########################################################################
def db_open(n):
    return open(os.path.join(prjxray_part_db, "%s_%s_%s.db" % (n, tile_type.lower(), tile_dir.lower())))

wires_internal = {}

prefix_re = re.compile("^(.*[^0-9])([0-9]+)$")

def process_wire(wire_name):
    """Extract data from the wire name and added to global database."""
    orig_wire_name = wire_name
    assert wire_name.startswith(tile_type), wire_name
    wire_name = wire_name[len(tile_type+'_'):]

    if wire_name.startswith("L_"):
        wire_name = "CLBLL_L."+wire_name[2:]
    elif wire_name.startswith("M_"):
        wire_name = "CLBLL_M."+wire_name[2:]
    elif wire_name.startswith("LL_"):
        wire_name = "CLBLL_LL."+wire_name[3:]

    g = prefix_re.match(wire_name)
    if not g:
        # Have to special case the A, B, C, D out wires as they conflict wit the
        # A/B/C/D LUT input names
        if wire_name[-2:] in (".A", ".B", ".C", ".D"):
            wire_name += "OUT"

        prefix, num = wire_name, None
    else:
        prefix, num = g.groups()
        num = int(num)

    name = prefix

    if name not in wires_internal:
        wires_internal[name] = set()
    wires_internal[name].add(num)
    return name, num


connections = {}

# Read in all the Pseudo PIP definitions.
for line in db_open('ppips').readlines():
    assert line.startswith('%s_%s.' % (tile_type, tile_dir)), line
    name, bits = line.strip().split(' ', maxsplit=1)
    _, net_to, net_from = name.split('.')

    if bits != "always":
        print("Skipping line: %r" % line)
        continue

    net_to = process_wire(net_to)
    net_from = process_wire(net_from)
    connections[net_from] = net_to

# Work out the direction of all wires.
# All wires are uni-directional, so we know the input/output stuff from that.
clbll_inputs = set()
slice_inputs = set()

slice_outputs = set()
clbll_outputs = set()

for name, pins in wires_internal.items():
    if name.startswith("CLBLL_"):
        inputs = slice_outputs
        outputs = slice_inputs
    else:
        inputs = clbll_inputs
        outputs = clbll_outputs

    input = True
    for p in pins:
        if (name, p) in connections:
            assert input == True
        else:
            input = False

    wire = (name, tuple(pins))
    if input:
        inputs.add(wire)
    else:
        outputs.add(wire)

##########################################################################
# Generate the pb_type.xml file                                          #
##########################################################################
def add_direct(xml, input, output):
    ET.SubElement(xml, 'direct', {'name': '%-30s' % output, 'input': '%-30s' % input, 'output': '%-30s' % output})

tile_name = "TILE_%s_%s" % (tile_type, tile_dir)

pb_type_xml = ET.Element(
    'pb_type', {
        'name': tile_name,
        'num_pb': str(1),
    })

def fmt(wire, pin):
    if pin is None:
        return wire
    return '%s[%s]' % (wire, pin)

interconnect_xml = ET.SubElement(pb_type_xml, 'interconnect')

pb_type_xml.append(ET.Comment(" Tile Inputs "))
interconnect_xml.append(ET.Comment(" Tile->Slice "))
for name, pins in sorted(clbll_inputs):
    # Input definitions for the TILE
    ET.SubElement(
        pb_type_xml,
        'input',
        {'name': '%-20s' % name, 'num_pins': str(len(pins))},
    )

    for p in pins:
        # Connections from the TILE to the CLBLL_XX
        add_direct(interconnect_xml, '%s.%s' % (tile_name, fmt(name, p)), fmt(*connections[(name, p)]))


pb_type_xml.append(ET.Comment(" Tile Outputs "))
for name, pins in sorted(clbll_outputs):
    # Output definitions for the TILE
    ET.SubElement(
        pb_type_xml,
        'output',
        {'name': '%-20s' % name, 'num_pins': str(len(pins))},
    )

pb_type_xml.append(ET.Comment(" Internal Slices "))

# CLBLL's have two slices internally.
if tile_type.startswith('CLBLL'):
    # CLBLL's have two SLICELs, one called CLBLL_L and one called CLBLL_LL
    slice0_name = 'CLBLL_L'
    slice0_type = 'SLICEL'
    slice1_name = 'CLBLL_LL'
    slice1_type = 'SLICEL'
elif tile_type.startswith('CLBLM'):
    # CLBLM's have one SLICELs called CLBLL_L and one SLICEM called CLBLL_M
    slice0_name = 'CLBLL_M'
    slice0_type = 'SLICEM'
    slice1_name = 'CLBLL_L'
    slice1_type = 'SLICEL'
else:
    assert False, tile_type

# Internal pb_type definition for the first slice
slice0_xml = ET.SubElement(pb_type_xml, 'pb_type', {'name': slice0_name, 'num_pbs': '1'})
ET.SubElement(slice0_xml, 'xi-include', {'href': '%s.xml' % slice0_type.lower()})
slice0_interconnect_xml = ET.SubElement(slice0_xml, 'interconnect')
slice0_interconnect_xml.append(ET.Comment(" Slice->Cell "))

# Internal pb_type definition for the second slice
slice1_xml = ET.SubElement(pb_type_xml, 'pb_type', {'name': slice1_name, 'num_pbs': '1'})
ET.SubElement(slice1_xml, 'xi-include', {'href': '%s.xml' % slice0_type.lower()})
slice1_interconnect_xml = ET.SubElement(slice1_xml, 'interconnect')
slice1_interconnect_xml.append(ET.Comment(" Slice->Cell "))

for name, pins in sorted(slice_inputs):
    if name.startswith(slice0_name+'.'):
        slice_type = slice0_type
        slice_xml = slice0_xml
        slice_interconnect_xml = slice0_interconnect_xml
    elif name.startswith(slice1_name+'.'):
        slice_type = slice1_type
        slice_xml = slice1_xml
        slice_interconnect_xml = slice1_interconnect_xml
    else:
        assert False, name

    # Input pins for the CLBLL_X
    ET.SubElement(
        slice_xml,
        'input', {'name': ' %-20s' % name, 'num_pins': str(len(pins))},
    )

    # Connections from CLBLL_X type to the contained SLICEL/SLICEM
    for p in pins:
        input_name = fmt(name, p)
        add_direct(slice_interconnect_xml, input_name, '%s.%s' % (slice_type, input_name.split('.')[-1]))

slice0_interconnect_xml.append(ET.Comment(" Cell->Slice "))
slice1_interconnect_xml.append(ET.Comment(" Cell->Slice "))
interconnect_xml.append(ET.Comment(" Slice->Tile "))

for name, pins in sorted(slice_outputs):
    if name.startswith(slice0_name+'.'):
        slice_type = slice0_type
        slice_xml = slice0_xml
        slice_interconnect_xml = slice0_interconnect_xml
    elif name.startswith(slice1_name+'.'):
        slice_type = slice1_type
        slice_xml = slice1_xml
        slice_interconnect_xml = slice1_interconnect_xml
    else:
        assert False

    # Output pins for the CLBLL_X
    ET.SubElement(
        slice_xml,
        'output', {'name': '%-20s' % name, 'num_pins': str(len(pins))},
    )

    for p in pins:
        output_name = fmt(name, p)
        # Connections from SLICEL/SLICEM to the containing CLBLL_X type
        add_direct(slice_interconnect_xml, ('%s.%s' % (slice_type, output_name.split('.')[-1])), output_name)
        # Connections from the CLBLL_XX to the TILE
        add_direct(interconnect_xml, output_name, '%s.%s' % (tile_name, fmt(*connections[(name, p)])))

pb_type_str = ET.tostring(pb_type_xml, pretty_print=True).decode('utf-8')
args.output.write(pb_type_str)
args.output.close()