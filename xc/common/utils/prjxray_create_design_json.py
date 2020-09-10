import argparse
import prjxray.db
from prjxray.roi import Roi
import simplejson as json
from functools import partial
from prjxray_create_synth_tiles import map_tile_to_vpr_coord, tile_in_roi, wire_in_roi, wire_manhattan_distance, find_wire_from_node

from prjxray_db_cache import DatabaseCache


def determine_node_type(conn, roi, node_name):
    tile, _ = node_name.split('/')

    x, y = map_tile_to_vpr_coord(conn, tile)
    
    if x >= roi.x1 and x <= roi.x2 and y >= roi.y1 and y <= roi.y2:
        return 'out'
    else:
        return 'in'


def split_node_list(conn, roi, nodes):
    inputs = list()
    outputs = list()
    for n in nodes:
        node_type = determine_node_type(conn, roi, n[6])
        if node_type == 'in':
            inputs.append(n)
        elif node_type == 'out':
            outputs.append(n)
        else:
            assert False, node_type + ' is an invalid node type'
    return (inputs, outputs)


def get_nodes(conn):
    if get_nodes.nodes == None:
        c = conn.cursor()
        c.execute("""
SELECT graph_node.pkey,graph_node.node_pkey,graph_node.x_low,
       graph_node.x_high,graph_node.y_low,graph_node.y_high,node.name
FROM graph_node 
INNER JOIN node
ON graph_node.node_pkey = node.pkey
ORDER BY graph_node.node_pkey
        """)
        get_nodes.nodes = c.fetchall()

    return get_nodes.nodes
get_nodes.nodes = None


def convert_from_canon_to_vpr_coord(conn, grid_x, grid_y):
    c = conn.cursor()
    c.execute("""
SELECT name FROM phy_tile 
WHERE grid_x = ? AND grid_y = ?
    """, (grid_x, grid_y))

    tiles = c.fetchall()
    assert len(tiles) == 1
    x, y = map_tile_to_vpr_coord(conn, tiles[0][0])
    return (x,y)


def choose_partition_pins(conn, g, roi, num_inputs, num_outputs, num_clks, side, pins_per_tile):
    # n[2] = x_low, n[3] = x_high, n[4] = y_low, n[5] = y_high
    if side == 'north':
        func = lambda n, roi: n[2] >= roi[0] and n[3] <= roi[2] \
                and n[4] < roi[1] and n[5] > roi[1] and n[5] < roi[3] and n[6] != None
    elif side == 'south':
        func = lambda n, roi: n[2] >= roi[0] and n[3] <= roi[2] \
                and n[4] < roi[3] and n[5] > roi[3] and n[4] > roi[1] and n[6] != None
    elif side == 'east':
        func = lambda n, roi: n[2] < roi[2] and n[3] > roi[2] \
                and n[2] > roi[0] and n[4] >= roi[1] and n[5] <= roi[3] and n[6] != None
    else:
        func = lambda n, roi: n[2] < roi[0] and n[3] > roi[0] \
                and n[3] < roi[2] and n[4] >= roi[1] and n[5] <= roi[3] and n[6] != None

    x1, y1 = convert_from_canon_to_vpr_coord(conn, roi.x1, roi.y1)
    x2, y2 = convert_from_canon_to_vpr_coord(conn, roi.x2, roi.y2)
    possible_nodes = list(filter(partial(func, roi=(x1,y1,x2,y2)), get_nodes(conn)))

    def filter_bad_nodes(n):
        tile, _ = n[6].split('/')
        return ('IOB' not in tile) and ('BRAM' not in n[6]) and ('DSP' not in n[6]) and ('CLK' not in n[6])

    possible_nodes = list(filter(filter_bad_nodes, possible_nodes))
    inputs, outputs = split_node_list(conn, roi, possible_nodes)
    clock_func = lambda n, roi: ((n[2] < roi.x1 and n[3] > roi.x1) or \
            (n[2] > roi.x1 and n[3] < roi.x1)) \
            and n[4] >= roi.y1 and n[5] <= roi.y2 and n[6] != None and ('BUFHCLK' in n[6])
    possible_clock_nodes = list(filter(partial(clock_func, roi=roi), get_nodes(conn)))

    ports = list()
    if num_clks > 0:
        clocks_remaining = num_clks
        for c in possible_clock_nodes:
            if clocks_remaining == 0:
                break
            if c[6] in choose_partition_pins.nodes_used:
                continue
            ports.append(c[6])
            clocks_remaining -= 1
            choose_partition_pins.nodes_used[c[6]] = True

    inputs_remaining = num_inputs
    for i in inputs:
        if inputs_remaining == 0:
            break;
        node = i[6]
        if node in choose_partition_pins.nodes_used:
            continue
        tile, _ = find_wire_from_node(conn, g, roi, node)
        if tile not in choose_partition_pins.tiles_used or choose_partition_pins.tiles_used[tile] < pins_per_tile:
            if tile not in choose_partition_pins.tiles_used:
                choose_partition_pins.tiles_used[tile] = 1
            else:
                choose_partition_pins.tiles_used[tile] += 1
            ports.append(node)
            inputs_remaining -= 1
            choose_partition_pins.nodes_used[node] = True

    outputs_remaining = num_outputs
    for o in outputs:
        if outputs_remaining == 0:
            break;
        node = o[6]
        if node in choose_partition_pins.nodes_used:
            continue
        tile, _ = find_wire_from_node(conn, g, roi, node)
        if tile not in choose_partition_pins.tiles_used or choose_partition_pins.tiles_used[tile] < pins_per_tile:
            if tile not in choose_partition_pins.tiles_used:
                choose_partition_pins.tiles_used[tile] = 1
            else:
                choose_partition_pins.tiles_used[tile] += 1
            ports.append(node)
            outputs_remaining -= 1
            choose_partition_pins.nodes_used[node] = True
    
    return ports
