def load_input(filename="inputs/day-24.txt"):
    lines = [i.strip() for i in open(filename).readlines()]
    tiles = {}
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            tiles[(x, y)] = col == "#"
    return tiles

def get_adjacent(pos):
    x, y = pos
    return {
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1)
    }

def get_bounds(tiles):
    min_x = min_y = max_x = max_y = 0
    for tile in tiles:
        x, y = tile
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return (min_x, min_y), (max_x+1, max_y+1)

def process_tiles(tiles):
    new_tiles = {}
    min_tile, max_tile = get_bounds(tiles)
    for x in range(min_tile[0], max_tile[0]):
        for y in range(min_tile[1], max_tile[1]):
            sum_living = 0
            for tile in get_adjacent((x, y)):
                if tiles.get(tile, False):
                    sum_living += 1
            if tiles[(x, y)]:
                new_tiles[(x, y)] = sum_living == 1
            else:
                new_tiles[(x, y)] = sum_living in [1, 2]
    return new_tiles

def print_tiles(tiles):
    min_tile, max_tile = get_bounds(tiles)
    for row in range(min_tile[1], max_tile[1]):
        for col in range(min_tile[0], max_tile[0]):
            if tiles[(col, row)]:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()

def get_tile_immutable(tiles):
    living = set()
    for tile in tiles:
        if tiles[tile]:
            living.add(tile)
    return frozenset(living)

def run_tiles(tiles):
    # run until we get a layout that appears twice
    previous_layouts = set()
    while get_tile_immutable(tiles := process_tiles(tiles)) not in previous_layouts:
        previous_layouts.add(get_tile_immutable(tiles))
    return tiles

def get_biodiversity_rating(tiles):
    rating = 0
    for tile in tiles:
        if tiles[tile]:
            x, y = tile
            pos = x + y * 5
            rating += 2 ** pos
    return rating

tiles = load_input()
final_state = run_tiles(tiles)
print_tiles(final_state)
print(f"Part 1: {get_biodiversity_rating(final_state)}")