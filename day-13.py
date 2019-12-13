from intcode import Controller, load_program

controller = Controller(load_program("inputs/day-13.txt"))
controller.tape[0] = 2

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def get_tile(tiles, x, y):
    return tiles.get((x, y), EMPTY)

def set_tile(tiles, x, y, tile):
    tiles[(x, y)] = tile
    return tiles

def get_tile_pos(tiles, tile_type):
    for pos in tiles:
        if tiles[pos] == tile_type:
            return pos
    return (-1, -1)

def get_paddle_dir(tiles):
    paddle_pos = get_tile_pos(tiles, PADDLE)
    ball_pos = get_tile_pos(tiles, BALL)
    return -1 if paddle_pos[0] > ball_pos[0] else 0 if paddle_pos[0] == ball_pos[0] else 1

def get_outputs(controller, tiles, i=-2):
    outputs = []
    score = 0
    input_used = halted = False
    while not (input_used or halted):
        halted, input_used, output_sent = controller.step_until_action(get_paddle_dir(tiles) if i == -2 else i)
        outputs.append(controller.last_output)
        if len(outputs) == 3:
            x, y, tile = outputs
            if x == -1 and y == 0:
                score = tile
            tiles = set_tile(tiles, x, y, tile)
            outputs = []
    return tiles, score, halted, input_used, output_sent
tiles, score, halted, _, _ = get_outputs(controller, {}, i=0)

def count_tiles(tiles, tile_type):
    blocks = 0
    for pos in tiles:
        if tiles[pos] == tile_type:
            blocks += 1
    return blocks

def render_tiles(tiles):
    for y in range(23):
        s = ""
        for x in range(42):
            s += {
                EMPTY: " ",
                WALL: "█",
                BLOCK: "#",
                PADDLE: "-",
                BALL: "o"
            }[get_tile(tiles, x, y)]
        print(s)

print(f"Part 1: {count_tiles(tiles, BLOCK)}")

rendering = False
if rendering:
    import os, time

while not halted:
    new_tiles, score, halted, _, _ = get_outputs(controller, tiles)

    for tile in new_tiles:
        tiles = set_tile(tiles, tile[0], tile[1], new_tiles[tile])

    if rendering:
        os.system("clear")
        render_tiles(tiles)
        print(score)
        time.sleep(0.01)

print(f"Part 2: {score}")