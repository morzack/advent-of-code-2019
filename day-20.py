import sys
sys.setrecursionlimit(10000)

def get_map_bounds(tiles):
    min_x = min_y = max_x = max_y = 0
    for tile in tiles:
        x, y = tile
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return (min_x, min_y), (max_x, max_y)

def get_adjacent(pos):
    x, y = pos
    return (
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1)
    )

def load_map(input_file="inputs/day-20.txt"):
    tiles_raw = {}
    # divide the torus into horizontal, vertical, and corner pieces and parse appropriately
    with open(input_file, 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, col in enumerate(line.replace("\n", "")):
                tiles_raw[(x, y)] = col
    min_tile, max_tile = get_map_bounds(tiles_raw)
    # NOTE i'm going to end up spamming this algorithm for parsing purposes
    # future me can deal with code reuse
    portals = {}
    # for this algorithm to work we need to know the "thickness" of the maze
    middle = (max_tile[0]//2, max_tile[1]//2)
    dx = 1
    while tiles_raw[(pos := (middle[0]+dx, middle[1]))] not in ".#":
        dx += 1
    thickness = max_tile[0]-middle[0]-dx-1
    def update_portal_location(portals, portal_id, portal_pos):
        current = portals.get(portal_id, set())
        current.add(portal_pos)
        portals[portal_id] = current
        return portals    
    # get portals on left and right
    for y in range(2, max_tile[1]-1):
        if tiles_raw[(0, y)] not in ". #":
            portal_id = f"{tiles_raw[(0, y)]}{tiles_raw[(1, y)]}"
            portals = update_portal_location(portals, portal_id, (2, y))

        if tiles_raw[(max_tile[0]-1, y)] not in ". #":
            portal_id = f"{tiles_raw[(max_tile[0]-1, y)]}{tiles_raw[(max_tile[0], y)]}"
            portals = update_portal_location(portals, portal_id, (max_tile[0]-2, y))

        if tiles_raw[(thickness+2, y)] not in ". #" and tiles_raw[(thickness+3, y)] not in ". #":
            portal_id = f"{tiles_raw[(thickness+2, y)]}{tiles_raw[(thickness+3, y)]}"
            portals = update_portal_location(portals, portal_id, (thickness+1, y))

        if tiles_raw[(max_tile[0]-(thickness+2), y)] not in ". #" and tiles_raw[(max_tile[0]-(thickness+3), y)] not in ". #":
            portal_id = f"{tiles_raw[(max_tile[0]-(thickness+3), y)]}{tiles_raw[(max_tile[0]-(thickness+2), y)]}"
            portals = update_portal_location(portals, portal_id, (max_tile[0]-(thickness+1), y))

    # get portals on top and bottom
    for x in range(2, max_tile[0]-1):
        if tiles_raw[(x, 0)] != " ":
            portal_id = f"{tiles_raw[(x, 0)]}{tiles_raw[(x, 1)]}"
            portals = update_portal_location(portals, portal_id, (x, 2))

        if tiles_raw[(x, max_tile[1]-1)] != " ":
            portal_id = f"{tiles_raw[(x, max_tile[1]-1)]}{tiles_raw[(x, max_tile[1])]}"
            portals = update_portal_location(portals, portal_id, (x, max_tile[1]-2))

        if tiles_raw[(x, thickness+2)] not in ". #" and tiles_raw[(x, thickness+3)] not in ". #":
            portal_id = f"{tiles_raw[(x, thickness+2)]}{tiles_raw[(x, thickness+3)]}"
            portals = update_portal_location(portals, portal_id, (x, thickness+1))
        
        if tiles_raw[(x, max_tile[1]-(thickness+3))] not in ". #" and tiles_raw[(x, max_tile[1]-(thickness+2))] not in ". #":
            portal_id = f"{tiles_raw[(x, max_tile[1]-(thickness+3))]}{tiles_raw[(x, max_tile[1]-(thickness+2))]}"
            portals = update_portal_location(portals, portal_id, (x, max_tile[1]-(thickness+1)))
    # load tiles into something more reasonable
    # MAKE THE PORTALS LINK TO EACH OTHER IN THE NODES THIS IS THE KEY THING TO DO
    portal_locations = set()
    start = (-1, -1)
    end = (-1, -1)
    for i in portals:
        for j in portals[i]:
            if i == "AA":
                start = j
            elif i == "ZZ":
                end = j
            else:
                portal_locations.add(j)
    nodes = {}
    for tile in tiles_raw:
        if tiles_raw[tile] == ".":
            adjacent = set()
            if tile in portal_locations:
                for portal in portals:
                    if tile in portals[portal]:
                        for i in portals[portal]:
                            if i != tile:
                                adjacent.add(i)
            for a in get_adjacent(tile):
                if tiles_raw[a] == ".":
                    adjacent.add(a)
            nodes[tile] = adjacent
    return tiles_raw, nodes, start, end

def get_map_string(tiles, filled=set()):
    min_tile, max_tile = get_map_bounds(tiles)
    s = ""
    for y in range(min_tile[1], max_tile[1]+1):
        for x in range(min_tile[0], max_tile[0]+1):
            if (x, y) in filled:
                s += "@"
            else:
                s += tiles[(x, y)]
        s += "\n"
    return s

def traverse_nodes(tiles, nodes, pos, end, traversed=-1, optimizations={}):
    if traversed == -1:
        traversed = set()
    if pos == end:
        print("solution")
        print(get_map_string(tiles, traversed))
        print(len(traversed) == 604)
        return 0, True
    optimizer_input = frozenset(set([frozenset(traversed), pos]))
    # if optimizer_input in optimizations:
    #     return optimizations[optimizer_input], True
    adjacent = nodes[pos]
    min_distance = 0
    for tile in adjacent:
        if tile not in traversed:
            # print(get_map_string(tiles, traversed))
            next_traversed = traversed.copy()
            next_traversed.add(tile)
            distance, valid = traverse_nodes(tiles, nodes, tile, end, next_traversed, optimizations)
            distance += 1
            if valid:
                if min_distance == 0:
                    min_distance = distance
                else:
                    min_distance = min(distance, min_distance)
    if min_distance == 0:
        return 0, False
    optimizations[optimizer_input] = min_distance
    return min_distance, True

tiles, nodes, start, end = load_map()
distance, possible = traverse_nodes(tiles, nodes, start, end)
print(f"Part 1: {distance}")