choose_partition_pins.tiles_used = {}
choose_partition_pins.nodes_used = {}


def create_design(conn, db, g, roi_def):
    with open(roi_def) as f:
        j = json.load(f)

    roi = Roi(
        db=db,
        x1=j['info']['GRID_X_MIN'],
        y1=j['info']['GRID_Y_MIN'],
        x2=j['info']['GRID_X_MAX'],
        y2=j['info']['GRID_Y_MAX']
    )

    pins_per_tile = j['info']['pins_per_tile']

    design = {}
    design['info'] = j['info']
    design['ports'] = list()

    num_ports = 0;
    for port in j['ports']:
        assert port['side'] in ['north', 'south', 'east', 'west'], side
        
        if port['data_type'] == 'scalar':
            num_io = 1
        elif port['data_type'] == 'bus':
            assert 'msb' and 'lsb' in port
            num_io = abs(port['msb'] - port['lsb']) + 1
        else:
            assert False

        num_inputs = 0
        num_outputs = 0
        num_clocks = 0
        if port['type'] == 'clk':
            num_clocks = num_io
        elif port['type'] == 'in':
            num_inputs = num_io
        elif port['type'] == 'out':
            num_outputs = num_io
        else:
            assert False

        part_pins = choose_partition_pins(conn, g, roi, num_inputs, num_outputs, num_clocks, port['side'], pins_per_tile)
        if len(part_pins) != num_io:
            from IPython import embed; embed()
        assert len(part_pins) == num_io

        for i in range(0, num_io):
            p = {}
            if port['data_type'] == 'scalar':
                p['name'] = port['name']
            else:
                p['name'] = port['name'] + '[' + str(i) + ']'
            p['type'] = port['type']
            p['node'] = part_pins.pop()
            p['pin'] = j['info']['name'] + '_SYN' + str(num_ports)
            num_ports += 1
            design['ports'].append(p)

        assert len(part_pins) == 0

    return design


def main():
    parser = argparse.ArgumentParser(description="Generate design.json")
    parser.add_argument('--db_root', required=True)
    parser.add_argument('--part', required=True)
    parser.add_argument('--roi_def', required=False, help='Path to ROI definition json')
    parser.add_argument('--overlay_devices', required=False)
    parser.add_argument(
        '--connection_database', help='Connection database', required=True
    )
    parser.add_argument('--design', required=True)

    args = parser.parse_args()

    db = prjxray.db.Database(args.db_root, args.part)
    g = db.grid()

    if args.roi_def:

        with DatabaseCache(args.connection_database, read_only=True) as conn:
            design = create_design(conn, db, g, args.roi_def)
    elif args.overlay:
        with open(args.overlay) as f:
            j = json.load(f)

    else:
        assert False, 'Design json must be for roi or overlay'

    with open(args.design, 'w') as f:
        json.dump(design, f, indent=2)


if __name__ == "__main__":
    main()
