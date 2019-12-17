from intcode import load_program, Controller

def read_controller_map(controller, i=0):
    tiles = {}
    halted = input_used = output_returned = False
    x = y = 0
    while not halted and not input_used:
        halted, input_used, output_returned = controller.step_until_action(i)
        if output_returned:
            tile = chr(controller.last_output)
            if tile == "\n":
                y += 1
                x = -1
            else:
                tiles[(x, y)] = tile
            x += 1
    return tiles, halted

def get_max_tiles(tiles):
    max_x = max_y = 0
    for tile in tiles:
        max_x = max(tile[0], max_x)
        max_y = max(tile[1], max_y)
    return max_x, max_y

def format_tiles_printing(tiles):
    max_x, max_y = get_max_tiles(tiles)
    r = ""
    for y in range(max_y+1):
        for x in range(max_x+1):
            tile = tiles.get((x, y), "?")
            r += {
                ".": " ",
                "#": "█"
            }.get(tile, tile)
        r += "\n"
    return r

def get_adjacent_positions(pos):
    adjacent = {
        ( pos[0]+1, pos[1]   ),
        ( pos[0]-1, pos[1]   ),
        ( pos[0]  , pos[1]+1 ),
        ( pos[0]  , pos[1]-1 )
    }
    return adjacent

def check_intersection(tiles, pos):
    adjacent = get_adjacent_positions(pos)
    intersection = True
    for a in adjacent:
        if a not in tiles or tiles[a] in ". ":
            intersection = False
            break
    return intersection and tiles[pos] == "#"

def get_program_inputs(program):
    program = [ord(i) for i in program] + [10]
    assert len(program) <= 21
    return program

def attempt_traversal(controller, routine, program_a, program_b, program_c):
    program = routine + "\n" + program_a + "\n" + program_b + "\n" + program_c + "\nn\n"
    halted = input_used = output_returned = False
    input_index = 0
    while input_index < len(program):
        _, input_used, output_returned = controller.step_until_action(ord(program[input_index]))
        if input_used:
            input_index += 1
    while not halted:
        halted, _, output_returned = controller.step_until_action(-1)
    assert halted
    return controller.last_output

controller = Controller(load_program("inputs/day-17.txt"))
tiles, _ = read_controller_map(controller)

intersection_sum = 0
for tile in tiles:
    if check_intersection(tiles, tile):
        tiles[tile] = "X"
        intersection_sum += tile[0] * tile[1]

print("Tiles:")
print(format_tiles_printing(tiles))
print()
print(f"Part 1: {intersection_sum}")

controller.reset()
controller.tape[0] = 2
# program -- ideally in the future this would be calculated not by hand
routine = "A,A,B,C,C,A,C,B,C,B"
a = "L,4,L,4,L,6,R,10,L,6"
b = "L,12,L,6,R,10,L,6"
c = "R,8,R,10,L,6"
print(f"Part 2: {attempt_traversal(controller, routine, a, b, c)}")