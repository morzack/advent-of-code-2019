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

def traverse_nodes(nodes, pos, end, traversed=set()):
    if pos == end:
        return 0, True
    min_distance = 0
    for tile in nodes[pos]:
        if tile not in traversed:
            next_traversed = traversed.copy()
            next_traversed.add(tile)
            distance, valid = traverse_nodes(nodes, tile, end, next_traversed)
            distance += 1
            if valid:
                if min_distance == 0:
                    min_distance = distance
                else:
                    min_distance = min(distance, min_distance)
    if min_distance == 0:
        return 0, False
    return min_distance, True

def get_available_portals(start, inner_portals, outer_portals, nodes):
    # basically a traversal to find portals
    available = {}
    for portal in inner_portals:
        for i in inner_portals[portal]:
            if i != start:
                distance, possible = traverse_nodes(nodes, start, i)
                if possible:
                    available[f"{portal}I"] = distance
    for portal in outer_portals:
        for i in outer_portals[portal]:
            if i != start:
                distance, possible = traverse_nodes(nodes, start, i)
                if possible:
                    available[f"{portal}O"] = distance
    return available

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
    outer_portals = {}
    inner_portals = {}
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
            outer_portals = update_portal_location(outer_portals, portal_id, (2, y))

        if tiles_raw[(max_tile[0]-1, y)] not in ". #":
            portal_id = f"{tiles_raw[(max_tile[0]-1, y)]}{tiles_raw[(max_tile[0], y)]}"
            outer_portals = update_portal_location(outer_portals, portal_id, (max_tile[0]-2, y))

        if tiles_raw[(thickness+2, y)] not in ". #" and tiles_raw[(thickness+3, y)] not in ". #":
            portal_id = f"{tiles_raw[(thickness+2, y)]}{tiles_raw[(thickness+3, y)]}"
            inner_portals = update_portal_location(inner_portals, portal_id, (thickness+1, y))

        if tiles_raw[(max_tile[0]-(thickness+2), y)] not in ". #" and tiles_raw[(max_tile[0]-(thickness+3), y)] not in ". #":
            portal_id = f"{tiles_raw[(max_tile[0]-(thickness+3), y)]}{tiles_raw[(max_tile[0]-(thickness+2), y)]}"
            inner_portals = update_portal_location(inner_portals, portal_id, (max_tile[0]-(thickness+1), y))

    # get portals on top and bottom
    for x in range(2, max_tile[0]-1):
        if tiles_raw[(x, 0)] != " ":
            portal_id = f"{tiles_raw[(x, 0)]}{tiles_raw[(x, 1)]}"
            outer_portals = update_portal_location(outer_portals, portal_id, (x, 2))

        if tiles_raw[(x, max_tile[1]-1)] != " ":
            portal_id = f"{tiles_raw[(x, max_tile[1]-1)]}{tiles_raw[(x, max_tile[1])]}"
            outer_portals = update_portal_location(outer_portals, portal_id, (x, max_tile[1]-2))

        if tiles_raw[(x, thickness+2)] not in ". #" and tiles_raw[(x, thickness+3)] not in ". #":
            portal_id = f"{tiles_raw[(x, thickness+2)]}{tiles_raw[(x, thickness+3)]}"
            inner_portals = update_portal_location(inner_portals, portal_id, (x, thickness+1))
        
        if tiles_raw[(x, max_tile[1]-(thickness+3))] not in ". #" and tiles_raw[(x, max_tile[1]-(thickness+2))] not in ". #":
            portal_id = f"{tiles_raw[(x, max_tile[1]-(thickness+3))]}{tiles_raw[(x, max_tile[1]-(thickness+2))]}"
            inner_portals = update_portal_location(inner_portals, portal_id, (x, max_tile[1]-(thickness+1)))
    portals = {}
    outer_set = set()
    inner_set = set()
    for portal in inner_portals:
        for i in inner_portals[portal]:
            portals = update_portal_location(portals, portal, i)
            inner_set.add(i)
    for portal in outer_portals:
        for i in outer_portals[portal]:
            portals = update_portal_location(portals, portal, i)
            if portal not in ("AA", "ZZ"):
                outer_set.add(i)
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
    nodes_no_portals = {}
    for tile in tiles_raw:
        if tiles_raw[tile] == ".":
            adjacent = set()
            for a in get_adjacent(tile):
                if tiles_raw[a] == ".":
                    adjacent.add(a)
            nodes_no_portals[tile] = adjacent.copy()
            if tile in portal_locations:
                for portal in portals:
                    if tile in portals[portal]:
                        for i in portals[portal]:
                            if i != tile:
                                adjacent.add(i)
            nodes[tile] = adjacent.copy()

    portal_connections = {}
    for portal in inner_portals:
        for i in inner_portals[portal]:
            portal_connections[f"{portal}I"] = get_available_portals(i, inner_portals, outer_portals, nodes_no_portals)
    for portal in outer_portals:
        for i in outer_portals[portal]:
            portal_connections[f"{portal}O"] = get_available_portals(i, inner_portals, outer_portals, nodes_no_portals)

    return tiles_raw, nodes, start, end, outer_set, inner_set, portal_connections

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

def traverse_2d(current_portal, end_portal, portal_connections, traversed=-1):
    if traversed == -1:
        traversed = set([current_portal])
    if current_portal[:2] == end_portal[:2]:
        return 0, True
    adjacent = portal_connections[current_portal]
    min_distance = 0
    for portal in adjacent:
        if portal not in traversed:
            portal_opposite = portal[:2] + ("I" if portal[2] == "O" else "O")
            next_traversed = traversed.copy()
            next_traversed.add(portal)
            next_traversed.add(portal_opposite)
            distance, valid = traverse_2d(portal_opposite, end_portal, portal_connections, next_traversed)
            distance += portal_connections[current_portal][portal]
            if valid:
                if distance < min_distance or min_distance == 0:
                    min_distance = distance
    if min_distance == 0:
        return 0, False
    else:
        return min_distance+1, True

tiles, _, start, end, _, _, portal_connections = load_map()
distance, possible = traverse_2d("AAO", "ZZO", portal_connections)
print(f"Part 1: {distance-1}")

def traverse_p2(portal_connections, path=[("AAO", 0)], best_distance=-1, steps=0, max_depth=26):
    depth = path[-1][1]
    if depth > max_depth:
        return -1
    if depth == -1:
        return steps
    adjacent_portals = portal_connections[path[-1][0]]
    for portal in adjacent_portals:
        next_portal = (portal, depth)
        distance = steps + adjacent_portals[portal] + 1
        traversable = True
        if next_portal in path:
            traversable = False
        elif next_portal[0][:2] in ["AA", "ZZ"] and depth > 0:
            traversable = False
        elif next_portal[0][:2] not in ["AA", "ZZ"] and next_portal[0][2] == "O" and depth == 0:
            traversable = False
        elif distance >= best_distance and best_distance != -1:
            traversable = False
        if traversable:
            next_path = path + [next_portal] + [(next_portal[0][:2] + ("O" if next_portal[0][2] == "I" else "I"), depth + (-1 if next_portal[0][2] == "O" else 1))]
            d = traverse_p2(portal_connections, next_path, best_distance, distance)
            if d < best_distance or best_distance == -1:
                best_distance = d
    return best_distance

best_steps = traverse_p2(portal_connections) - 1
print(f"Part 2: {best_steps}")