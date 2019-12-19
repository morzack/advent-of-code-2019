from intcode import Controller, load_program
import math

def check_pulling(controller, pos):
    controller.reset()
    assert len(pos) == 2
    for i in pos:
        _, input_used, _ = controller.step_until_action(i)
        assert input_used
    _, _, output_returned = controller.step_until_action(0)
    assert output_returned
    return controller.last_output == 1

def query_square(controller, distance):
    # make this not O(n^2) using trig 4head
    tiles = set()
    for x in range(distance):
        for y in range(distance):
            tile = (x, y)
            pulling = check_pulling(controller, tile)
            if pulling:
                tiles.add(tile)
    return tiles

def expand_square(controller, distance):
    tiles = set()
    adding_x = started_x = False
    adding_y = started_y = False
    for i in range(distance+1)[::-1]:
        if not adding_x and not adding_y and started_x and started_y:
            break
        tile_y, tile_x = (i, distance), (distance, i)
        if not started_x or adding_x:
            if check_pulling(controller, tile_x):
                tiles.add(tile_x)
                started_x = True
                adding_x = True
            else:
                adding_x = False
        if not started_y or adding_y:
            if check_pulling(controller, tile_y):
                tiles.add(tile_y)
                started_y = True
                adding_y = True
            else:
                adding_y = False
    return tiles

def check_square_fit(tiles, side_length, pos):
    x, y = pos
    for dx in range(side_length):
        for dy in range(side_length):
            if (x+dx, y+dy) not in tiles:
                return False
    return True

def check_fit(tiles, side_length):
    min_x = min_y = -1
    for start_pos in tiles:
        if check_square_fit(tiles, side_length, start_pos):
            x, y = start_pos
            if x < min_x and y < min_y or min_x == -1 and min_y == -1:
                min_x, min_y = x, y
    return (min_x, min_y)

def draw_beam(tiles, side_length):
    for y in range(side_length):
        for x in range(side_length):
            if (x, y) in tiles:
                print("#", end="")
            else:
                print(" ", end="")
        print("")
    print("")

def get_box_pos(controller, box_size):
    # Original solution involved brute forcing the size
    # this just goes down and across until we get one that's large enough
    y = box_size
    x = 0
    while True:
        while check_pulling(controller, (x, y)) == 0:
            x += 1
        if check_pulling(controller, (x+box_size-1, y-box_size+1)) == 1:
            return (x, y-box_size+1)
        y += 1

tractor_controller = Controller(load_program("inputs/day-19.txt"))
print(f"Part 1: {len(query_square(tractor_controller, 50))}")

box_pos = get_box_pos(tractor_controller, 100)
print(f"Part 2: {box_pos[0]*10000 + box_pos[1]}")