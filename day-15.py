from intcode import Controller, load_program
import random
from os import system

def update_position(pos, direction, status):
    dx, dy = {
        1: (0, 1),
        2: (0, -1),
        3: (-1, 0),
        4: (1, 0)
    }[direction]

    robot_pos = pos
    tile_pos = (pos[0]+dx, pos[1]+dy)
    
    if status == 0:
        return robot_pos, tile_pos, "█"
    
    robot_pos = tile_pos
    return robot_pos, tile_pos, {1: ".", 2: "O"}[status]

def get_next_direction(pos, status, tiles):
    # for now just randomly traverse the maze
    # ideally this would implement some kind of semi-sophisticated algorithm
    return random.choice([1, 2, 3, 4])

def get_adjacent(pos):
    x, y = pos
    adjacent = (
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1)
    )
    return adjacent

def check_filled(tiles):
    for tile in tiles:
        if tiles[tile] == ".":
            for a in get_adjacent(tile):
                if a not in tiles:
                    return False
    return True

def render_tiles(tiles, robot_pos=-1):
    min_x = min_y = max_x = max_y = 0
    for tile in tiles:
        x, y = tile
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    
    r = ""
    for y in range(min_y, max_y+1):
        s = ""
        for x in range(min_x, max_x+1):
            if (x, y) == (0, 0):
                s += "X"
            elif robot_pos != -1 and (x, y) == robot_pos:
                s += "@"
            else:
                s += tiles.get((x, y), " ")
        r += s + "\n"
    return r

def search_map(program="inputs/day-15.txt", rendering=False):
    controller = Controller(load_program(program))

    start_pos = (0, 0)
    pos = start_pos
    direction = 1
    tiles = {pos: "."}
    generator_position = -1

    while not check_filled(tiles):
        _, _, output_returned = controller.step_until_action(direction)
        if output_returned:
            status = controller.last_output
            pos, tile_pos, tile = update_position(pos, direction, status)
            tiles[tile_pos] = tile
            direction = get_next_direction(pos, tile, tiles)
            if generator_position == -1 and tile == 2:
                generator_position = tile_pos
            if rendering:
                print(render_tiles(tiles, robot_pos=pos) + "\n\n\n")
    
    return tiles, generator_position, start_pos

def load_map(map_file="inputs/day-15-map.txt"):
    rows = open(map_file).readlines()
    tiles = {}
    generator_pos = -1
    start_pos = -1
    for y, row in enumerate(rows):
        for x, col in enumerate(row.replace("\n", "")):
            if col == "O":
                generator_pos = (x, y)
                tiles[(x, y)] = "O"
            elif col == "X":
                start_pos = (x, y)
                tiles[(x, y)] = "."
            else:
                tiles[(x, y)] = col
    return tiles, generator_pos, start_pos

def save_map(tiles, map_file="inputs/day-15-map.txt"):
    with open(map_file, 'w') as f:
        f.write(render_tiles(tiles))

def get_nodes(tiles):
    nodes = {}
    for tile in tiles:
        if tiles[tile] == ".":
            available = set()
            for a in get_adjacent(tile):
                if tiles.get(a, " ") in ".O":
                    available.add(a)
            nodes[tile] = available
    return nodes

def traverse(pos, end_pos, nodes, traversed=-1):
    if traversed == -1:
        traversed = set()
    if pos == end_pos:
        return 0
    adjacent = nodes[pos]
    min_distance = -2
    for node in adjacent:
        if node not in traversed:
            traversed.add(node)
            distance = traverse(node, end_pos, nodes, traversed=traversed.copy())
            if distance != -1:
                min_distance = distance if min_distance == -2 else min(distance, min_distance)
    return min_distance + 1

map_generated = True
if map_generated:
    tiles, generator_pos, start_pos = load_map()
else:
    tiles, generator_pos, start_pos = search_map(rendering=True)
    save_map(tiles)

nodes = get_nodes(tiles.copy()).copy()

print("Map:")
print(render_tiles(tiles) + "\n")

print(f"Part 1: {traverse(start_pos, generator_pos, nodes)}")

# get longest distance from any tile to the generator
distances = set()
for tile in tiles:
    if tiles[tile] in ".OX":
        distances.add(traverse(tile, generator_pos, nodes))
print(f"Part 2: {max(distances)}")