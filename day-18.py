def load_tiles(input_file="inputs/day-18.txt"):
    tiles = {}
    pos = (0, 0)
    with open(input_file, 'r') as f:
        for y, line in enumerate(f.readlines()):
            for x, val in enumerate(line.strip()):
                if val == "@":
                    pos = (x, y)
                    tiles[(x, y)] = "@"
                else:
                    tiles[(x, y)] = val
    return tiles, pos

def get_tile_bounds(tiles):
    # get bounds for x and y
    min_x = max_x = 0
    min_y = max_y = 0
    for tile in tiles:
        x, y = tile
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return (min_x, max_x+1), (min_y, max_y+1)

def get_string_map(tiles, pos=(0, 0)):
    x_bounds, y_bounds = get_tile_bounds(tiles)
    board = ""
    for y in range(y_bounds[0], y_bounds[1]):
        for x in range(x_bounds[0], x_bounds[1]):
            if (x, y) == pos:
                board += "@"
            else:
                board += tiles.get((x, y), " ")
        board += "\n"
    return board

def get_adjacent_tiles(pos):
    x, y = pos
    adjacent = {
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1)
    }
    return adjacent

def build_nodes(tiles):
    nodes = {}
    for tile in tiles:
        adjacent = {a for a in get_adjacent_tiles(tile) if a in tiles and tiles[a] != "#"}
        nodes[tile] = adjacent
    return nodes

def get_all_keys(tiles):
    return [tile for tile in tiles if tiles[tile] in "abcdefghijklmnopqrstuvwxyz@"]

def get_distance(tiles, nodes, pos, end_pos, keys, traversed=-1):
    if traversed == -1:
        traversed = set()
    if pos == end_pos:
        return 0, True
    adjacent = nodes[pos]
    min_distance = -2
    for node in adjacent:
        if node not in traversed:
            if tiles[node] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and tiles[node].lower() not in keys:
                return 0, False
            traversed.add(node)
            distance, possible = get_distance(tiles, nodes, node, end_pos, keys, traversed=traversed.copy())
            if possible and distance != -1:
                min_distance = distance if min_distance == -2 else min(distance, min_distance)
    return min_distance + 1, min_distance != -2

def get_key_distances(tiles, pos, keys=set()):
    key_distances = {}
    all_keys = get_all_keys(tiles)
    nodes = build_nodes(tiles)
    for key_pos in all_keys:
        distance, possible = get_distance(tiles, nodes, pos, key_pos, keys)
        if possible:
            key_distances[tiles[key_pos]] = distance
    return key_distances

def get_key_pos(tiles, key):
    for tile in tiles:
        if tiles[tile] == key:
            return tile
    return (0, 0)

def get_closest_key(tiles, pos, keys=set()):
    key_distances = get_key_distances(tiles, pos, keys)
    min_distance = -1
    min_key = ""
    key_pos = (0, 0)
    for key in key_distances:
        if key not in keys:
            if min_distance == -1 or key_distances[key] < min_distance:
                min_distance = key_distances[key]
                min_key = key
                key_pos = get_key_pos(tiles, min_key)
    return min_key, key_pos, min_distance

def traverse_keys_naiive(tiles, pos, keys=set()):
    # this probably needs to be migrated to BFS to work properly
    # this solution does work however but is to slow to apply
    # TL;DR recursion bad
    key_distances = get_key_distances(tiles, pos, keys)
    available_keys = {key for key in key_distances if key not in keys}
    min_distance = 0
    for key in available_keys:
        next_keys = keys.copy()
        next_keys.add(key)
        distance = traverse_keys_naiive(tiles, get_key_pos(tiles, key), next_keys) + key_distances[key]
        if min_distance == 0:
            min_distance = distance
        else:
            min_distance = min(min_distance, distance)
    return min_distance

def get_key_distance(tiles, nodes, pos, end_pos, keys=-1, traversed=-1):
    if keys == -1:
        keys = set()
    if traversed == -1:
        traversed = set()
    if pos == end_pos:
        return 0, True, keys
    adjacent = nodes[pos]
    min_distance = -2
    more_keys = set()
    for node in adjacent:
        if node not in traversed:
            if tiles[node] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                keys.add(tiles[node].lower())
            traversed.add(node)
            distance, possible, next_stage_keys = get_key_distance(tiles, nodes, node, end_pos, keys.copy(), traversed.copy())
            if possible and distance != -1:
                if min_distance == -2:
                    min_distance = distance
                    more_keys = next_stage_keys
                else:
                    if distance < min_distance:
                        min_distance = distance
                        more_keys = next_stage_keys
    return min_distance + 1, min_distance != -2, more_keys

def get_key_traversal(start, end, key_distances, keys=-1):
    if keys == -1:
        keys = set()
    distance, intermediate = key_distances[start][end]
    needed_keys = keys.difference(intermediate)
    keys.add(start)
    if len(needed_keys) == 0:
        return distance
    min_additional = -1
    for key in needed_keys:
        i, _ = key_distances[start][key]
        d = get_key_traversal(key, end, key_distances, keys.copy()) + i
        if d < min_additional or min_additional == -1:
            min_additional = d
    return min_additional

def calculate_distances(tiles):
    nodes = build_nodes(tiles)
    # first get the distance between different keys and prereqs
    keys = get_all_keys(tiles)
    key_distances = {tiles[i]: {} for i in keys} # {key: {other: (distance, prereq)}}
    for key in keys:
        for other in keys:
            if other != key:
                distance, valid, keys_needed = get_key_distance(tiles, nodes, key, other)
                key_distances[tiles[key]][tiles[other]] = (distance, keys_needed)
    # then take those precalculated distances and work backwards while finding the shortest path
    return key_distances

tiles, pos = load_tiles()
# print(traverse_keys_naiive(tiles, pos))
distances = calculate_distances(tiles)
print(get_key_traversal("@", "g", distances))
for tile in distances:
    print(f"--- {tile} ---")
    for j in distances[tile]:
        print(f"   -> {j} {distances[tile][j]}")